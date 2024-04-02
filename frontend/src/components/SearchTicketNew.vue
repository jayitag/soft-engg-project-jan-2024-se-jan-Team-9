<template>
  <div class="search-ticket-form">
    <!-- Search form -->
    <b-form @submit.prevent="onSubmit" class="search-form">
      <b-container class="search-filters" fluid="xll">
        <b-row>
          <b-col cols="12">
            <b-form-group>
              <label for="input-query">Search Query:</label>
              <b-form-input
                id="input-query"
                v-model="form.query"
                type="text"
                placeholder="Enter search query"
              ></b-form-input>
            </b-form-group>
          </b-col>
        </b-row>
      </b-container>
      <!-- <b-button style="margin: 10px" type="submit" variant="primary">Search</b-button> -->
    </b-form>

    <!-- Ticket cards display -->
    <b-container fluid="xll">
        <b-row>
          <b-col cols="12">
            <div style="height: 500px; overflow: auto; padding: 20px;">
        <div v-for="ticket in filteredTickets" :key="ticket.ticket_id">
          <SupportStaffTicketCard
            :ticket_id="ticket.ticket_id"
            :created_on="ticket.created_on"
            :title="ticket.title"
            :chat="ticket.chat || ''"
            :created_by="ticket.created_by"
            :support_staff_tag_id="ticket.support_staff_tag_id"
            :is_faq="ticket.is_faq"
            :is_flag="ticket.is_flag"
            :status="ticket.status"
          ></SupportStaffTicketCard>
        </div>
      </div>
          </b-col>
        </b-row>
    </b-container>
  
    </div>
</template>

<script>
import SupportStaffTicketCard from "../components/SupportStaffTicketCard.vue";

export default {
  name: "SearchTicket",
  components: { SupportStaffTicketCard },
  props: ["upvote_disabled", "delete_disabled", "edit_disabled", "ticket_card_details"],
  data() {
    return {
      form: {
        query: "",
      },
    };
  },
  computed: {
    filteredTickets() {
      if (!this.form.query || !Array.isArray(this.ticket_card_details)) {
        console.log(this.ticket_card_details)
        return this.ticket_card_details;
      }
      const query = this.form.query.toLowerCase();
      console.log(this.ticket_card_details.filter(ticket => {
        return (
          (ticket.title && ticket.title.toLowerCase().includes(query)) ||
          (ticket.description && ticket.description.toLowerCase().includes(query))
        );
      }))
      return this.ticket_card_details.filter(ticket => {
        return (
          (ticket.title && ticket.title.toLowerCase().includes(query)) ||
          (ticket.description && ticket.description.toLowerCase().includes(query))
        );
      });
    },
  },
  methods: {
    onSubmit() {
      // No need for API call, as searching is done client-side
    },
  },
};
</script>

<!-- style scoped>
.search-ticket-form {
  display: flex;
  flex-direction: row-reverse; /* Reverse the order of flex items */
}

.search-form-container {
  flex: 1;
  display: flex;
  justify-content: flex-end; /* Align search form to the right */
  padding-right: 10px; /* Add some padding on the right */
}

.ticket-cards {
  flex: 3; /* Take up more space than the search form */
  margin-right: 20px; /* Add some margin between the tickets and search form */
}
</style -->