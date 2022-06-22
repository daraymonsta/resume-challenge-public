import logging
import pytest
import azure.functions as func
import io
import sys


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    stdout_bak = sys.stdout  # backup stdout
    sys.stdout = io.StringIO()
    # run pytests
    pytest.main(["-x", "tests"])
    output = sys.stdout.getvalue()
    sys.stdout.close()
    sys.stdout = stdout_bak  # restore stdout

    return func.HttpResponse(str(output), status_code=200)
