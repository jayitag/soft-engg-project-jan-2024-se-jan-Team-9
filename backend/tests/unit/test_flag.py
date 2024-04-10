from application.globals import API_VERSION
# # from conftest_dev import (
# #     admin_user_id,
# #     admin_web_token,
# # )

import json
from conftest import *
from application.database import db
from application.models import Auth
ticketId='4a998a50872adb240f50fc3cbddc5747'

def test_get_flag(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/tickets/user/{user_id}' endpoint is requested (GET) by a student
    THEN check that the response is 200 and contains all tickets created 
    """


    response = test_client.get(
        f"/api/v1/admin/flag",
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'flagdata' in data
    assert isinstance(data["flagdata"], list)
    if len(data["flagdata"]) !=0 :
        assert 'created_on' in data["flagdata"][0]
        assert 'description' in data["flagdata"][0]
        assert 'id' in data["flagdata"][0]
        assert 'title' in data["flagdata"][0]


def test_put_flag(test_client):
    data = {
            "flag_type": "string",
            "is_flag": "False"
    }

# Convert Python dictionary to JSON string
    json_data = json.dumps(data)

# Assuming ticketId is already defined
    response = test_client.put(
        f"/api/v1/admin/flag/{ticketId}",
        data=json_data,  # Pass JSON data here
        content_type='application/json'  # Specify content type as JSON
    )
    
    assert response.status_code == 200
    