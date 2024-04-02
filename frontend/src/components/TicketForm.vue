<template>
  <div
    class="ticket-form"
    style="margin-top: 5px; margin-left: 5px; margin-right: 5px; text-align: left"
  >
    <b-form @submit="onSubmit" @reset="onReset" v-if="show">
      <b-form-group
        ><b-form-input
          id="input-title"
          v-model="form.title"
          type="text"
          placeholder= "Enter title OR search title"
          :state="check_title"
          aria-describedby="input-live-feedback-title"
          :disabled="user_role == 'student' ? false : true"
          required
        ></b-form-input>
        <b-form-invalid-feedback id="input-live-feedback-title">
          Title should be atleast 15 characters long.
        </b-form-invalid-feedback>
      </b-form-group>

      <b-form-group
        ><b-form-textarea
          id="input-description"
          v-model="form.chat"
          type="text"
          placeholder="Enter description"
          rows="3"
          max-rows="6"
          :disabled="user_role == 'student' ? false : true"
          required
        ></b-form-textarea
      ></b-form-group>

      <b-container>
        <b-row>
          <b-col>
            <b-form-group
        label="Select Type:"
        title="Public tickets will be added to discourse, for peer collaboration"
        v-slot="{ ariaDescribedby }"
        v-show="user_role == 'student' ? true : false"
      >
        <b-form-radio-group
          id="radio-group-priority"
          v-model="form.type"
          :options="type_options"
          :aria-describedby="ariaDescribedby"
          name="radio-group-priority"
          required
        ></b-form-radio-group>
      
      </b-form-group>
          </b-col>
          <b-col>
            <b-form-group
        label="Select Support Staff(optional):"
        v-slot="{ ariaDescribedby }"
        v-show="user_role == 'student' ? true : false"
      >
            <b-form-select v-model="form.support_staff_tag_id" size="sm" :options="support_staff_option" ></b-form-select>
</b-form-group>
          </b-col>
          <b-col>
            <b-form-group
        label="Select Category:"
        v-slot="{ ariaDescribedby }"
        v-show="user_role == 'student' ? true : false"
      >
            <b-form-select v-model="form.catagory" size="sm" :options="category_option" required></b-form-select>
            </b-form-group>
          </b-col>
        </b-row>
      </b-container>

      <FileUpload @file_uploading="onFileUpload"></FileUpload>

      <br />
      <br />
      <b-button style="margin: 10px" type="submit" variant="primary">Submit</b-button>
      <b-button v-show="hideReset ? false : true" style="margin: 10px" type="reset" variant="danger"
        >Reset</b-button>

    </b-form>
    <br />
  </div>
</template>

<script>
import * as common from "../assets/common.js";
import FileUpload from "./FileUpload.vue";
// import Tagging from "./Tagging.vue";

export default {
  name: "TicketForm",
  props: ["ticket_id", "title", "description", "priority", "tags", "hideReset", "editTicket"],
  components: { FileUpload },
  data() {
    return {
      type_options: [
        { text: "Private", value: "private" },
        { text: "Public", value: "public" },
      ],
      support_staff_option: [
      { value: null, text: 'Please select an option' },
      ],
      category_option: [
          { value: null, text: 'Please select an option' },
          { value: 'Operational', text: 'Operational' },
          { value: 'Admistration', text: 'Admistration' },
          { value: 'Accounts', text: 'Accounts' },
          { value: 'Web Op', text: 'Web Op'}
      ],
      form: {
        title: "",
        chat: "",
        type: "",
        support_staff_tag_id: null,
        catagory: null,
        attachments: [],
      },
      user_role: this.$store.getters.get_user_role,
      show: true,
    };
  },
  watch: {
    'form.title': function(newTitle, oldTitle) {
      if (newTitle !== oldTitle) {
        this.$emit("title-change", newTitle);
      }
    }
  },
  created() {

  this.fetch_all_support_data();
    
  },
  methods: {
    fetch_all_support_data(){
      fetch(common.SUPPORT_API + "/fetch_all_support_data", {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          web_token: this.$store.getters.get_web_token,
          user_id: this.$store.getters.get_user_id,
        },
      })
        .then((response) => response.json())
        .then((data) => {
          for (let i in data.message){
            this.support_staff_option.push(data.message[i])
          }
        })
        .catch((error) => {
          this.$log.error(`Error : ${error}`);
          this.flashMessage.error({
            message: "Internal Server Error",
          });
        });
    },
    
    onFileUpload(value) {
      this.form.attachments.splice(0, this.form.attachments.length, ...value);
      for (let i = 0; i < this.form.attachments.length; i++) {}
    },
    onSubmit(event) {
      if (event && event.preventDefault) {
        event.preventDefault();
      }

      if (this.user_role == "student" && !this.check_title) { //Harman - negated title condition
        alert("title should be atleast 15 characters long.");
      } 
      else {
        alert('Submitting form. Click "Ok" to proceed?');
        this.$log.info("Submitting Ticket form");

        let fetch_url = common.TICKET_API + `/${this.$store.getters.get_user_id}`;
        let method = "POST";
    
        fetch(fetch_url, {
          method: method,
          headers: {
            "Content-Type": "application/json",
            web_token: this.$store.getters.get_web_token,
            user_id: this.$store.getters.get_user_id,
          },
          body: JSON.stringify(this.form),
        })
          .then((response) => response.json())
          .then((data) => {
            if (data.category == "success") {
              this.flashMessage.success({
                message: data.message,
              });
              if (!this.editTicket) {
                this.onReset();
              }
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
    onReset(event) {
      if (event && event.preventDefault) {
        event.preventDefault();
      }
      this.form.title = "";
      this.form.description = "";
      this.form.attachments = [];
      this.form.type = "";
      this.form.support_staff_selected= null;
      this.form.category_selected = null;
      this.show = false;
      this.$nextTick(() => {
        this.show = true;
      });
    },
  
  },
  computed: {
    check_title() {
      console.log(this.form.title.length)
      return this.form.title.length < 20 ? false : true;
    },
  },
};
</script>

<style></style>
