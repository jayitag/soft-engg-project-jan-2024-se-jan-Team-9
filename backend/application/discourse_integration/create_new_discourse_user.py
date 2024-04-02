from application.models import *
from application.discourse_integration.discourse_config import *
import json

def create_new_discourse_user(user_id):
        user = Auth.query.filter_by(user_id=user_id).first()
        name = str(user.first_name + " " + user.last_name)
        email = str(user.email)
        username= str(str(user.email).split('@')[0])
        password = str(user.password)
        result = d_session.post( Discourse_path + '/users.json',data = {"name":name,
                "email": email,
                "password": password,
                "username":username,
                "active": True,
                "approved": True,
                "user_fields[1]": True,
                "external_ids": {}
                },
                headers={"Api-Key": Discourse_Admin_key,
                    "Api-Username":Discourse_Admin_username })
        # print(name)
        # print(email)
        # print(username)
        # print(password)

        print(result.text)
        print(result.status_code)
        if result.status_code == 200:
            output = json.loads(result.text)
            print(output)
            if output['success'] == True:
                if output['active'] == True: 
                    user.discourse_id = output['user_id']
                    user.discourse_username = username
                    db.session.commit()
                    
                    return "success"
                if output['active'] == False:
                    return "account not activated"
        else:
            return "failed"               