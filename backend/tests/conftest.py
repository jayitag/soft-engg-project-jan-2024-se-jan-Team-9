# Online Support Ticket Application
# Tushar Supe : 21f1003637
# Vaidehi Agarwal: 21f1003880
# File Info: Contains fixtures for testing.

# --------------------  Imports  --------------------

from application import create_app
import pytest
from application.logger import logger

# --------------------  Constants  --------------------

# Please set following required constants to mimic a specific user role.

# STUDENT
student_user_id = "5e223a298a380579d1108529d299484e"
student_web_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InN0dWRlbnQxQGdtYWlsLmNvbSIsImV4cGlyeSI6MTcxMjI1NDQzNn0.wdxZ6lQIutGDdr4FMS-X6ltvFfg3nP9k3TA9qU-i0os"
 
# SUPPORT
support_user_id = "a5997f803b4dfbdb0a7f17b012ca1697"
support_web_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InN0dWRlbnQxQGdtYWlsLmNvbSIsImV4cGlyeSI6MTcxMjI1NDQzNn0.wdxZ6lQIutGDdr4FMS-X6ltvFfg3nP9k3TA9qU-i0os"

# ADMIN
admin_user_id = "3ad51db3c4defba9c7f1ca7549712e25"
admin_web_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InN0dWRlbnQxQGdtYWlsLmNvbSIsImV4cGlyeSI6MTcxMjI1NDQzNn0.wdxZ6lQIutGDdr4FMS-X6ltvFfg3nP9k3TA9qU-i0os"

# --------------------  Code  --------------------

# before testing set current dir to `\code\backend`
@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app(env_type="dev")
    logger.info("Testing fixture set.")
    
    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as testing_client:
        # Establish an application context
        with flask_app.app_context():
            yield testing_client  # this is where the testing happens!