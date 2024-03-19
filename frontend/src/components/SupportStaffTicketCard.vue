<template>
  <div :key="componentKey">
    <b-container class="ticket-card-container" v-show="!ticket_deleted" :style="{
    'background-color': getBackgroundColor()
  }">
      <b-row class="row" @click="getTicketDetails">
        <b-col class="col" cols="7" md="8" lg="8"><i>Ticket ID: </i>{{ ticket_id.slice(0, 15) }}</b-col>
        <b-col class="col text-right" cols="5" md="4" lg="4"><i>Created On: </i>{{ created_on }}</b-col>
      </b-row>
      <b-row class="row">
        <b-col class="col" cols="12" @click="getTicketDetails">
          <b-row class="row">
            <b-col class="col" cols="12"><b>Title: </b>{{ title.slice(0, 80) }}</b-col>
          </b-row>
          <b-row class="row">
            <b-col class="col" cols="12"><b>Description: </b>{{ description.slice(0, 200) }}</b-col>
          </b-row>
        </b-col>
      </b-row>
      <b-row class="row ticket-card-buttons">
        <b-col class="col text-right">
          <b-button v-if="status === 'resolved' && !(is_faq === 'True')" variant="link" @click="suggestForFAQ">Suggest
            for
            FAQ</b-button>
          <div v-if="status === 'resolved' && (is_faq === 'True')">This ticket is already marked as an FAQ</div>
          <b-button variant="link" @click="showChat()"><b-icon icon="reply" aria-hidden="true"></b-icon>Reply</b-button>
          <b-dropdown variant="link" text="Forward" right>
            <b-dropdown-item v-for="(option, index) in forwardOptions" :key="index" @click="forwardTicket(index)">
              {{ option }}
            </b-dropdown-item>
          </b-dropdown>
          <b-button ref="flagButton" variant="link" @click="toggleFlag"> <b-icon :icon="is_flag ? 'flag-fill' : 'flag'"
              class="mr-1"></b-icon>
            Flag</b-button>

        </b-col>
      </b-row>
    </b-container>
    <ChatWindow v-if="displayChat" :format_chat="get_formated_ticket" :close_chat="closeChat" :chat="formated_chat" :tick_id="ticket_id"></ChatWindow>

  </div>
</template>

<script>
import * as common from "../assets/common.js";
import ChatWindow from "../components/ChatWindow.vue";

export default {
  name: "TicketCard",
  props: [
    "ticket_id",
    "created_on",
    "created_by",
    "title",
    "chat",
    "support_staff_tag_id",
    "is_faq",
    "is_flag",
    "status"
  ],
  components: { ChatWindow },
  created() {
    this.get_formated_ticket()
  },
  data() {
    return {
      componentKey: 0,
      forwardOptions: ['Higher authority', 'Relevant teams'],
      selectedOption: null,
      user_id: this.$store.getters.get_user_id,
      ticket_deleted: false,
      description: "",
      displayChat: false,
      formated_chat:""

    };
  },
  methods: {
    showChat() {
      this.displayChat = true;
    },
    closeChat() {
      this.displayChat = false;
    },
    get_formated_ticket() {
      // console.log(this.chat)
      // Your input string
      var inputString = this.chat;

      console.log(inputString)
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

      this.created_on = formatTimestamp(this.created_on)

      // Extracting the chat
      this.description = jsonArray[0].chat;


      this.formated_chat = jsonArray

    },
    openForwardDropdown() {
      this.$refs.forwardDropdown.toggle();
    },
    forwardTicket(index) {
      let destination = '';
      if (index === 0) {
        // Forward to Higher authority
        destination = 'higher_authority'; // Replace with actual destination
      } else if (index === 1) {
        // Forward to Relevant teams
        destination = 'relevant_teams'; // Replace with actual destination
      }
      console.log("forward ticket")
      // Make a request to forward the ticket
      // Replace this with your actual implementation using webhooks
      fetch('https://eoeb4ldad26yrmo.m.pipedream.net', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          ticket_id: this.ticket_id,
          destination: destination
        })
      })
        .then(response => {
          if (!response.ok) {
            throw new Error('Network response was not ok');
          }
          return response.json();
        })
        .then(data => {
          // Handle response if necessary
          console.log(data);
          this.$router.go();
        })
        .catch(error => {
          console.error('There was a problem with your fetch operation:', error);
        });
    },

    getBackgroundColor() {
      if (this.status === 'resolved' && this.support_staff_tag_id === this.user_id) {
        return 'lightgreen';
      } else if (!(this.status === 'resolved') && this.support_staff_tag_id === this.user_id) {
        return 'lightyellow';
      } else if (!(this.status === 'resolved')) {
        return 'lightred';
      } else {
        return ''; // Default background color
      }
    },
    suggestForFAQ() {
      // Implement suggest for FAQ functionality
      // You can add the necessary logic here
      fetch(common.TICKET_API + `/${this.ticket_id}` + `/${this.user_id}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          web_token: this.$store.getters.get_web_token,
          user_id: this.user_id,
        },
        body: JSON.stringify({ is_faq: "True", is_flag: this.is_flag, support_staff_tag_id: this.support_staff_tag_id, status: this.status, suggested_by_id: this.user_id }), // Include is_flag attribute in request body
        //field "suggested_by_id" added by Harman
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
            console.log("made an faq")
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
    getTicketDetails() {
      // Implement method to get ticket details
    },
    // reply() {
    //   // Implement reply functionality
    //   fetch(common.TICKET_API + `/${this.ticket_id}` + `/${this.user_id}`, {
    //     method: "PUT",
    //     headers: {
    //       "Content-Type": "application/json",
    //       web_token: this.$store.getters.get_web_token,
    //       user_id: this.user_id,
    //     },
    //     body: JSON.stringify({ is_faq: this.is_faq, is_flag: this.is_flag, support_staff_tag_id: this.user_id, status: "resolved" }), // Include is_flag attribute in request body
    //   })
    //     .then((response) => response.json())
    //     .then((data) => {
    //       if (data.category == "success") {
    //         this.flashMessage.success({
    //           message: data.message,
    //         });
    //         // Update UI or perform any other action upon successful flagging
    //         // const isfaq = document.querySelector('.flag-button');
    //         // flagButton.style.backgroundColor = 'darkred';
    //         console.log("Replied")
    //         // this.$router.go();

    //       }
    //       if (data.category == "error") {
    //         this.flashMessage.error({
    //           message: data.message,
    //         });
    //       }
    //     })
    //     .catch((error) => {
    //       this.$log.error(`Error : ${error}`);
    //       this.flashMessage.error({
    //         message: "Internal Server Error",
    //       });
    //     });
    // },
    forward() {
      // Implement forward functionality
    },
    toggleFlag() {
      // this.componentKey++;

      this.flag(); // Call your existing flag method
      this.$router.go();

    },
    flag() {
      console.log(this.$store.getters.get_web_token)

      fetch(common.TICKET_API + `/${this.ticket_id}` + `/${this.user_id}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          web_token: this.$store.getters.get_web_token,
          user_id: this.user_id,
        },
        body: JSON.stringify({ is_flag: "true", is_faq: this.is_faq, support_staff_tag_id: this.support_staff_tag_id, status: this.status }), // Include is_flag attribute in request body
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.category == "success") {
            this.flashMessage.success({
              message: data.message,
            });
            // Update UI or perform any other action upon successful flagging
            // this.$refs.flagButton.$el.style.backgroundColor = 'darkred';
            this.reloadTrigger = !this.reloadTrigger;
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

  }
}
</script>

<style scoped>
.ticket-card-container {
  box-shadow: 2px 4px 5px 5px #dbdada;
  background-color: rgb(255, 204, 204);
  margin: 12px 5px;
}

.ticket-card-container:hover {
  box-shadow: 5px 8px 8px 10px #888888;
  background-color: rgb(255, 255, 255);
}

.row {
  padding-top: 5px;
  padding-bottom: 5px;
}

.ticket-card-buttons button {
  background-color: transparent !important;
  color: black !important;
  /* Add this line */
}

.ticket-card-buttons:hover:not([disabled]) {
  border-color: #95ddfa;
  box-shadow: 0 12px 16px 0 rgba(0, 0, 0, 0.24), 0 17px 50px 0 rgba(0, 0, 0, 0.19);
}

button {
  background-color: transparent !important;
}
</style>
