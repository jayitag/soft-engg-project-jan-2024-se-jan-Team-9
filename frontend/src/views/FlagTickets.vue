<template>
    <div >
      <UserNavbar :id_="1"></UserNavbar>

      <div class="container">
        <h1 v-if="empty" style="margin-top: 40px;">No Flag Tickets Found</h1>
        <FlagTicketCard v-for="i in ticketData"
        :ticket_id="i.id"
        :created_on="i.created_on"
        :title="i.title"
        :chat="i.description"
        :key="i.id"></FlagTicketCard>
      </div>
       

     
    </div>
  </template>
  
  <script>
  import UserNavbar from "../components/UserNavbar.vue";
  import * as common from "../assets/common.js";
  import FlagTicketCard from "../components/FlagTicketCard.vue"
  
  export default {
    name: "FlagTickets",
    components: { UserNavbar, FlagTicketCard  },
    data() {
      return {
        ticketData:'',
        empty:false
      };
    },
    created() {
    },
    mounted() {


      fetch(common.ADMIN_API + `/flag`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        web_token: this.$store.getters.get_web_token,
        user_id: this.user_id,
      },
    })
      .then((response) => response.json())
      .then((data) => {
        {
          // console.log(data)
          this.ticketData = data.flagdata
          // console.log(this.ticketData)
          // console.log(this.ticketData.length)
          if (this.ticketData.length === 0){ this.empty = true}

        }
      })
    



      // 
    },
    
    
  };
  </script>
  
  <style>
  .container {
        
        display: flex;
        flex-direction: column;
        justify-content: center; /* Horizontally center */
        align-items: center; /* Vertically center */
        
    }
  </style>
  