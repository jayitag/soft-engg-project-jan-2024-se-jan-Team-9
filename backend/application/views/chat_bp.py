import hashlib
import time
from flask import Blueprint, request
from flask_restful import Api, Resource
from application.logger import logger
from application.common_utils import (
    token_required,
    users_required,
    )

from application.views.user_utils import UserUtils
from application.responses import *
from application.models import *
from copy import deepcopy
from application.globals import *
from application.notifications import send_email
from application.views.ticket_bp import ticket_utils, ticket_api

chat_bp = Blueprint("chat_bp", __name__)
chat_api = Api(chat_bp)

class chatAPI(Resource):
    @token_required
    @users_required(users=["student","support"])
    def get(self,ticket_id="",user_id=""):
        # return "hello"

        if ticket_utils.is_blank(ticket_id) or ticket_utils.is_blank(user_id):
            raise BadRequest(status_msg="User id or ticket id is missing.")
        
        try:
            ticket = Ticket.query.filter_by(ticket_id=ticket_id).first()
        except Exception as e:
            logger.error(
                f"TicketAPI->get : Error occured while fetching ticket data : {e}"
            )
            raise InternalServerError
        else:
            if ticket:
                # if user.role == "student":
                    # user = Auth.query.filter_by(user_id=user_id).first()
                    # if user_id == ticket.created_by:
                chat = ticket.chat
                return success_200_custom(data=chat)
                

    @token_required
    @users_required(users=["student","support"])
    def put(self,ticket_id="",user_id=""):


        details = {
            
            "new_message": "",

        }

        if ticket_utils.is_blank(ticket_id) or ticket_utils.is_blank(user_id):
            raise BadRequest(status_msg="User id or ticket id is missing.")
        

         # check form data
        try:
            form = request.get_json()
            for key in details:
                value = form.get(key, "")
                if ticket_utils.is_blank(value):
                    value = ""
                details[key] = value
        except Exception as e:
            logger.error(
                f"TicketAPI->put : Error occured while getting form data : {e}"
            )
            raise InternalServerError
        

        try:
            ticket = Ticket.query.filter_by(ticket_id=ticket_id).first()
            user = Auth.query.filter_by(user_id=user_id).first()
        except Exception as e:
            logger.error(
                f"TicketAPI->get : Error occured while fetching ticket data : {e}"
            )
            raise InternalServerError
        else:
            if ticket:
                user = Auth.query.filter_by(user_id=user_id).first()
                if user_id == ticket.created_by or user.role == "student":
                    ticket.status= "unresolved"
                    ticket.chat = str(ticket.chat[:-1]) + str(",") + str("{") + str("\"name\":\"") + str(user.first_name) + str(" ") + str(user.last_name) + str("\",") + str("\"role\":\"") + str(user.role) + str("\",") + str("\"chat\":\"") + str(details["new_message"]) + str("\",") + str("\"date_time\":\"") + str(time.time()) + str("\"}") + str("]")
                    db.session.commit()
                    return success_200_custom(data=ticket.chat)
                elif user.role == "support":
                    ticket.status= "resolved"
                    ticket.chat = str(ticket.chat[:-1]) + str(",") + str("{") + str("\"name\":\"") + str(user.first_name) + str(" ") + str(user.last_name) + str("\",") + str("\"role\":\"") + str(user.role) + str("\",") + str("\"chat\":\"") + str(details["new_message"]) + str("\",") + str("\"date_time\":\"") + str(time.time()) + str("\"}") + str("]")
                    db.session.commit()
                    return success_200_custom(data=ticket.chat)

                


chat_api.add_resource(chatAPI,'/<string:ticket_id>/<string:user_id>')
