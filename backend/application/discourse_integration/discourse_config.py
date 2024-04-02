import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


Discourse_Admin_key = "2bf3c186b80f30c7fa7dea26841a4a1aab63b7c3d91d889ec7f832774f0aab54"
Discourse_Admin_username = "admin_discourse"
Discourse_Admin_email = "admin_discourse@gmail.com"

Discourse_Categories = {"Operational":5,"Admistration":6,"Accounts":7,"Web Op":8}

Discourse_path = "http://127.0.0.1:4200"

d_session = requests.Session()
adapter = HTTPAdapter(max_retries=Retry(connect=3, backoff_factor=0.5))
d_session.mount('http://', adapter)