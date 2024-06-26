# Online Support Ticket Application
# Tushar Supe : 21f1003637
# Vaidehi Agarwal: 21f1003880
# File Info: This is Ticket Blueprint file.

# --------------------  Imports  --------------------

import hashlib
import time
from flask import Blueprint, request
from flask_restful import Api, Resource
from application.logger import logger
from application.common_utils import (
    token_required,
    users_required,
    convert_base64_to_img,
    convert_img_to_base64,
    is_img_path_valid,
    is_base64,
    get_encoded_file_details,
)
from application.views.user_utils import UserUtils
from application.discourse_integration.post_public_ticket_on_discourse import post_public_ticket_on_discourse
from application.responses import *
from application.models import *
from copy import deepcopy
from application.globals import *
from application.notifications import send_email

# --------------------  Code  --------------------


class TicketUtils(UserUtils):
    def __init__(self, user_id=None):
        self.user_id = user_id

    def convert_ticket_to_dict(self, ticket):
        ticket_dict = vars(ticket)  # verify if this properly converts obj to dict
        if "_sa_instance_state" in ticket_dict:
            del ticket_dict["_sa_instance_state"]
        attachments = self.get_ticket_attachments(ticket_id=ticket.ticket_id)
        ticket_dict["attachments"] = attachments
        return ticket_dict

    def get_ticket_attachments(self, ticket_id):
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

    def generate_ticket_id(self, title: str, user_id: str) -> str:
        """
        Ticket id is generated from ticket title and user id and timestamp
        """
        # generate unique id
        ts = str(int(time.time_ns()))
        string = f"{user_id}_{title}_{ts}"
        ticket_id = hashlib.md5(string.encode()).hexdigest()
        return ticket_id

    def save_ticket_attachments(
        self, attachments: list, ticket_id: str, user_id: str, operation: str
    ):
        # get list of files from db for the ticket and user
        # if file already exists then add number extension
        # file name is not saved , only number extension required
        # currently there is no option to delete attachment
        # file name: {ticket_id}_{user_id}_{number-extension-if-needed}_.{file_format}
        # operation : create_ticket , update_ticket only student can do | resolve_ticket only support can do.

        total_attachments = len(attachments)
        num_successful_attachments = 0

        if total_attachments == 0:
            return (False, "Attachments are empty.")

        files = [
            file
            for file in os.listdir(TICKET_ATTACHMENTS_PATH)
            if file.startswith(f"{ticket_id}_{user_id}")
        ]
        number_extension = len(files)  # starting point

        for attach in attachments:
            # attach will be of format {attachment_loc:'', user_id:''}
            # attachment_loc will contain base64 version of image while data transfer is occuring between backend and frontend
            # attachment_loc will contain image path when data is retried from db by backend
            # attachment_loc will contain base64 image when creating new attachment

            if attach["attachment_loc"]:
                if is_base64(attach["attachment_loc"].split(",")[1]):
                    file_type, file_format, encoded_data = get_encoded_file_details(
                        attach["attachment_loc"]
                    )
                    if (file_type == "image") and (
                        file_format in ACCEPTED_IMAGE_EXTENSIONS
                    ):
                        file_name = (
                            f"{ticket_id}_{user_id}_{number_extension}.{file_format}"
                        )
                        file_path = os.path.join(TICKET_ATTACHMENTS_PATH, file_name)
                        if convert_base64_to_img(file_path, encoded_data):
                            # successfully image saved and now add entry to database
                            try:
                                # while creating a ticket a student can upload multiple attachments
                                # verify whether each attachment is unique
                                attach["ticket_id"] = ticket_id
                                attach["attachment_loc"] = file_path
                                ticket_attach = TicketAttachment(**attach)
                                db.session.add(ticket_attach)
                                db.session.commit()
                                num_successful_attachments += 1
                                number_extension += 1
                            except Exception as e:
                                logger.error(
                                    f"TicketAPI->post : Error occured while creating a Ticket Attachment : {e}"
                                )
        return (
            True,
            f"Total {num_successful_attachments} / {total_attachments} attchements are valid and added successfully.",
        )

    def tickets_filter_by_query(self, all_tickets, query=""):
        # match tickets with query
        filtered_tickets = []
        if query:
            for ticket in all_tickets:
                search_in = (
                    f"{ticket['title']} {ticket['description']} {ticket['solution']}"
                )
                for q in query.split(" "):
                    if q.lower() in search_in.lower():
                        filtered_tickets.append(ticket)
                        break

            return filtered_tickets
        else:
            filtered_tickets = deepcopy(all_tickets)

            return filtered_tickets

    def tickets_filter_by_tags(self, all_tickets, tags=[]):
        # filter by tags (if present)
        filtered_tickets = []
        if tags:
            for ticket in all_tickets:
                ticket_tags = [ticket["tag_1"], ticket["tag_2"], ticket["tag_3"]]
                if set(ticket_tags).intersection(set(tags)):
                    filtered_tickets.append(ticket)

            return filtered_tickets
        else:
            filtered_tickets = deepcopy(all_tickets)

            return filtered_tickets

    def tickets_filter_by_status(self, all_tickets, status=[]):
        # filter by status (if present)
        filtered_tickets = []
        if status:
            for ticket in all_tickets:
                if ticket["status"] in status:
                    filtered_tickets.append(ticket)

            return filtered_tickets
        else:
            filtered_tickets = deepcopy(all_tickets)

            return filtered_tickets

    def tickets_filter_by_priority(self, all_tickets, priority=[]):
        # filter by priority (if present)
        filtered_tickets = []
        if priority:
            for ticket in all_tickets:
                if ticket["priority"] in priority:
                    filtered_tickets.append(ticket)

            return filtered_tickets
        else:
            filtered_tickets = deepcopy(all_tickets)

            return filtered_tickets

    def tickets_sort(self, all_tickets, sortby="", sortdir=""):
        # sort (if present)
        if sortby:
            # sortby should be 'created_on', 'resolved_on', 'votes'
            if sortby not in ["created_on", "resolved_on", "votes"]:
                sortby = "created_on"
        else:
            sortby = "created_on"
        if sortdir:
            # sortdir should be 'asc' or 'desc'
            sortdir = True if sortdir == "desc" else False
        else:
            sortdir = True
        all_tickets = sorted(all_tickets, key=lambda d: d[sortby], reverse=sortdir)
        return all_tickets

    def tickets_filter_sort(self, all_tickets, args):
        # match tickets with query
        all_tickets = self.tickets_filter_by_query(all_tickets, args["query"])

        # filter by tags (if present)
        all_tickets = self.tickets_filter_by_tags(all_tickets, args["tags"])

        # filter by status (if present)
        all_tickets = self.tickets_filter_by_status(all_tickets, args["status"])
        all_tickets = self.tickets_filter_by_status(all_tickets, args["type"])


        # filter by priority (if present)
        all_tickets = self.tickets_filter_by_priority(all_tickets, args["priority"])

        # sort (if present)
        all_tickets = self.tickets_sort(all_tickets, args["sortby"], args["sortdir"])

        return all_tickets

    def get_args_from_query(self, args):
        def convert_arg_to_list(arg: str):
            # for internal use only
            arg = args.get(arg, "")
            if arg == "":
                return []
            else:
                return arg.split(",")

        _args = {}
        _args["query"] = args.get("query", "")
        _args["sortby"] = args.get("sortby", "")
        _args["sortdir"] = args.get("sortdir", "")
        _args["status"] = convert_arg_to_list("filter_status")
        _args["type"] = convert_arg_to_list("filter_type")

        _args["priority"] = convert_arg_to_list("filter_priority")
        _args["tags"] = convert_arg_to_list("filter_tags")

        return _args


ticket_bp = Blueprint("ticket_bp", __name__)
ticket_api = Api(ticket_bp)
ticket_utils = TicketUtils()


class TicketAPI(Resource):
    @token_required
    @users_required(users=["student", "support", "admin"])
    def get(self, ticket_id="", user_id=""):
        """
        Usage
        -----
        Get a single ticket for the user and return

        Parameters
        ----------
        ticket is and user id

        Returns
        -------
        Ticket

        """

        if ticket_utils.is_blank(ticket_id) or ticket_utils.is_blank(user_id):
            raise BadRequest(status_msg="User id or ticket id is missing.")

        # check if ticket exists and it is created by user_id
        try:
            ticket = Ticket.query.filter_by(ticket_id=ticket_id).first()
        except Exception as e:
            logger.error(
                f"TicketAPI->get : Error occured while fetching ticket data : {e}"
            )
            raise InternalServerError
        else:
            if ticket:
                user = Auth.query.filter_by(user_id=user_id).first()
                if user_id == ticket.created_by or user.role == "support":
                    # the ticket and its user are matched or its a support staff
                    # convert to list of dict
                    ticket_dict = ticket_utils.convert_ticket_to_dict(ticket)
                    return success_200_custom(data=ticket_dict)
            else:
                raise NotFoundError(status_msg="Ticket does not exists")

    @token_required
    @users_required(users=["student"])
    def post(self, user_id=""):
        """
        Usage
        -----
        Create a new ticket. Only a student can create.

        Parameters
        ----------
        form data sent with request

        Returns
        -------

        """
        details = {
            "title": "",
            "chat": "",
            "type": "",
            "support_staff_tag_id": "",
            "catagory": "",
        }

        # check user_id
        if ticket_utils.is_blank(user_id):
            raise BadRequest(status_msg="User id is empty/missing in url")

        try:
            user = Auth.query.filter_by(user_id=user_id).first()
            if not user:
                # user id does not exists
                raise NotFoundError(status_msg="User id does not exists.")
        except Exception as e:
            logger.error(
                f"TicketAPI->post : Error occured while getting form data : {e}"
            )
            raise InternalServerError

        # get form data
        try:
            form = request.get_json()
            attachments = form.get("attachments", [])
            is_attachment = False
            if attachments:
                is_attachment = True
            for key in details:
                value = form.get(key, "")
                if ticket_utils.is_blank(value):
                    value = ""
                details[key] = value
        except Exception as e:
            logger.error(
                f"TicketAPI->post : Error occured while getting form data : {e}"
            )
            raise InternalServerError
        else:
            if details["title"] == "" or details["type"] == "":
                raise BadRequest(
                    status_msg=f"Ticket title and at type is required"
                )

            ticket_id = ticket_utils.generate_ticket_id(details["title"], user_id)
            if details["type"] == "public":
                result = post_public_ticket_on_discourse(Discourse_Username = user.discourse_username,
                                                public_ticket_title = details["title"],
                                                public_ticket_content = details["chat"],
                                                public_ticket_category = details["catagory"]
                                                )
                if result == "failed":
                    pass
                else:
                    details["discourse_public_ticket_url"] = result
            details["chat"] = "[" + "{" + "\"name\":\"" + user.first_name + " " + user.last_name + "\"," + "\"role\":\"" + user.role + "\"," + "\"chat\":\"" + details["chat"] + "\"," + "\"date_time\":\"" + str(time.time()) + "\"," + "\"is_attachment\":\"" + str(is_attachment) + "\"}"+ "]"
            details["ticket_id"] = ticket_id
            details["created_by"] = user_id
            details["created_on"] = int(time.time())
            ticket = Ticket(**details)

            db.session.add(ticket)
            db.session.commit()
                
            try:
                    ticket_created = Ticket.query.filter_by(ticket_id = ticket_id).first()
                    resp = send_email(
                        occasion= "ticket_creation",
                        to=[{"email": user.email, "username": user.first_name}],
                        _from= "admin@gmail.com",
                        subject="Your ticket was succefully created",
                        data={ "username": user.first_name, "ticket_id": ticket_id, "type": ticket_created.type, "ticket_category": ticket_created.catagory, "discourse_url": ticket_created.discourse_public_ticket_url}
                        )
            except Exception as e:
                    logger.error(
                        f"TicketAPI->post : Error occured while sending  new ticket mail : {e}"
                    )
                    raise InternalServerError(
                        status_msg="Error occured while sending new ticket creation mail"
                    )
            logger.info("Ticket created successfully.")

            # add attachments now
            status, message = ticket_utils.save_ticket_attachments(
                            attachments, ticket_id, user_id, operation="create_ticket"
                            )
            raise Success_200(status_msg=f"Ticket created successfully. {message}")

    @token_required
    @users_required(users=["student", "support", "admin"]) #edited by Harman - added admin
    def put(self, ticket_id="", user_id=""):
        """
        Usage
        -----
        Update a ticket.
        only student and support has access, role is checked later in code.
        Student who created a ticket can update : title, description, attachments, tags, priority
        Student who did not create : can vote a ticket
        Support can update : solution and attachment, status

        Parameters
        ----------
        form data sent with request

        Returns
        -------

        """
        # edited by yukti
        details = {
            
            "title": "",
            "description": "",
           "is_flag":"",
           "is_faq":"",
           "suggested_by_id": "", #by Harman
           "support_staff_tag_id":"",
           "type":"",
           "created_by":"",
           "created_on":0,
           "category":"",
            "status": "",
            "chat": "",

        }

        # check url data
        if ticket_utils.is_blank(ticket_id) or ticket_utils.is_blank(user_id):
            raise BadRequest(status_msg="User id or ticket id is missing.")

        # check form data
        try:
            form = request.get_json()
            attachments = form.get("attachments", [])
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

        # check if ticket exists and it is created by user_id
        try:
            ticket = Ticket.query.filter_by(ticket_id=ticket_id).first()
            ticket_attachment = TicketAttachment.query.filter_by(
                ticket_id=ticket_id
            ).all()
            user = Auth.query.filter_by(user_id=user_id).first()
        except Exception as e:
            logger.error(
                f"TicketAPI->get : Error occured while fetching user and ticket data : {e}"
            )
            raise InternalServerError
        else:
            if not ticket:
                raise NotFoundError(status_msg="Ticket does not exists")
            if not user:
                raise NotFoundError(status_msg="User does not exists")

            # if ticket.status == "resolved":
            #     raise BadRequest(status_msg=f"Resolved tickets can't be edited.")  # edited by yukti- need an edit on resolved tickets in order to change their is_faq attribute.

            role = user.role

            if role == "support" or (
                role == "student" and user_id == ticket.created_by
            ):
                # add attachments now
                status, message = ticket_utils.save_ticket_attachments(
                    attachments, ticket_id, user_id, operation="update_ticket"
                )

            if role == "student":
                if user_id == ticket.created_by:
                    # student is creator of the ticket
                    if details["title"] == "" or details["tag_1"] == "":
                        raise BadRequest(
                            status_msg=f"Ticket title and at least one tag is required"
                        )

                    ticket.title = details["title"]
                    ticket.description = details["description"]
                    ticket.tag_1 = details["tag_1"]
                    ticket.tag_2 = details["tag_2"]
                    ticket.tag_3 = details["tag_3"]
                    ticket.priority = details["priority"]

                    db.session.add(ticket)
                    db.session.commit()

                    raise Success_200(status_msg="Successfully updated a ticket.")

                else:
                    # student has not created this ticket, so only vote can be done
                    ticket_vote = TicketVote.query.filter_by(
                        ticket_id=ticket_id, user_id=user_id
                    ).first()
                    if ticket_vote:
                        # student has already voted
                        raise AlreadyExistError(
                            status_msg="You have already voted this ticket."
                        )
                    else:
                        # ticket upvoted
                        ticket_vote = TicketVote(ticket_id=ticket_id, user_id=user_id)
                        db.session.add(ticket_vote)

                        ticket.votes = ticket.votes + 1
                        db.session.add(ticket)

                        db.session.commit()
                        raise Success_200(status_msg="Successfully upvoted ticket.")

            if role == "support": # edited by yukti
                # sol = details["solution"]
                # if ticket_utils.is_blank(sol):
                    # raise BadRequest(status_msg="Solution can not be empty")
                is_flag=details["is_flag"]
                status=details["status"]
                support_staff_tag_id=details["support_staff_tag_id"]
                is_faq=details["is_faq"]
                if ticket_utils.is_blank(is_flag):
                    raise BadRequest(status_msg="Flag can not be empty")
                else:
                    ticket.is_flag = is_flag
                    ticket.is_faq=is_faq
                    ## by Harman
                    if details["suggested_by_id"]:
                        suggested_by_id = details["suggested_by_id"]
                        user = Auth.query.filter_by(user_id=suggested_by_id).first()
                        ticket.suggested_by_name = user.first_name
                    ############
                    ticket.support_staff_tag_id=support_staff_tag_id
                    ticket.status=status
                    # ticket.status = "resolved"
                    # ticket.support_staff_tag_id = user_id  # Edited by yukti - replaced resolved_by with support_staff_tag_id attribute of Ticket.
                    # ticket.resolved_on = int(time.time())

                    # db.session.add(ticket)
                    db.session.commit()

                    # send notification to user who created as well as voted
                    # try:
                    #     _from = user.email
                    #     ticket_votes = TicketVote.query.filter_by(
                    #         ticket_id=ticket_id
                    #     ).all()
                    #     users_voted = [
                    #         ticket_vote.user_id for ticket_vote in ticket_votes
                    #     ]
                    #     users_voted.append(ticket.created_by)
                    #     users_email_name = []
                    #     for user_id_ in users_voted:
                    #         user_ = Auth.query.filter_by(user_id=user_id_).first()
                    #         users_email_name.append(
                    #             {
                    #                 "email": user_.email,
                    #                 "first_name": user_.first_name,
                    #                 "ticket_id": ticket_id,
                    #             }
                    #         )

                    #     resp = send_email(
                    #         to=users_email_name,
                    #         _from=_from,
                    #         sub="Your ticket is resolved",
                    #     )
                    # except Exception as e:
                    #     logger.error(
                    #         f"TicketAPI->send mail : Error occured while sending notification : {e}"
                    #     )

                    raise Success_200(status_msg="Successfully resolved a ticket.")

            if role == "admin": #by Harman
                ticket = Ticket.query.filter_by(ticket_id=ticket_id).first()
                ticket.is_faq = "False"
                db.session.commit()
                raise Success_200(status_msg="Suggestion deleted successfully")
                
                # try:
                # except Exception as e:
                #     print("I am here")
                #     raise InternalServerError
                
                # admin dont have access
                # raise Unauthenticated(
                #     status_msg="Admin don't have access to this endpoint."
                # )

    @token_required
    @users_required(users=["student"])
    def delete(self, ticket_id="", user_id=""):
        """
        Usage
        -----
        Delete a single ticket. Only a student who created  a ticket can delete

        Parameters
        ----------
        ticket is and user id

        Returns
        -------


        """
        if ticket_utils.is_blank(ticket_id) or ticket_utils.is_blank(user_id):
            raise BadRequest(status_msg="User id or ticket id is missing.")

        # check if ticket exists and it is created by user_id
        try:
            ticket = Ticket.query.filter_by(ticket_id=ticket_id).first()
        except Exception as e:
            logger.error(
                f"TicketAPI->delete : Error occured while fetching ticket data : {e}"
            )
            raise InternalServerError
        else:
            if ticket:
                user = Auth.query.filter_by(user_id=user_id).first()
                if user_id == ticket.created_by:
                    # the ticket and its user are matched

                    # delete ticket votes
                    ticket_votes = TicketVote.query.filter_by(ticket_id=ticket_id).all()
                    for ticket_vote in ticket_votes:
                        db.session.delete(ticket_vote)
                    db.session.commit()

                    # delete ticket attachments
                    ticket_attachments = TicketAttachment.query.filter_by(
                        ticket_id=ticket_id
                    ).all()
                    for ticket_attachment in ticket_attachments:
                        db.session.delete(ticket_attachment)
                    db.session.commit()

                    # delete ticket
                    db.session.delete(ticket)
                    db.session.commit()
                    raise Success_200(status_msg="Ticket deleted successfully")
                else:
                    raise PermissionDenied(
                        status_msg="Only a user who created a ticket can delete it."
                    )
            else:
                raise NotFoundError(status_msg="Ticket does not exists")


class AllTicketsAPI(Resource):
    @token_required
    @users_required(users=["student", "support", "admin"])
    def get(self):
        """
        Usage
        -----
        Get all tickets based on query and user role.
        Sorting and filtering will be applied as per query.
        Student needs all tickets while searching and needs all their tickets (created and upvoted)
        Support needs pending tickets while resolving and needs all their resolved tickets
        Admin needs resolved tickets while creating FAQ

        Parameters
        ----------
        query

        Returns
        -------
        List of tickets
        """

        # user is student and is searching tickets while creating a new ticket.
        # get query arguments
        try:
            # args = request.args.to_dict(flat=True)
            # args = ticket_utils.get_args_from_query(args)
            user_id = request.headers.get("user_id", "")
        except Exception as e:
            logger.error(f"AllTickets->get : Error occured while resolving query : {e}")
            raise InternalServerError
        user = Auth.query.filter_by(
            user_id=user_id
        ).first()  # user already exists as user_required verified it

        # verify is user is student
        if user.role != "student":
            raise PermissionDenied(
                status_msg="Only student can search all tickets using query."
            )

        all_tickets = []

        # get all tickets
        tickets = Ticket.query.all()
        for ticket in tickets:
            tick = ticket_utils.convert_ticket_to_dict(ticket)
            all_tickets.append(tick)

        # all_tickets = ticket_utils.tickets_filter_sort(all_tickets, args)

        logger.info(f"All tickets found : {len(all_tickets)}")

        return success_200_custom(data=all_tickets)

# Added by yukti -  support staff fetch api for all the tickets both resolved and unresolved.
########
# class AllSupportTicketsAPI(Resource):
#     @token_required
#     @users_required(users=["support"])
#     def get(self, user_id=""):
#         if ticket_utils.is_blank(user_id):
#             raise BadRequest(status_msg="User id is missing.")

#         user = Auth.query.filter_by(user_id=user_id).first()

#         resolved_tickets = Ticket.query.filter_by( type="private",status="resolved", is_flag="False").all()
#         unresolved_tickets = Ticket.query.filter_by(type="private",status="unresolved", is_flag="False").all()
#         print(resolved_tickets)
#         print(unresolved_tickets)
#         resolved_tickets = [ticket_utils.convert_ticket_to_dict(ticket) for ticket in resolved_tickets]
#         unresolved_tickets = [ticket_utils.convert_ticket_to_dict(ticket) for ticket in unresolved_tickets]

#         logger.info(f"Resolved tickets found : {len(resolved_tickets)}")
#         logger.info(f"Unresolved tickets found : {len(unresolved_tickets)}")

#         return success_200_custom(data={"resolved_tickets": resolved_tickets, "unresolved_tickets": unresolved_tickets})
# from flask import jsonify
# class SupportStaffFlagAPI(Resource):
#     @token_required
#     @users_required(users=["support"])
#     def put(self, user_id="", ticket_id=""):
#         if ticket_utils.is_blank(ticket_id) or ticket_utils.is_blank(user_id):
#             raise BadRequest(status_msg="User id or ticket id is missing.")
#         print(ticket_id)
#         print(user_id)

#         user = Auth.query.filter_by(user_id=user_id).first()
#         ticket = Ticket.query.filter_by(ticket_id=ticket_id).first()
#         if not ticket:
#             return {'message': 'Ticket not found'}, 404
#         ticket.is_flag = True
#         db.session.commit()
#         logger.info(f"Flagged this ticket : {ticket_id}")
#         print("successfully flagged.")
#         raise Success_200(status_msg="Successfully flagged ticket.")
    
###########
class AllTicketsUserAPI(Resource):
    @token_required
    @users_required(users=["student", "support", "admin"])
    def get(self, user_id=""):
        # tickets retrieved based on user role.

        if ticket_utils.is_blank(user_id):
            raise BadRequest(status_msg="User id is missing.")

        # get query arguments
        try:
            args = request.args.to_dict(flat=True)

            args = ticket_utils.get_args_from_query(args)
        except Exception as e:
            logger.error(f"AllTickets->get : Error occured while resolving query : {e}")
            raise InternalServerError
        user = Auth.query.filter_by(
            user_id=user_id
        ).first()  # user already exists as user_required verified it

        all_tickets = []

        # verify user role
        role = user.role

        if role == "student":
            # student : all tickets created or upvoted by him/her
            # status, priority, sort, filter will be as per filter options received
            # upvoted ticket can be checked by comparing created_by with user_id
            user_tickets = Ticket.query.filter_by(created_by=user.user_id).all()
            for ticket in user_tickets:
                # tick = ticket_utils.convert_ticket_to_dict(ticket)
                # all_tickets.append(tick)
                all_tickets = [ticket_utils.convert_ticket_to_dict(ticket) for ticket in user_tickets]
                return success_200_custom(data={"all_tickets": all_tickets})

        if role == "support":
            # support : all tickets resolvedby him/her
            # get all pending tickets
            # status, priority, sort, filter will be as per filter options received

            # if "resolved" in args["status"]:
            #     # get all tickets resolved by the support staff
            #     user_tickets = Ticket.query.filter_by(support_staff_tag_id=user.user_id).all() # Edited by yukti - replaced resolved_by with support_staff_tag_id attribute of Ticket.
            # elif "pending" in args["status"]:
            #     # get all pending tickets
            #     user_tickets = Ticket.query.filter_by(status="pending").all()
            # else:
            #     user_tickets = []
            # for ticket in user_tickets:
            #     tick = ticket_utils.convert_ticket_to_dict(ticket)
            #     all_tickets.append(tick)
            if ticket_utils.is_blank(user_id):  ## Edited by yukti
                raise BadRequest(status_msg="User id is missing.")

            user = Auth.query.filter_by(user_id=user_id).first()

            resolved_tickets = Ticket.query.filter_by( type="private",status="resolved", is_flag="False").all()
            unresolved_tickets = Ticket.query.filter_by(type="private",status="unresolved", is_flag="False").all()
            print(resolved_tickets)
            print(unresolved_tickets)
            resolved_tickets = [ticket_utils.convert_ticket_to_dict(ticket) for ticket in resolved_tickets]
            unresolved_tickets = [ticket_utils.convert_ticket_to_dict(ticket) for ticket in unresolved_tickets]

            logger.info(f"Resolved tickets found : {len(resolved_tickets)}")
            logger.info(f"Unresolved tickets found : {len(unresolved_tickets)}")
            print("unresolved_tickets", unresolved_tickets)
            print("resolved_tickets", resolved_tickets)

            return success_200_custom(data={"resolved_tickets": resolved_tickets, "unresolved_tickets": unresolved_tickets})

        if role == "admin":
            # admin : get all tickets resolved globally (for creating faq)
            # status, priority, sort, filter will be as per filter options received
            user_tickets = Ticket.query.filter_by(status="resolved").all()
            for ticket in user_tickets:
                tick = ticket_utils.convert_ticket_to_dict(ticket)
                all_tickets.append(tick)

        all_tickets = ticket_utils.tickets_filter_sort(all_tickets, args)
        logger.info(f"All tickets found : {len(all_tickets)}")

        return success_200_custom(data=all_tickets)
    

##### by Harman; for FAQ marked tickets to Admin
class AllTicketsAdminAPI(Resource):
    @token_required
    @users_required(users=["admin"])
    def get(self, user_id=""):
        # tickets retrieved based on user role.

        if ticket_utils.is_blank(user_id):
            raise BadRequest(status_msg="User id is missing.")

        # get query arguments
        try:
            args = request.args.to_dict(flat=True)

            args = ticket_utils.get_args_from_query(args)
        except Exception as e:
            logger.error(f"AllTickets->get : Error occured while resolving query : {e}")
            raise InternalServerError
        user = Auth.query.filter_by(
            user_id=user_id
        ).first()  # user already exists as user_required verified it

        all_tickets = []

        # verify user role
        role = user.role

        if role == "admin":
            # admin : get all tickets resolved globally (for creating faq)
            # status, priority, sort, filter will be as per filter options received
            faq_tickets = Ticket.query.filter_by(is_faq="True").all()
            for ticket in faq_tickets:
                tick = ticket_utils.convert_ticket_to_dict(ticket)
                all_tickets.append(tick)

        all_tickets = ticket_utils.tickets_filter_sort(all_tickets, args)
        logger.info(f"All tickets found : {len(all_tickets)}")

        return success_200_custom(data=all_tickets)
    
    @token_required
    @users_required(users=["admin"])
    def put(self, ticket_id="", user_id=""):

        """
        Usage
        -----
        For admin to remove the ticket showing as suggestion 
        by changing the value of flag is_faq FALSE
        """

        try:
            ticket = Ticket.query.filter_by(ticket_id=ticket_id).first()
            ticket.is_faq = False
            db.session.commit()
            raise Success_200(status_msg="Suggestion deleted successfully")
        except Exception as e:
            raise InternalServerError
        

#####
    
ticket_api.add_resource(
    TicketAPI,
    "/<string:ticket_id>/<string:user_id>",
    "/<string:user_id>",
)  # path is /api/v1/ticket
ticket_api.add_resource(AllTicketsAPI, "/all-tickets")
ticket_api.add_resource(AllTicketsUserAPI, "/all-tickets/<string:user_id>")
ticket_api.add_resource(AllTicketsAdminAPI, "/all-faq-tickets/<string:user_id>",
                                            "/all-faq-tickets/<string:ticket_id>/<string:user_id>") #Harman
# ticket_api.add_resource(AllSupportTicketsAPI, "/all-support-tickets/<string:user_id>")
# ticket_api.add_resource(SupportStaffFlagAPI, "/support-staff-flag-api/<string:user_id>/<string:ticket_id>")


# --------------------  END  --------------------
