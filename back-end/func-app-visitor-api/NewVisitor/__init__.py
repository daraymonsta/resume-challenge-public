import logging
import azure.functions as func
from shared_code import extra_func, db_func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # assign the url passed in to a variable
    urlstr = extra_func.get_parameter('url', req)

    if urlstr and urlstr != "{*url}":

        valid_url = extra_func.check_valid_url(urlstr)
        if valid_url == True:
            logging.info(f'The url {urlstr} is valid')

            # setup connection to cosmos DB + container
            container = db_func.setup_db_and_container("ResumeDB", "VisitorCount")

            # get visitor record from DB query already done using url parameter
            visitor_record_list = db_func.query_records_by_url(container, urlstr)
            if len(visitor_record_list) == 1:
                logging.info(f"A record exists for {urlstr}")
                # there's only one record as there should be for a url, so continue
                read_item = db_func.read_record(visitor_record_list[0], container)
                
                # increment visitor counter by 1 and update record
                read_item['visitorCounter'] = read_item['visitorCounter'] + 1
                updated_item = db_func.update_record(read_item, container)
                logging.info('Replaced Item\'s Id is {0}, new visitorCounter={1}'.format(updated_item['id'], updated_item['visitorCounter']))
                status_code_value = 200
                json_return_data = extra_func.create_json_to_return(status_code_value, updated_item['visitorCounter'])
                json_to_return = extra_func.wrap_json_for_response(json_return_data)
                return func.HttpResponse(json_to_return, mimetype='text/javascript')
            elif len(visitor_record_list) == 0:
                # this is the first time this url has logged a visitor, so create initialise a new visitor record
                logging.info('No visitor record exists for this url. Creating one...')
                new_url_visitor_dict = extra_func.create_new_url_visitor_dict(urlstr)
                db_func.create_record(new_url_visitor_dict, container)
                logging.info(f"Created new visitor record for {urlstr}. Visitor count initialised at 1.")

                status_code_value = 200
                json_return_data = extra_func.create_json_to_return(status_code_value, 1)
                json_to_return = extra_func.wrap_json_for_response(json_return_data)
                return func.HttpResponse(json_to_return, mimetype='text/javascript')
            else:
                return func.HttpResponse(
                    "Multiple records for this url. Remove duplicate record(s) so that visitor count can be checked.",
                    status_code=400
                )
        else:
            return func.HttpResponse(
                "Invalid url. Visitor count cannot be checked.",
                status_code=400
            )
            
    else:
        return func.HttpResponse(
             "No url was passed. Visitor count cannot be checked.",
             status_code=400
        )
