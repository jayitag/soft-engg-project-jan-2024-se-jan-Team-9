<template>
    <div>

        <div class="ticket_card_background">
            <div class="ticket_card">
                <b-container fluid="xll">
                    <b-row>
                        <b-col cols="12" sm="5" md="1">
                        </b-col>
                        <b-col cols="12" sm="5" md="8">
                            <p style="font-weight: 500; font-size:x-large; margin: 0;">Title: F**K
                            </p>
                            <p style="font-weight: 200; font-size:large; margin: 0;">
                                Description: You are a A@# $%^&* pice Of #$%^&%$%^&^%$#</p>
                        </b-col>
                        <b-col cols="12" sm="5" md="3" align-v="center">
                            <p style="font-size: small;"> created_on: 13/3/2024 5:13:13 am </p>
                        </b-col>

                    </b-row>
                    
                    <b-row style="margin-top:10px">
                        <b-col cols="12" sm="5" md="1">
                        </b-col>
                        <b-col cols="12" sm="5" md="9">
                            <form name="optionsForm">
                                <input type="radio" name="option" value="Misbehavior">Misbehavior
                                <input type="radio" name="option" value="Irrelevant" style="margin-left: 20px;">Irrelevant
                            </form>
                        </b-col>
                        
                    </b-row>
                    <b-row style="margin-top:10px ;">
                        <b-col cols="12" sm="5" md="1">
                        </b-col>
                        <b-col cols="12" sm="5" md="9">
                            <b-button variant="outline-primary" @click="commit"> 
                                &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Commit &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; </b-button> </b-col>
                        <!-- <b-col cols="12" sm="5" md="2">
                            <p style="color: blue; font-size: smaller;">Ticekt ID: {{ ticket_id }}</p>
                        </b-col> -->

                    </b-row>
                    <b-row style="margin: 0;">
                        <b-col cols="12" sm="5" md="9">
                        
                        </b-col>
                        <b-col cols="12" sm="5" md="3">
                            <p style="color: blue; font-size: xx-small;">Ticekt ID:  f20d39020cacdeda80f81797c7c6a01a</p>
                        </b-col>
                    </b-row>

                </b-container>
            </div>
        </div>


        <!-- <ChatWindow v-if="displayChat" :format_chat="get_formated_ticket" :close_chat="closeChat" :chat="formated_chat" :tick_id="ticket_id" :ticket_title="title"></ChatWindow> -->
    </div>
</template>

<script>



export default {
    name: "FlagTicketCard",
    components: { },
    props: [
        // "ticket_id",
        // "created_on",
        // "title",
        // "chat",
        // "type",
        // "status",
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
    },
    methods: {
        commit(){
            const selectedOption = this.$el.querySelector('input[name="option"]:checked');
            if (selectedOption) {
                console.log("Selected option:", selectedOption.value);
            }
            // submit the ticket form  with the input value and ticket id 
        }
    }
}
</script>

<style scoped>
.ticket_card {
    min-height: 100px;
    background-color: rgba(255, 0, 0, 0.129);
    margin-left: 10px;
    /* border: 1px solid black; */

    border-left: 0px;
    /* box-shadow: 5px 5px 5px  5px rgb(91, 180, 14); */
    padding: 15px 15px 0px 15px;
    /* background-color: rgb(255 6 6 / 23%); */
    margin-top: 20px;
    width: 68vw;
    border-left: solid rgb(185, 0, 0) 7px;
    box-sizing: border-box;
}
input[type="radio"] {
        margin-right: 5px;
    }


</style>