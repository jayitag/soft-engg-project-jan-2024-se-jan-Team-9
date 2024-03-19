<template>
    <div>
        <div :class="'ticket_card_background_' + status ">
            <div class="ticket_card">
                <b-container fluid="xll">
                    <b-row>
                        <b-col cols="1">
                            <!-- <b-icon icon="check2-all" variant="success" v-show="status == 'resolved'"></b-icon>
                            <b-icon icon="x-circle" variant="danger" v-show="status == 'unresolved'"></b-icon> -->
                        </b-col>
                        <b-col cols="8">
                            <p style="font-weight: 500; font-size:x-large; margin: 0;">{{ title }}</p>
                        </b-col>
                        <b-col cols="3" align-v="center"  style="text-align: end;">
                            <p style="font-size: small;">Created on: {{ formated_created_on }}</p>
                        </b-col>
                    </b-row>
                    <b-row style="margin-top:3px; margin-bottom: 3px;">
                        <b-col cols="1"></b-col>
                        <b-col cols="8"></b-col>
                        <b-col cols="3" align-v="center"  style="text-align: end;">
                            <p style="font-size: small;">Resolved on: {{ formatted_resolved_on }}</p>
                        </b-col>
                    </b-row>
                    <b-row>
                        <b-col><br></b-col>
                    </b-row>
                    <b-row style="margin-top:3px; margin-bottom: 3px;">
                        <b-col cols="1"></b-col>
                        <b-col cols="6">
                            Suggested by: {{ suggested_by_name }}
                        </b-col>
                        <b-col cols="2">
                            <p style="color: blue; font-size: smaller;">Type: {{ type }}</p>
                        </b-col>
                        <b-col cols="3">
                            <p style="color: blue; font-size: xx-small;">Ticekt ID: {{ ticket_id }}</p>
                        </b-col>
                    </b-row>
                    <b-row style="margin-top:3px; margin-bottom: 10px;">
                        <b-col cols="1"></b-col>
                        <b-col cols="8">
                            <b-button variant="outline-primary" @click="showChat()">
                                <b-icon icon="chat"
                                    variant="primary">
                                </b-icon>
                                Discussion  
                            </b-button>
                        </b-col>
                        <b-col cols="3" style="text-align: end;">
                            <b-button variant="outline-danger" @click="removeSuggestion(ticket_id)">
                                Remove 
                            </b-button>
                        </b-col>
                    </b-row>
                </b-container>
            </div>
        </div>
        <ChatWindowAdmin v-if="displayChat" 
            :format_chat="get_formated_ticket" 
            :close_chat="closeChat" 
            :chat="formated_chat" :tick_id="ticket_id">
        </ChatWindowAdmin>
    </div>
</template>

<script>
    import * as common from "../assets/common.js";
    import ChatWindowAdmin from './ChatWindowAdmin.vue';


    export default {
        name: "FAQTicketCard",
        components: { ChatWindowAdmin },
        props: [
            "ticket_id",
            "created_on",
            "title",
            "chat",
            "type",
            "status",
            "suggested_by_name",
        ],
        data() {
            return {
                description: "",
                formated_chat: "",
                displayChat: false,
                formated_created_on :"",
                formatted_resolved_on : "",
            }
        },
        created() {
            this.get_formated_ticket()
        },
        methods: {
            get_formated_ticket() {
                // console.log(this.chat)
                // Your input string
                var inputString = this.chat;

                // console.log(inputString)
                // Parsing the string as JSON
                var jsonArray = JSON.parse(inputString);


                // Function to format timestamp into date and time
                function formatTimestamp(timestamp) {
                    var date = new Date(timestamp * 1000); // Convert timestamp to milliseconds
                    var formattedDate = date.toLocaleDateString(); // Get formatted date
                    //var formattedTime = date.toLocaleTimeString(); // Get formatted time
                    return formattedDate;
                }

                // Loop through jsonArray and format the time property
                for (var i = 0; i < jsonArray.length; i++) {
                    jsonArray[i].date_time = formatTimestamp(jsonArray[i].date_time);
                }

                this.formated_created_on = formatTimestamp(this.created_on);

                // Extracting the chat
                this.description = jsonArray[0].chat;


                this.formated_chat = jsonArray;
                const date_time = jsonArray[jsonArray.length - 1].date_time;
                this.formatted_resolved_on = date_time;

            },
            showChat() {
                this.displayChat = true;
            },
            closeChat() {
                this.displayChat = false;
            },
            // updateResolvedOn(lastDateTime) {
            //     this.formatted_resolved_on = formatTimestamp(lastDateTime);
            //     console.log(lastDateTime);
            // },
            removeSuggestion(ticket_id) {
                // Implement suggest for FAQ functionality
                // You can add the necessary logic here
                fetch(common.TICKET_API + `/${this.ticket_id}` + `/${this.$store.getters.get_user_id}`, {
                    method: "PUT",
                    headers: {
                    "Content-Type": "application/json",
                    web_token: this.$store.getters.get_web_token,
                    user_id: this.$store.getters.get_user_id,
                    },
                    body: JSON.stringify({})
                    //body: JSON.stringify({ is_faq: "False", is_flag: this.is_flag, support_staff_tag_id: this.support_staff_tag_id, status: this.status }), // Include is_flag attribute in request body
                })
                .then((response) => response.json())
                .then((data) => {
                if (data.category == "success") {
                    this.flashMessage.success({
                    message: data.message,
                    });
                    // Update UI or perform any other action upon successful flagging
                    // const isfaq = document.querySelector('.flag-button');
                    // flagButton.style.backgroundColor = 'darkred';
                    console.log("removed an faq suggestion")
                    this.$router.go();

                }
                if (data.category == "error") {
                    this.flashMessage.error({
                    message: data.message,
                    });
                }
                })
                .catch((error) => {
                this.$log.error(`Error : ${error}`);
                this.flashMessage.error({
                    message: "Internal Server Error",
                });
                });
            },
        },
    }
</script>

<style scoped>
.ticket_card {
    min-height: 100px;
    background-color: rgba(250, 246, 246, 0.959);
    margin-left: 10px;
    /* border: 1px solid black; */

    border-left: 0px;
    /* box-shadow: 5px 5px 5px  5px rgb(91, 180, 14); */
    padding: 15px 15px 5px 5px;
}

.ticket_card_background_resolved {
    background-color: rgba(0, 128, 0, 0.524);
    margin-top: 20px;
}

.ticket_card_background_unresolved {
    background-color: rgba(224, 99, 9, 0.599);
    margin-top: 20px;

}
</style>