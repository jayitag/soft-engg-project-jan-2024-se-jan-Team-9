<template>
  <div :key="componentKey">
    <b-container class="ticket-card-container" fluid="xll" v-show="!ticket_deleted" :style="{
    'background-color': getBackgroundColor()
  }" style="padding:10px;">
      <b-row class="row" @click="getTicketDetails">
        <b-col class="col" cols="7" md="8" lg="8"><i>Ticket ID: </i>{{ ticket_id.slice(0, 15) }}</b-col>
        <b-col class="col text-right" cols="5" md="4" lg="4"><i>Created On: </i>{{ created_on }}</b-col>
      </b-row>
      <b-row class="row">
        <b-col class="col" cols="12" @click="getTicketDetails">
          <b-row class="row">
            <b-col class="col" cols="12"><b>Title: </b>{{ title.slice(0, 50) }}..</b-col>
          </b-row>
          <b-row class="row">
            <b-col class="col" cols="12"><b>Description: </b>{{ JSON.parse(chat)[0].chat.slice(0,80) }}..</b-col>
          </b-row>
          
        </b-col>
      </b-row>
      <b-row class="row ticket-card-buttons">
        <b-col>
          <b-button variant="link" v-show="this.support_staff_tag_id === this.user_id" style="height: 40px; margin-right: 10px; text-decoration: none;"><p style="color: darkgreen;"> <b-icon icon="tag-fill" scale="1" variant="success"></b-icon>Tagged</p></b-button>
          <b-button variant="link" v-if="status === 'resolved' && (is_faq === 'True')" style="height: 40px; text-decoration: none;"><p style="color: blue;"><b-icon icon="bookmarks-fill" variant="primary"></b-icon>Suggested for FAQ</p></b-button>

        </b-col>
        <b-col class="col text-right">
          <b-button v-if="status === 'resolved' && !(is_faq === 'True')" variant="link" @click="suggestForFAQ"><b-icon icon="bookmarks"></b-icon>Suggest
            for
            FAQ</b-button>
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
    <ChatWindow v-if="displayChat"  :close_chat="closeChat" :chat="formated_chat" :tick_id="ticket_id" :ticket_title="title"></ChatWindow>

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
    // this.get_formated_ticket()
  },
  data() {
    return {
      componentKey: 0,
      forwardOptions: ['Higher authority', 'Operations Team', 'Administration', 'Accounts Team'],
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
    forwardTicket(index) { //edited by yukti
          let webhookUrl = '';
          let destination='';

          // Determine the destination based on the index and set the appropriate webhook URL
          switch (index) {
            case 0:
              // Forward to Higher authority
              webhookUrl = 'https://chat.googleapis.com/v1/spaces/AAAASF1IRAg/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=WazRo0Emq6CtZw7UAvpluu626SHgxADt1cuwyAxybdk';  // Replace with the actual webhook URL
              destination = 'Higher Authority'
              break;
            case 1:
              // Forward to Operations team
              webhookUrl = 'https://chat.googleapis.com/v1/spaces/AAAAUt0p1VY/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=Q9AM8GnoIebsVBy3foAq9as8B-Hmo8lguuGJIrVaIsE';  // Replace with the actual webhook URL
              destination = 'Operations Team'
              break;
            case 2:
              // Forward to Administration
              webhookUrl = 'https://chat.googleapis.com/v1/spaces/AAAAGHeFNSk/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=ekdM6NMOCs39XfeV6_eBbgGlLmZZcE9sREybPl69eqw';  // Replace with the actual webhook URL
              destination='Administration'
              break;
            case 3:
              // Forward to Accounts
              webhookUrl = 'https://chat.googleapis.com/v1/spaces/AAAAIIVFGM4/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=feMjyp2u50RUQw0JGTBH0vFmZ_3GyFwPtil51k4aUn0';  // Replace with the actual webhook URL
              destination='Accounts Team'
              break;
            default:
              onsole.error('Invalid index, no valid destination.');
              return; // Exit if no valid index is provided
          }
          console.log("forward ticket")
          // Make a request to forward the ticket
          // Replace this with your actual implementation using webhooks
          fetch(webhookUrl, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({
              text: `*Forwarded for escalation to ${destination}.* \n \n Ticket ID: ${this.ticket_id}.  \n Title : ${this.title}. \n Description : ${JSON.parse(this.chat)[0].chat}. \n Forwarded by : ${this.$store.getters.get_user_email}.`
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
            console.log('Successfully forwarded:', data);
            this.$router.go();  // assuming you want to navigate to another route
          })
          .catch(error => {
            console.error('There was a problem with your fetch operation:', error);
          });
      },
    openForwardDropdown() {
      this.$refs.forwardDropdown.toggle();
    },
   

    getBackgroundColor() {
      if (this.status === 'resolved' && this.support_staff_tag_id === this.user_id) {
        return 'rgba(200, 246, 198, 0.959)';
      } else if ((this.status === 'resolved' )) {
        return 'rgba(200, 247, 209, 0.500)';
      } else if ((this.status === 'unresolved') && this.support_staff_tag_id === this.user_id) {
        return 'rgba(235, 237, 200, 0.959)'
      } else if ((this.status === 'unresolved')) {
        return 'rgba(235, 237, 200, 0.500)';
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
        body: JSON.stringify({ is_flag: "True", is_faq: this.is_faq, support_staff_tag_id: this.support_staff_tag_id, status: this.status }), // Include is_flag attribute in request body
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
  /* box-shadow: 2px 4px 5px 5px #dbdada; */
  background-color: rgb(255, 204, 204);
  margin: 12px 5px;
}

/* .ticket-card-container:hover {
  box-shadow: 5px 8px 8px 10px #888888;
  background-color: rgb(255, 255, 255);
} */

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
  /* box-shadow: 0 12px 16px 0 rgba(0, 0, 0, 0.24), 0 17px 50px 0 rgba(0, 0, 0, 0.19); */
}

button {
  background-color: transparent !important;
}
</style>
