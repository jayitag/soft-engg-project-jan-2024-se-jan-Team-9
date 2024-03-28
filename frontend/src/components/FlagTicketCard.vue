<template>
    <div>

        <div class="ticket_card_background" v-if="show">
            <div class="ticket_card">
                <b-container fluid="xll">
                    <b-row>
                        <b-col cols="12" sm="5" md="1">
                        </b-col>
                        <b-col cols="12" sm="5" md="8">
                            <p style="font-weight: 500; font-size:x-large; margin: 0;">Title: {{ title }}
                            </p>
                            <p style="font-weight: 200; font-size:large; margin: 0;">
                                Description: {{ chat }} </p>
                        </b-col>
                        <b-col cols="12" sm="5" md="3" align-v="center" class="date_x_container">
                            <b-icon icon="x-square" variant="danger" font-scale="1" class="close_x" @click="cancel"></b-icon>
                            <p style="font-size: small;"> created_on: {{ created_on }} </p>
                            
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
                            <p style="color: blue; font-size: xx-small;">Ticekt ID:  {{ ticket_id }}</p>
                        </b-col>
                    </b-row>

                </b-container>
            </div>
        </div>


        <!-- <ChatWindow v-if="displayChat" :format_chat="get_formated_ticket" :close_chat="closeChat" :chat="formated_chat" :tick_id="ticket_id" :ticket_title="title"></ChatWindow> -->
    </div>
</template>

<script>
import * as common from "../assets/common.js";


export default {
    name: "FlagTicketCard",
    components: { },
    props: [
        "ticket_id",
        "created_on",
        "title",
        "chat",
    ],
    data() {
        return {
           show:true 
        }
    },
    created() {},
    methods: {
        commit(){
            const selectedOption = this.$el.querySelector('input[name="option"]:checked');
            if (selectedOption) {
                const payload = {
                                    flag_type: selectedOption.value,  
                                    is_flag: "False",
                                };
                fetch(common.ADMIN_API + `/flag/` + this.ticket_id, {
                                                                        method: "PUT",
                                                                        headers: {
                                                                                    "Content-Type": "application/json",
                                                                                    web_token: this.$store.getters.get_web_token,
                                                                                    user_id: this.user_id,
                                                                                },
                                                                        body: JSON.stringify(payload),
                                                                    })
                                                                        .then((response) => response.json())
                                                                        .then((data) => {
                                                                                            {
                                                                                            // console.log(data)
                                                                                            this.ticketData = data.flagdata
                                                                                            console.log(this.ticketData)
                                                                                            this.show = false
                                                                                            }
                                                                                        })
            }
            
        },

        cancel(){
                    const payload = {
                                         flag_type: "none",  
                                         is_flag: "False",
                                     };
                    fetch(common.ADMIN_API + `/flag/` + this.ticket_id, {
                                                    method: "PUT",
                                                    headers: {
                                                                "Content-Type": "application/json",
                                                                web_token: this.$store.getters.get_web_token,
                                                                user_id: this.user_id,
                                                            },
                                                    body: JSON.stringify(payload),
                                                })
                                                    .then((response) => response.json())
                                                    .then((data) => {
                                                                        {
                                                                        // console.log(data)
                                                                        this.ticketData = data.flagdata
                                                                        console.log(this.ticketData)
                                                                        }
                                                                    })
            this.show = false
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
.date_x_container{
    position: relative !important;
    top: -13px;
}

.close_x{
    position: relative;
    left: 95%;
}

</style>