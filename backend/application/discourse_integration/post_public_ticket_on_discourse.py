from application.models import *
from application.discourse_integration.discourse_config import *
import json
from application.logger import logger


def post_public_ticket_on_discourse(Discourse_Username,public_ticket_title,public_ticket_content,public_ticket_category):
        result = d_session.post( Discourse_path + '/posts.json',data = {"title":public_ticket_title,
                "raw": public_ticket_content,
                "category":Discourse_Categories[public_ticket_category],
                },
                headers={"Api-Key": Discourse_Admin_key,
                    "Api-Username":Discourse_Username })
        

        print(result.text)
        print(result.status_code)
        if result.status_code == 200:
            output = json.loads(result.text)
            print(output)
            discourse_public_ticket_url = "http://localhost:4200/t/" +  str(output['topic_slug']) + "/" + str(output['topic_id'])
            logger.info("post_created_on_discourse: ", output)
            return discourse_public_ticket_url
        else:
            return "failed"               