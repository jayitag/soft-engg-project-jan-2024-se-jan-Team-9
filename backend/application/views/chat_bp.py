import hashlib
import time
from flask import Blueprint, request
from flask_restful import Api, Resource
from application.logger import logger
from application.common_utils import (
    token_required,
    users_required,
    is_img_path_valid,
    convert_img_to_base64,
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


def get_chat_attachments(ticket_id):
        ticket_attch = TicketAttachment.query.filter_by(ticket_id=ticket_id).all()
        attachments = []
        for att in ticket_attch:
            file_path = att.attachment_loc
            img_base64 = ""
            if is_img_path_valid(file_path):
                img_base64 = convert_img_to_base64(file_path)
            d_ = {"user_id": att.user_id, "attachment_loc": img_base64}
            attachments.append(d_)
        return attachments

class chatAPI(Resource):
    @token_required
    @users_required(users=["student","support", "admin"]) # admin added by Harman
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
                commented_by_user = Auth.query.filter_by(user_id=user_id).first()
                if user_id == ticket.created_by or commented_by_user.role == "student":
                    ticket.status= "unresolved"
                    ticket.chat = str(ticket.chat[:-1]) + str(",") + str("{") + str("\"name\":\"") + str(commented_by_user.first_name) + str(" ") + str(commented_by_user.last_name) + str("\",") + str("\"role\":\"") + str(commented_by_user.role) + str("\",") + str("\"chat\":\"") + str(details["new_message"]) + str("\",") + str("\"date_time\":\"") + str(time.time()) + str("\",") + str("\"is_attachment\":\"") + str(False) + str("\"}") + str("]")
                    db.session.commit()
                    return success_200_custom(data=ticket.chat)
                elif user.role == "support":
                    ticket.status= "resolved"
                    ticket.chat = str(ticket.chat[:-1]) + str(",") + str("{") + str("\"name\":\"") + str(commented_by_user.first_name) + str(" ") + str(commented_by_user.last_name) + str("\",") + str("\"role\":\"") + str(commented_by_user.role) + str("\",") + str("\"chat\":\"") + str(details["new_message"]) + str("\",") + str("\"date_time\":\"") + str(time.time()) + str("\",") + str("\"is_attachment\":\"") + str(False) + str("\"}") + str("]")
                    db.session.commit()
                    try:
                        ticeket_created_by_user = Auth.query.filter_by(user_id = ticket.created_by).first()
                        
                        resp = send_email(
                            occasion = "ticket_resolution",
                            to=[{"email": ticeket_created_by_user.email,"username": ticeket_created_by_user.first_name}],
                            _from=commented_by_user.email,
                            subject="Your ticket is resolved",
                            data = {"username": ticeket_created_by_user.first_name, "ticket_id": ticket_id}
                        )
                    except Exception as e:
                        logger.error(
                            f"TicketAPI->send mail : Error occured while sending notification : {e}"
                        )
                    return success_200_custom(data=ticket.chat)

                
                
class chatAttachmentAPI(Resource):
    @token_required
    @users_required(users=["student","support", "admin"]) # admin added by Harman
    def get(self,ticket_id="",user_id=""):
        # return "hello"

        if ticket_utils.is_blank(ticket_id) or ticket_utils.is_blank(user_id):
            raise BadRequest(status_msg="User id or ticket id is missing.")
        
        try:
            ticket_attachment = TicketAttachment.query.filter_by(ticket_id=ticket_id).first()
        except Exception as e:
            logger.error(
                f"TicketAPI->get : Error occured while fetching ticket data : {e}"
            )
            raise InternalServerError
        else:
            if ticket_attachment:
                # if user.role == "student":
                    # user = Auth.query.filter_by(user_id=user_id).first()
                    # if user_id == ticket.created_by:
                attachment = get_chat_attachments(ticket_id = ticket_id)
                return success_200_custom(data=attachment)



chat_api.add_resource(chatAPI,'/<string:ticket_id>/<string:user_id>')
chat_api.add_resource(chatAttachmentAPI,'/attachment/<string:ticket_id>/<string:user_id>')
