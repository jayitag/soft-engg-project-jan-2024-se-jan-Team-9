<!--Please make sure that SupportStaff can mark only those 
tickets for flag which are already resolved -->
<template>
    <div class="search-ticket-form">
      <!-- Search form -->
      <b-form @submit.prevent="onSubmit" class="search-form">
        <b-container class="search-filters">
          <b-row>
            <b-col cols="12">
              <b-form-group>
                <label for="input-query">Search resolved tickets:</label>
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
    </b-form>
  
    <!-- Ticket cards display -->
    <b-container>
        <b-row>
            <b-col cols="12">
                <div style="height: 500px; overflow: auto;"">
                    <div v-for="ticket in filteredTickets" :key="ticket.id" style="padding-bottom: 10px;">
                      <FAQTicketCard 
                        :ticket_id="ticket.ticket_id" 
                        :created_on="ticket.created_on" 
                        :title="ticket.title"
                        :chat="ticket.chat" 
                        :type="ticket.type" 
                        :status="ticket.status"
                        :suggested_by_name="ticket.suggested_by_name"></FAQTicketCard>
                    </div>
                </div>
            </b-col>
        </b-row>
    </b-container>
    
      </div>
</template>
  
<script>
  import FAQTicketCard from "../components/FAQTicketCard.vue";
  export default {
    name: "SearchTicketFAQ",
    components: {FAQTicketCard},
    props: ["ticket_card_details"],
    data() {
      return {
        form: {
          query: "",
        },
      };
    },
    computed: {
      filteredTickets() {
        if (!Array.isArray(this.ticket_card_details)) {
          console.log("no details found")
          //return this.ticket_card_details;
        }
        else {
            const query = this.form.query.toLowerCase();
            // console.log(this.ticket_card_details.filter(ticket => {
            // return (
            //     (ticket.title && ticket.title.toLowerCase().includes(query)) ||
            //     (ticket.description && ticket.description.toLowerCase().includes(query))
            // );
            // }))
            return this.ticket_card_details.filter(ticket => {
                return (
                    (ticket.title && ticket.title.toLowerCase().includes(query)) ||
                    (ticket.description && ticket.description.toLowerCase().includes(query))
                );
            });
        }
        
      },
    },
    methods: {
      onSubmit() {
        // No need for API call, as searching is done client-side
      },
      // solution(ticket) {
      //   const chat = JSON.parse(ticket.chat);
      //   const solution = chat[chat.length - 1].chat;
      //   return solution;
      // }
    },
  };
</script>