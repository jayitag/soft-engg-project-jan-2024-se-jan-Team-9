<template>
    <div >
      <UserNavbar :id_="1"></UserNavbar>

      <div class="container">
      <FlagTicketCard></FlagTicketCard>
      <FlagTicketCard></FlagTicketCard>
      <FlagTicketCard></FlagTicketCard>
      <FlagTicketCard></FlagTicketCard>
      <FlagTicketCard></FlagTicketCard>
      <FlagTicketCard></FlagTicketCard>
      <FlagTicketCard></FlagTicketCard>
      </div>
      
    </div>
  </template>
  
  <script>
  import UserNavbar from "../components/UserNavbar.vue";
//   import * as common from "../assets/common.js";
  import FlagTicketCard from "../components/FlagTicketCard.vue"
  
  export default {
    name: "FlagTickets",
    components: { UserNavbar, FlagTicketCard  },
    data() {
      return {
        
      };
    },
    created() {
    },
    mounted() {},
    
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
  