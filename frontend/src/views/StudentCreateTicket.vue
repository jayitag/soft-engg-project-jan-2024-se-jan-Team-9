<template>
  <div>
    <UserNavbar :id_="2"></UserNavbar>

    <b-container fluid="xll" style="margin: 20px;">
      <b-row class="text-start">
        <b-col cols="12" sm="6" md="8">
          <h2 style="text-align: center; font-weight: 500;">Create Ticket</h2>
          <div style="border: 2px solid black; padding: 30px;">
          <TicketForm :hideReset=false :editTicket=false></TicketForm>
          </div>
        </b-col>
        <b-col cols="12" sm="6" md="4">
          <h2 style="text-align: left; font-weight: 700;">Search Results</h2>
          <div style="border: 2px solid black; padding: 30px;">
          </div>
          <!-- <SearchTicket :upvote_disabled="false"
          :delete_disabled="true"
          :edit_disabled="true"></SearchTicket> -->
        </b-col>
      </b-row>
    </b-container>

    <br />
  </div>
</template>

<script>
import UserNavbar from "../components/UserNavbar.vue";
import TicketForm from "../components/TicketForm.vue";
import SearchTicket from "../components/SearchTicket.vue";

export default {
  name: "StudentCreateTicket",
  components: { UserNavbar, TicketForm, SearchTicket },
  data() {
    return {};
  },
  mounted() {},
  methods: {},
  computed: {},
};
</script>

<style></style>
