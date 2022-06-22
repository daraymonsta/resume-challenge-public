# runs the speed tests: cosmos bindings vs no-bindings in fucntion.json
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
    response = requests.get('http://localhost:7071/api/AddAVisitor/' + test_input)
    json_return_data = extra_func.create_json_to_return(200, expected)
    response_to_match = (extra_func.wrap_json_for_response(json_return_data)).encode('UTF-8')
    assert response.content == response_to_match, f"Should have a value of {expected}"


@pytest.mark.parametrize("test_input", [("rayrossi0000001.net"), ("rayrossi0000001.net/test/index.html")])
def test_delete_visitor(test_input):
    db_func.delete_record_with_url(test_input)