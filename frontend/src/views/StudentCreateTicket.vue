<template>
  <div>
    <UserNavbar :id_="2"></UserNavbar>

    <b-container fluid="xll" style="margin: 20px;">
      <b-row class="text-start">
        <b-col cols="12" sm="6" md="8">
          <h2 style="text-align: center; font-weight: 500;">Create Ticket</h2>
          <div style="border: 2px solid black; padding: 30px;">
          <TicketForm :hideReset=false :editTicket=false @title-change="onTitleChange"></TicketForm>
          </div>
        </b-col>
        <b-col cols="12" sm="6" md="4">
          
            <h2 style="text-align: left; font-weight: 700;">Search Results</h2>
            <div style="border: 2px solid black; padding: 30px; height: 500px; overflow-y: auto;">
            <div v-for="ticket in ticket_card_details" :key="ticket.ticket_id">
              <template v-if="ticket.type === 'public' && ticket.title.toLowerCase().includes(ticketTitle.toLowerCase())">
                <StudentTicketCard :ticket_id="ticket.ticket_id" :created_on="ticket.created_on" :title="ticket.title"
                  :chat="ticket.chat" :type="ticket.type" :status="ticket.status" :public_ticket_url="ticket.discourse_public_ticket_url">
                </StudentTicketCard>
              </template>
            </div>
          </div>
        </b-col>
      </b-row>
      </b-container>        
    <br />
  </div>
</template>

<script>
import UserNavbar from "../components/UserNavbar.vue";
import TicketForm from "../components/TicketForm.vue";
import StudentTicketCard from "../components/StudentTicketCard.vue";
import SearchTicket from "../components/SearchTicket.vue";
import * as common from "../assets/common.js";

export default {
  name: "StudentCreateTicket",
  components: { UserNavbar, TicketForm, SearchTicket ,StudentTicketCard},
  data() {
    return {
      ticket_card_details:[],
      ticketTitle:'',
    };
  },
  methods: {
    onTitleChange(title) {
      this.ticketTitle = title;
      console.log(this.ticketTitle)
    }
  },
  computed: {
    filteredTickets() {
      return this.ticket_card_details.filter(
        ticket =>
          ticket.status === "unresolved" &&
          ticket.type === "public" &&
          ticket.title.toLowerCase().includes(this.searchTerm.toLowerCase())
      );
    }
  },
  created() {
    fetch(common.TICKET_API_ALLTICKETS, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        "web_token": this.$store.getters.get_web_token,
        "user_id": this.$store.getters.get_user_id,
      },
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then((data) => {
        if (data.category == "success") {
          this.flashMessage.success({
            message: `Total ${data.message.length} Tickets retrieved.`,
          });
          this.ticket_card_details = data.message;
          
          
        } else if (data.category == "error") {
          this.flashMessage.error({
            message: data.message,
          });
        }
      })
      .catch((error) => {
        console.error(`Error: ${error}`);
        this.flashMessage.error({
          message: "Internal Server Error",
        });
      });
  }
}

</script>

<style></style>