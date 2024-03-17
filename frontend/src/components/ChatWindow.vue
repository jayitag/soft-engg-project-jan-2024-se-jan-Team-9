<template>
  
  <div class="chat_window">
    <h3 class="card_title">Title: {{ ticket_title }}</h3>
    <button class="close_button" @click="close()">
                                <span class=" X"></span>
      <span class="Y"></span>
    </button>
    <div class="chatBox">
      <div class="chat_display">
        <div v-for="(value, key) in massages" :key="key">
          <p :class="['chat_bubble',  value.role]">{{ value.chat }} </p>
          <p :class="['chat_bubble_name_' + value.role]">{{ value.name }} </p>
          <p :class="['chat_bubble_date_' + value.role]">{{ value.date_time }} </p>
        </div>
      </div>
      
      <form id="chatInputForm">
        <b-row>
          <b-col cols="12" sm="9" md="10">
            <textarea rows="3" cols="60" name="text" id="textInput" v-model="form.new_message"></textarea>

          </b-col>
          <b-col cols="12" sm="3" md="2">
            <b-button variant="outline-primary" @click="sendMassage"> Submit</b-button>
            <!-- <button id="textInputButton" class="btn btn-primary" @click="sendMessage()"
              style="width: 100%;">Submit</button> -->
          </b-col>
        </b-row>
      </form>
    </div>
    

  </div>
</template>

<script>

import * as common from "../assets/common.js";

export default {
  props: {
    tick_id: String,
    close_chat: Function,
    format_chat: Function,
    ticket_title:String
  },
  data() {
    return {
      form: {
        new_message: "",
      },
      massages: "",
      user_logined_role: this.$store.getters.get_user_role,
    }
  },
  created() {
    this.get_chat()
  },
  methods: {
    close() {
      this.close_chat();
    },
    get_chat() {
      fetch(common.CHAT_API + `/${this.tick_id}/${this.$store.getters.get_user_id}`, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          web_token: this.$store.getters.get_web_token,
          user_id: this.$store.getters.get_user_id,
        },
      })
        .then((response) => response.json())
        .then((data) => {

          if (data.category == "success") {
            // console.log("chat_fetched",data.message)
            console.log(this.ticket_title)


            var inputString = data.message;


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


            this.massages = jsonArray

            console.log(this.massages)
          }
          if (data.category == "error") {
            
            this.flashMessage.error({
              message: data.message,
            });
          }
        })
        .catch((error) => {
          this.$log.error(`Error : ${error}`);
          console.error(error)
          this.flashMessage.error({
            message: "Internal Server Error",
          });
        });
    },
    sendMassage() {
      console.log(this.newMassage)
      if (this.newMassage != "") {
        let fetch_url = common.CHAT_API + `/${this.tick_id}/${this.$store.getters.get_user_id}`;
        let method = "PUT";

        fetch(fetch_url, {
          method: method,
          headers: {
            "Content-Type": "application/json",
            web_token: this.$store.getters.get_web_token,
            user_id: this.$store.getters.get_user_id,
          },
          body: JSON.stringify(this.form),
        })
          .then((response) => response.json())
          .then((data) => {
            if (data.category == "success") {
              this.get_chat()
              console.log("chat sent")
              console.log(data.message)
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





        console.log(this.newMassage)
        this.form.new_message = ""
      }
    }
  }
}
</script>

<style scoped>
.chat_window {
  width: 100vw;
  height: 200%;
  position: absolute;
  z-index: 1;
  top: -40%;
  left: -10px;
  background-color: rgba(255, 255, 255, 0);
  /* backdrop-filter: blur(10px); */
}

.close_button {
  position: relative;
  top: 13%;
  width: 2.5em;
  height: 2.5em;
  border: none;
  background: rgba(190, 98, 121, 0.558);
  border-radius: 5px;
  transition: background 0.5s;
  float: right;
  right: 24.1vw;
  margin-top: 5px;
  margin-right: 5px;
  z-index: 10;
}

.X {
  content: "";
  position: absolute;
  top: 50%;
  left: 50%;
  width: 1em;
  height: 1.5px;
  background-color: rgb(255, 255, 255);
  transform: translateX(-50%) rotate(45deg);
}

.Y {
  content: "";
  position: absolute;
  top: 50%;
  left: 50%;
  width: 1em;
  height: 1.5px;
  background-color: #fff;
  transform: translateX(-50%) rotate(-45deg);
}



.close_button:hover {
  background-color: rgb(211, 21, 21);
}

.close_button:active {
  background-color: rgb(130, 0, 0);
}

.close_button:hover>.close {
  animation: close 0.2s forwards 0.25s;
}

@keyframes close {
  100% {
    opacity: 1;
  }
}

.chatBox {
  width: 50%;
  height: 49%;
  /* border-style: solid;
    border-color: black; */
  position: relative;
  transform: translate(52%, 26%);
  background-color: #fff;
  border-style: solid;
  border-color: #ffffff;
  border-width: 30px;
  border-bottom-width: 40px;
  border-top-width: 70px;
  box-shadow: rgb(163, 163, 163) 5px 5px 15px 5px;
  border-radius: 5PX;
}

#textInputButton {
  background-color: blue;
  color: white;
  border-color: rgb(0, 123, 255);
  font-size: 18px;
  border-radius: 7px;
  height: 51px;
  /* width: 112px; */
  margin-left: 10px;
  float: right;
  position: relative;


}

#textInput {
  width: 102% !important;
  resize: none;
  position: relative;
  border-color: #28a745;
  padding-right: calc(1.5em + 0.75rem);
  display: block;
  /* width: 80%; */
  height: 51px;
  padding: 0.375rem 0.75rem;
  font-size: 1rem;
  font-weight: 400;
  line-height: 1.5;
  color: #495057;
  border: 1px solid;
  border-radius: 0.25rem;
  transition: border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
  overflow: visible;
  float: left;
}

#chatInputForm {
  position: relative;

}

.chat_display {
  widows: 100%;
  height: 90%;
  overflow: auto;
  margin-bottom: 20px;
}


.chat_bubble {
  display: inline-block;
  max-width: 550px;
  overflow-wrap: break-word;
  white-space: pre-wrap;
  padding: 10px;
  font-size: 17px;
}

.student {
  position: relative;
  background-color: #02D926;
  color: #fff;
  float: right;
  clear: both;
  right: 10px;
  border-radius: 10px 10px 2px 10px;
}

.support {
  position: relative;
  float: left;
  clear: both;
  left: 10px;
  background-color: #009EFF;
  color: #fff;
  border-radius: 10px 10px 10px 2px;
}

.chat_bubble_name_student {
  position: relative;
  float: right;
  clear: both;
  right: 10px;
}

.chat_bubble_name_support {
  position: relative;
  float: left;
  clear: both;
  left: 10px;

}

.chat_bubble_date_student {
  position: relative;
  float: right;
  clear: both;
  right: 10px;
}

.chat_bubble_date_support {
  position: relative;
  float: left;
  clear: both;
  left: 10px;

}

.chat_bubble_name_student,
.chat_bubble_name_support {
  color: #00000073;
  font-size: 11px;
  top: -15px
}

.chat_bubble_date_support,
.chat_bubble_date_student {
  color: #00000073;
  font-size: 11px;
  top: -35px;
}

.card_title{
  position: relative;
    transform: translate(63%, 612%);
    z-index: 1;
    font-weight: bold;
    width: 671px;
    overflow: hidden;
    text-overflow: ellipsis;
}
</style>