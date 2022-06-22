import logging
import azure.functions as func
from shared_code import extra_func, db_func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # assign the id passed in to a variable
    para_id = extra_func.get_parameter('id', req)

    if para_id:
        database = db_func.if_not_exists_create_db('ResumeDB')
        container = db_func.if_not_exists_create_container('VisitorCount', database)
        db_func.delete_record(para_id, container)
        logging.info('Deleted item\'s Id is {0}'.format(para_id))
        return func.HttpResponse(f"Deleted visitor record with id: {para_id}", status_code=200)
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass in the record's id to delete that record.",
             status_code=200
        )
