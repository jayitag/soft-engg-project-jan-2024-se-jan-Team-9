<template>
  <div>
    <UserNavbar :id_="1"></UserNavbar>
    <h1>Dashboard</h1> <!-- edited by shubham @ make Dashborad heading -->

    <b-container fluid="xll" style="margin: 20px;">
      <b-row class="text-start">
        <b-col cols="12" sm="5" md="8">
          <!-- <h3 style="text-align: center">My Unresolved Tickets</h3> -->
          <b-nav style="margin: 1px;">
            <b-nav-item @click="all_tickets_filter()" :style="all_tickets_filter_style">All Tickets</b-nav-item>
            <b-nav-item @click="resolved_tickets_filter()" :style="resolved_tickets_filter_style">Resolved
              Tickets</b-nav-item>
            <b-nav-item @click="unresolved_tickets_filter()" :style="unresolved_tickets_filter_style">Unresolved
              Tickets</b-nav-item>
          </b-nav>
          <div style="height: 550px; border: 2px solid black; overflow: auto; padding: 10px">
            <div v-for="ticket in filtered_ticket_card_details" :key="ticket.ticket_id">

              <StudentTicketCard :ticket_id="ticket.ticket_id" :created_on="ticket.created_on" :title="ticket.title"
                :chat="ticket.chat" :type="ticket.type" :status="ticket.status"></StudentTicketCard>
            </div>
          </div>
        </b-col>
        <!-- <b-col cols="12" sm="5" md="4" style="border: solid black"> -->
        <b-col cols="12" sm="5" md="4"> <!-- edited by shubham @ remove side border -->
          <!-- <h3 style="text-align: center">My Activity</h3> -->
          <h3 style="text-align: left">My Activity</h3> <!-- edited by shubham @ align title left -->
          <div style="border: 2px solid black;"> <!-- edited by shubham @ make border -->
            <InfoCard title="tickets created" :value="n_tickets_created.toString()"></InfoCard>
            <InfoCard title="tickets resolved" :value="n_tickets_resolved.toString()"></InfoCard>
            <InfoCard title="tickets pending" :value="n_tickets_pending.toString()"></InfoCard>
            <InfoCard title="tickets upvoted" :value="n_tickets_upvoted.toString()"></InfoCard>
          </div>
        </b-col>
      </b-row>
    </b-container>
  
    <br />
  </div>
</template>

<script>
import UserNavbar from "../components/UserNavbar.vue";
import * as common from "../assets/common.js";
import StudentTicketCard from "../components/StudentTicketCard.vue";
import InfoCard from "../components/InfoCard.vue";



export default {
  name: "StudentHome",
  components: { UserNavbar, StudentTicketCard, InfoCard },
  data() {
    return {
      n_tickets_created: 0,
      n_tickets_resolved: 0,
      n_tickets_pending: 0,
      n_tickets_upvoted: 0,
      user_id: this.$store.getters.get_user_id,
      ticket_card_details: [],
      filtered_ticket_card_details: [],
      all_tickets_filter_style: "text-decoration: underline 4px solid black;",
      resolved_tickets_filter_style: "",
      unresolved_tickets_filter_style: ""
    };
  },
  created() {

    fetch(common.STUDENT_API + `/${this.user_id}`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        web_token: this.$store.getters.get_web_token,
        user_id: this.user_id,
      },
    })
      .then((response) => response.json())
      .then((data) => {
        console.log(this.$store.getters.get_web_token)
        if (data.category == "success") {
          this.flashMessage.success({
            message: "User data retrieved.",
          });
          this.n_tickets_created = data.message.n_tickets_created;
          this.n_tickets_resolved = data.message.n_tickets_resolved;
          this.n_tickets_pending = data.message.n_tickets_pending;
          this.n_tickets_upvoted = data.message.n_tickets_upvoted;
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

    this.get_all_ticket_data()
    // fetch(common.TICKET_API_ALLTICKETS + `/${this.user_id}`, {
    //   method: "GET",
    //   headers: {
    //     "Content-Type": "application/json",
    //     web_token: this.$store.getters.get_web_token,
    //     user_id: this.user_id,
    //   },
    // })
    //   .then((response) => response.json())
    //   .then((data) => {
    //     if (data.category == "success") {
    //       this.flashMessage.success({
    //         message: `Total ${data.message.length} Tickets retrieved.`,
    //       });

    //       this.ticket_card_details = data.message.all_tickets;
    //     }
    //     if (data.category == "error") {
    //       this.flashMessage.error({
    //         message: data.message,
    //       });
    //     }
    //   })
    //   .catch((error) => {
    //     this.$log.error(`Error : ${error}`);
    //     this.flashMessage.error({
    //       message: "Internal Server Error",
    //     });
    //   });
  },
  mounted() { },
  methods: {
    all_tickets_filter() {
      this.all_tickets_filter_style = "text-decoration: underline 4px solid black;"
      this.resolved_tickets_filter_style = ""
      this.unresolved_tickets_filter_style = ""
      this.filtered_ticket_card_details = this.ticket_card_details

    },
    resolved_tickets_filter() {
      this.all_tickets_filter_style = ""
      this.resolved_tickets_filter_style = "text-decoration: underline 4px solid black;"
      this.unresolved_tickets_filter_style = ""
      this.filtered_ticket_card_details = []
      for (let ticket of this.ticket_card_details) {
        if (ticket.status == 'resolved') {
          this.filtered_ticket_card_details.push(ticket)
        }
      }
    
    },
    unresolved_tickets_filter() {
      this.all_tickets_filter_style = ""
      this.resolved_tickets_filter_style = ""
      this.unresolved_tickets_filter_style = "text-decoration: underline 4px solid black;"
      this.filtered_ticket_card_details = this.ticket_card_details
      this.filtered_ticket_card_details = []
      for (let ticket of this.ticket_card_details) {
        if (ticket.status == 'unresolved') {
          this.filtered_ticket_card_details.push(ticket)
        }
      }
    },
    get_all_ticket_data() {
      fetch(common.TICKET_API_ALLTICKETS + `/${this.user_id}`, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          web_token: this.$store.getters.get_web_token,
          user_id: this.user_id,
        },
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.category == "success") {
            this.flashMessage.success({
              message: `Total ${data.message.length} Tickets retrieved.`,
            });

            this.ticket_card_details = data.message.all_tickets;
            this.all_tickets_filter()
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
    }
  },
  computed: {},
};
</script>

<style></style>
