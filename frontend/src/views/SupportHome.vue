<template>
  <div>
    <UserNavbar :id_="1"></UserNavbar>

    <b-container fluid="xll" style="margin: 20px; height: 100vh;">
      <b-row class="text-start">
        <b-col cols="12" sm="7" md="8">
          <h3 style="text-align: center">Unresolved Tickets</h3>
          <div style="height: 80 vh; padding: 10px; border: 2px solid black;">
            <SearchTicketNew
              
              :ticket_card_details="unresolved_tickets"
            ></SearchTicketNew>
          </div>
        </b-col>
        <b-col cols="12" sm="5" md="4" >
          <h3 style="text-align: center">My Activity</h3>
          <div style="border: 2px solid black;">
          <InfoCard title="tickets resolved" :value="n_tickets_resolved.toString()"></InfoCard>
          <InfoCard
            title="tickets pending"
            :value="n_total_unresolved_tickets.toString()"
          ></InfoCard>
          </div>
        </b-col>
      </b-row>
    </b-container>
  </div>
</template>

<script>
import UserNavbar from "../components/UserNavbar.vue";
import * as common from "../assets/common.js";
import InfoCard from "../components/InfoCard.vue";
import SearchTicket from "../components/SearchTicket.vue";
import SearchTicketNew from "@/components/SearchTicketNew.vue"; 

export default {
  name: "SupportHome",
  components: { UserNavbar, InfoCard, SearchTicket , SearchTicketNew},
  data() {
    return {
      n_tickets_resolved: 0,
      n_total_unresolved_tickets: 0,
      unresolved_tickets:[],
      user_id: this.$store.getters.get_user_id,
    };
  },
  created() {
    fetch(common.TICKET_API_ALLTICKETS + `/${this.user_id}`, { // Edited by yukti -> fetched from a new api.
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        web_token: this.$store.getters.get_web_token,
        user_id: this.user_id,
      },
    })
      .then((response) => response.json())
      .then((data) => {
        console.log(data)
        if (data.category == "success") {
          this.flashMessage.success({
            message: "User data retrieved.",
          });

          this.n_tickets_resolved = data.message.resolved_tickets ? data.message.resolved_tickets.length : 0;
          this.n_total_unresolved_tickets = data.message.unresolved_tickets ? data.message.unresolved_tickets.length : 0;
          this.unresolved_tickets = data.message.unresolved_tickets; // For passing on the data to the search ticket new component.
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
  mounted() {},
  methods: {},
  computed: {},
};
</script>

<style></style>
