<template>
  <div>
    <UserNavbar :id_="3"></UserNavbar>
    <br>
    <b-container fluid="xll">
      <b-row class="text-start">
        <b-col cols="1"></b-col>
        <b-col cols="6">
          <h3 style="text-align: center"><br>Suggestions</h3>
          <div style="  padding: 10px ;border: 2px solid black;">
            <SearchTicketFAQ :ticket_card_details="resolved_tickets" />

          </div>
        </b-col>
        <!-- <b-col cols="1"></b-col> -->
        <b-col cols="4">
          <h3 style="text-align: center"><br>Create FAQ</h3>
          <div style="height: 550px; overflow: auto; padding: 10px ;border: 2px solid black;">
            <FAQForm></FAQForm>

          </div>
        </b-col>
        <b-col cols="1"></b-col>
      </b-row>
    </b-container>
  </div>
</template>

<script>
import UserNavbar from "../components/UserNavbar.vue";
import * as common from "../assets/common.js";
import TicketForm from "../components/TicketForm.vue";
import SearchTicketFAQ from "../components/SearchTicketFAQ.vue";
import FAQForm from "../components/FAQForm.vue";

export default {
  name: "AdminCreateFAQ",
  components: { UserNavbar, FAQForm, SearchTicketFAQ },
  data() {
    return {
      resolved_tickets:[],
      user_id: this.$store.getters.get_user_id,
    };
  },
  created() {
    fetch(common.TICKET_API_ALLFAQTICKETS + `/${this.user_id}`, { // Harman
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        web_token: this.$store.getters.get_web_token,
        user_id: this.user_id,
      },
    })
      .then((response) => response.json())
      .then((data) => {
        //console.log(data.message)
        if (data.category == "success") {
          this.flashMessage.success({
            message: "Data retrieved",
          });

          this.resolved_tickets = data.message; // For passing on the data to the search ticket new component.
          console.log("res_tickets");
          // const chat = JSON.parse(data.message[0].chat);
          // const solution = chat[chat.length - 1].chat;
          // console.log(solution);
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
