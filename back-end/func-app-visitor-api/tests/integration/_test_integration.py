# runs the integration tests
import requests
from shared_code import db_func, extra_func
import pytest


@pytest.mark.parametrize("test_input,expected", [
    ("rayrossi0000001.net", 1),
    ("rayrossi0000001.net", 2),
    ("rayrossi0000001.net/test/index.html", 1),
    ("rayrossi0000001.net/test/index.html", 2)
    ])
def test_new_visitor(test_input, expected):
    # test_urlstr = "rayrossi0000001.net/folder/index.html"
    response = requests.get('http://localhost:7071/api/ANewVisitor/' + test_input)
    json_return_data = extra_func.create_json_to_return(200, expected)
    response_to_match = (extra_func.wrap_json_for_response(json_return_data)).encode('UTF-8')
    assert response.content == response_to_match, f"Should have a value of {expected}"


@pytest.mark.parametrize("test_input", [("rayrossi0000001.net"), ("rayrossi0000001.net/test/index.html")])
def test_delete_url(test_input):
    # setup connection to cosmos DB + container
    container = db_func.setup_db_and_container("ResumeDB", "VisitorCount")
    filter_records_list = db_func.query_records_by_url(container, test_input)
    record_to_delete_id = filter_records_list[0]["id"]
    response = requests.get('http://localhost:7071/api/Delete?id=' + record_to_delete_id)
    # encode string as bytes so will match reponse.content (which is in bytes)
    response_to_match = f"Deleted visitor record with id: {record_to_delete_id}".encode('UTF-8')
    assert response.content == response_to_match, "Should say 'Deleted visitor record with id: [id]"

def test_invalid_url_is_caught():
    test_urlstr = "rayrossi0000001..."
    response = requests.get('http://localhost:7071/api/ANewVisitor/' + test_urlstr)
    response_to_match = b"Invalid url. Visitor count cannot be checked."
    assert response.content == response_to_match, "Should say: Invalid url. Visitor count cannot be checked."
