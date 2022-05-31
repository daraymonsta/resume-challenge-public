# extra functions
import logging
import uuid
import validators

def get_parameter(parameter_name, req_binding):

    temp_parameter_str = req_binding.route_params.get(parameter_name)
    if not temp_parameter_str:
        temp_parameter_str = req_binding.params.get(parameter_name)

    # if can't get url from route parameter string, get from request body
    if not temp_parameter_str:
        try:
            req_body = req_binding.get_json()
        except ValueError:
            pass
        else:
            temp_parameter_str = req_body.get(parameter_name)

    logging.info('{0} passed: {1}'.format(parameter_name, temp_parameter_str))  
    return temp_parameter_str

def check_valid_url(urlstr):
    # check urlstr is a valid url
    if urlstr.startswith('https://') or urlstr.startswith('http://'):
        urlprefix = ""
    else:
        urlprefix = "https://"
    url_to_test = urlprefix + urlstr
    return validators.url(url_to_test)

def create_new_url_visitor_dict(urlstr):
    new_url_visitor_dict = {
        "id": str(uuid.uuid4()),
        "visitorCounter": 1,
        "url": urlstr
    }
    return new_url_visitor_dict

# custom functions to get visitor record info
# --------------------------------------------
def get_id(item):
    return item.get('id')

def get_url(item):
    return item.get('url')

def get_visitorCounter(item):
    return item.get('visitorCounter')
# --------------------------------------------

def create_json_to_return(status_code_value, visitor_count):
    return {
        'code': status_code_value,
        'value': visitor_count
    }

def wrap_json_for_response(json_data):
    return f"/**/ typeof liveViews === 'function' && liveViews({json_data});"