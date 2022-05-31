import logging
import json
import azure.functions as func
from shared_code import extra_func, db_func

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    database = db_func.if_not_exists_create_db('ResumeDB')
    container = db_func.if_not_exists_create_container('VisitorCount', database)
    
    # assign the id passed in to a variable
    para_orderby = extra_func.get_parameter('orderby', req)
    # set default for orderby (if no parameter passed)
    if not para_orderby:
        para_orderby = "id"
    para_rev = extra_func.get_parameter('rev', req)
    # set default for rev parameter
    para_rev_bool = False
    if para_rev == "true":  # anything else will not reverse the orderby
        para_rev_bool = True

    logging.info(f'Sorting by {para_orderby}')
    if para_orderby == "id":
        items = db_func.list_all_records(container,'id', para_rev_bool)
    elif para_orderby == "url":
        items = db_func.list_all_records(container,'url', para_rev_bool)
    elif para_orderby == "visitors":
        items = db_func.list_all_records(container,'visitorCounter', para_rev_bool)
    return func.HttpResponse(
        json.dumps(items, indent=2, separators=(',', ': '), sort_keys=False),
            status_code=200
    )