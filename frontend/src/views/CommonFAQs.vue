<!-- Edited by Yukti -->
<template>
	<div>
		<UserNavbar :id_="id_"></UserNavbar>

		<b-container fluid="xl">
			<b-row>
				<b-col cols="12" sm="12" md="12">
					<h3 style="text-align: center">Frequently Asked Questions</h3>
					<b-row>

						<b-col cols="5" sm="12" md="5">
							<b-form-group>
								<label for="input-query">Search Query:</label>
								<b-form-input id="input-query" v-model="query" type="text"
									placeholder="Enter search query"
									aria-describedby="input-live-feedback-query"></b-form-input> </b-form-group></b-col>
					</b-row>
					<div style="height: 550px; overflow: auto; padding: 10px">
						<div v-for="faq in filterCards" :key="faq.faq_id">
							<FAQCard :faq_id="faq.faq_id" :question="faq.question" :answer="faq.solution"
								:attachments="faq.attachments"></FAQCard>
						</div>
					</div>
				</b-col>
			</b-row>
		</b-container>
	</div>
</template>

<script>
import FAQCard from "../components/FAQCard.vue";
import UserNavbar from "../components/UserNavbar.vue";
import * as common from "../assets/common.js";
import Tagging from "../components/Tagging.vue";

export default {
	name: "CommonFAQs",
	components: { UserNavbar, FAQCard, Tagging },
	data() {
		return {
			id_: null,
			user_id: this.$store.getters.get_user_id,
			faq_card_details: [],
			filtered_faq_card_details: [],
			filter_tags: [],
			query: "",
			show: true,
		};
	},
	created() {
		let user_role = this.$store.getters.get_user_role;
		if (user_role == "student") {
			this.id_ = 4;
		}
		if (user_role == "support") {
			this.id_ = 3;
		}
		if (user_role == "admin") {
			this.id_ = 4;
		}
		let form = {
			filter_status: ["pending"],
		};
		let params = "";
		params = new URLSearchParams(form).toString();

		fetch(common.FAQ_API, {
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
						message: `Total ${data.message.length} FAQs retrieved.`,
					});
					this.faq_card_details = data.message;
					this.filtered_faq_card_details = data.message;
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
	computed: {
		filterCards() {
			const query = this.query.toLowerCase();
			return this.faq_card_details.filter(card => {
				return (
					(card.question && card.question.toLowerCase().includes(query)) ||
					(card.solution && card.solution.toLowerCase().includes(query))
				);
			});
		},
	},
};
</script>

<style></style>
