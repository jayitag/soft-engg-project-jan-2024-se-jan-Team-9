<template>
    <div >
      <UserNavbar :id_="1"></UserNavbar>

      <div class="container">
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
        ticketData:''
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
          console.log(this.ticketData)
        }
      })
    



      // 
    }
    
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
  