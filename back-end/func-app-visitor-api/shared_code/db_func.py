# database functions
import logging
import os
from azure.cosmos import CosmosClient, PartitionKey
import azure.functions as func
from shared_code import extra_func

def setup_db_and_container(database_name, container_name):
    database = if_not_exists_create_db('ResumeDB')
    container = if_not_exists_create_container('VisitorCount', database)
    return container

def if_not_exists_create_db(database_name):
    endpoint = os.getenv('AzureCosmosDBAccountEndpoint')
    key = os.getenv('AzureCosmosDBAccountKey')
    client = CosmosClient(endpoint, key)
    database = client.create_database_if_not_exists(id=database_name)
    return database

def if_not_exists_create_container(container_name, database):
    container = database.create_container_if_not_exists(id=container_name,partition_key=PartitionKey(path="/name"),
    offer_throughput=400)
    return container

def read_record(visitor_record_json, container):
    read_item = container.read_item(item=visitor_record_json['id'], partition_key=visitor_record_json['id'])
    return read_item

def update_record(read_item, container):
    updated_item = container.replace_item(item=read_item, body=read_item)
    return updated_item

def create_record(new_item, container):
    created_item = container.create_item(body=new_item)
    return created_item

def create_new_visitor_record(newvisitor_dict, cosmos_out_binding):
    newdocs = func.DocumentList() 
    newdocs.append(func.Document.from_dict(newvisitor_dict))
    return cosmos_out_binding.set(newdocs)

def list_all_records(container, orderby_field, reverse_bool):
    # enable_cross_partition_query should be set to True as the container is partitioned
    items = list(container.query_items(
        query="SELECT * FROM c",
        enable_cross_partition_query=True
    ))
    
    if orderby_field == 'id':
        items.sort(key=extra_func.get_id, reverse=reverse_bool)
    elif orderby_field == 'url':
        items.sort(key=extra_func.get_url, reverse=reverse_bool)
    elif orderby_field == 'visitorCounter':
        items.sort(key=extra_func.get_visitorCounter, reverse=reverse_bool)
    
    return items

def query_records_by_url(container, urlstr):
    # enable_cross_partition_query should be set to True as the container is partitioned
    items = list(container.query_items(
        query="SELECT * FROM c WHERE c.url=@url",
        parameters=[
            { "name":"@url", "value": urlstr }
        ],
        enable_cross_partition_query=True
    ))
    return items

def delete_record(doc_id, container):
    deleted_item = container.delete_item(item=doc_id, partition_key=doc_id)
    return deleted_item

def delete_record_with_url(urlstr):
    # setup connection to cosmos DB + container
    container = setup_db_and_container("ResumeDB", "VisitorCount")
    filter_records_list = query_records_by_url(container, urlstr)
    record_to_delete_id = filter_records_list[0]["id"]
    response = delete_record(record_to_delete_id, container)
