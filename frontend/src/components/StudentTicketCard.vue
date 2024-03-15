<template>
    <div>

        <div :class="'ticket_card_background_' + status ">
            <div class="ticket_card">
                <b-container fluid="xll">
                    <b-row>
                        <b-col cols="12" sm="5" md="1">
                            <b-icon icon="check2-all" variant="success" v-show="status == 'resolved'"></b-icon>
                            <b-icon icon="x-circle" variant="Danger" v-show="status == 'unresolved'"></b-icon>
                        </b-col>
                        <b-col cols="12" sm="5" md="8">
                            <p style="font-weight: 500; font-size:x-large; margin: 0;">Title: {{ title }}
                            </p>
                            <p style="font-weight: 200; font-size:large; margin: 0;">
                                Description:{{ description }}</p>
                        </b-col>
                        <b-col cols="12" sm="5" md="3" align-v="center">
                            <p style="font-size: small;"> created_on: {{ formated_created_on }} </p>
                        </b-col>

                    </b-row>
                    <b-row style="margin-top:30px ;">
                        <b-col cols="12" sm="5" md="1">
                        </b-col>
                        <b-col cols="12" sm="5" md="9">
                            <b-button variant="outline-primary" @click="showChat()"> <b-icon icon="chat"
                                    variant="primary"></b-icon>
                                Comment</b-button> </b-col>
                                <b-col cols="12" sm="5" md="2">
                            <p style="color: blue; font-size: smaller;">Type: {{ type }}</p>
                            <!-- <p style="color: blue; font-size: xx-small;">Ticekt ID: {{ ticket_id }}</p> -->
                        </b-col>
                        <!-- <b-col cols="12" sm="5" md="2">
                            <p style="color: blue; font-size: smaller;">Ticekt ID: {{ ticket_id }}</p>
                        </b-col> -->

                    </b-row>
                    <b-row style="margin: 0;">
                        <b-col cols="12" sm="5" md="9">

                        </b-col>
                        <b-col cols="12" sm="5" md="3">
                            <p style="color: blue; font-size: xx-small;">Ticekt ID: {{ ticket_id }}</p>
                        </b-col>
                    </b-row>

                </b-container>
            </div>
        </div>


        <ChatWindow v-if="displayChat" :format_chat="get_formated_ticket" :close_chat="closeChat" :chat="formated_chat" :tick_id="ticket_id"></ChatWindow>
    </div>
</template>

<script>

import ChatWindow from './ChatWindow.vue';


export default {
    name: "StudentTicketCard",
    components: { ChatWindow },
    props: [
        "ticket_id",
        "created_on",
        "title",
        "chat",
        "type",
        "status",
    ],
    data() {
        return {
            description: "",
            formated_chat: "",
            displayChat: false,
            formated_created_on :"",
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
                var formattedTime = date.toLocaleTimeString(); // Get formatted time
                return formattedDate + ' ' + formattedTime;
            }

            // Loop through jsonArray and format the time property
            for (var i = 0; i < jsonArray.length; i++) {
                jsonArray[i].date_time = formatTimestamp(jsonArray[i].date_time);
            }

            this.formated_created_on = formatTimestamp(this.created_on)

            // Extracting the chat
            this.description = jsonArray[0].chat;


            this.formated_chat = jsonArray

        },
        showChat() {
            this.displayChat = true;
        },
        closeChat() {
            this.displayChat = false;
        }
    }
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
    padding: 15px 15px 0px 15px;
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