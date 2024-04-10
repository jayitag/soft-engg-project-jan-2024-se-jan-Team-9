from application.globals import API_VERSION
# # from conftest_dev import (
# #     admin_user_id,
# #     admin_web_token,
# # )

import json
from conftest import *
from application.database import db
from application.models import Auth
ticketId='75e291e73487d329436f53cc55dfb1c8'

def test_get_chat(test_client):
    # Set up authentication headers
    headers = {
        "Content-type": "application/json",
        "web_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InN0dWRlbnQxQGdtYWlsLmNvbSIsImV4cGlyeSI6MTcxMjI2MDY4OX0.7jCDtpcGg-nvWP_fthvqGRdr1wmECQg0G3yBpY0nj2U",  
        "user_id": student_user_id,
    }

    response = test_client.get(
        f"/api/v1/chat/{ticketId}/{student_user_id}",
        headers=headers,
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "message" in data

def test_authinticate_chat(test_client):
    # Set up authentication headers
    headers = {
        "Content-type": "application/json",
        "web_token": "noToken",  
        "user_id": student_user_id,
    }

    response = test_client.get(
        f"/api/v1/chat/{ticketId}/{student_user_id}",   
    )
    assert response.status_code == 404

def test_add_massage_to_chat(test_client):
    # Set up authentication headers
    headers = {
        "Content-type": "application/json",
        "web_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InN0dWRlbnQxQGdtYWlsLmNvbSIsImV4cGlyeSI6MTcxMjI2MDY4OX0.7jCDtpcGg-nvWP_fthvqGRdr1wmECQg0G3yBpY0nj2U",  
        "user_id": student_user_id,
    }

    data = {
             "new_message": "Something"
    }

# Convert Python dictionary to JSON string
    json_data = json.dumps(data)

    response = test_client.put(
        f"/api/v1/chat/{ticketId}/{student_user_id}",
        headers=headers,
        data=json_data
    )
    assert response.status_code == 200

def test_add_unauthorised_massage_to_chat(test_client):
    # Set up authentication headers
    headers = {
        "Content-type": "application/json",
        "web_token": "randomekey",  
        "user_id": student_user_id,
    }

    data = {
             "new_message": ""
    }

# Convert Python dictionary to JSON string
    json_data = json.dumps(data)

    response = test_client.get(
        f"/api/v1/chat/{ticketId}/{student_user_id}",
        headers=headers,
        data=json_data
    )
    assert response.status_code == 401