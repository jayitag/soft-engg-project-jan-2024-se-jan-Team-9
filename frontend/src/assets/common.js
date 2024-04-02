/* eslint-disable */

const BASEURL = "http://127.0.0.1:5000";
const VERSION = "v1";

const AUTH_API_PREFIX = `/api/${VERSION}/auth`;
const STUDENT_API_PREFIX = `/api/${VERSION}/student`;
const SUPPORT_API_PREFIX = `/api/${VERSION}/support`;
const ADMIN_API_PREFIX = `/api/${VERSION}/admin`;
const FAQ_API_PREFIX = `/api/${VERSION}/faq/`;
const TICKET_API_PREFIX = `/api/${VERSION}/ticket`;
const CHAT_API_PREFIX = `/api/${VERSION}/chat`;    // added  by Shubham



const AUTH_API_LOGIN = `${BASEURL}${AUTH_API_PREFIX}/login`
const AUTH_API_REGISTER = `${BASEURL}${AUTH_API_PREFIX}/register`
const AUTH_API_NEWUSERS = `${BASEURL}${AUTH_API_PREFIX}/newUsers`

const STUDENT_API = `${BASEURL}${STUDENT_API_PREFIX}`;
const SUPPORT_API = `${BASEURL}${SUPPORT_API_PREFIX}`;
const ADMIN_API = `${BASEURL}${ADMIN_API_PREFIX}`;
const FAQ_API = `${BASEURL}${FAQ_API_PREFIX}`;
const TICKET_API = `${BASEURL}${TICKET_API_PREFIX}`;

const TICKET_API_ALLTICKETS = `${BASEURL}${TICKET_API_PREFIX}/all-tickets`;
// Added by yukti -  TICKET_API_ALL_SUPPORT_TICKETS for support staff to fetch all tickets both resolved and unresolved.
// const TICKET_API_ALL_SUPPORT_TICKETS = `${BASEURL}${TICKET_API_PREFIX}/all-support-tickets`; 
// Added by yukti -  api to flag a ticket.
// const SUPPORT_STAFF_FLAG_API= `${BASEURL}${TICKET_API_PREFIX}/support-staff-flag-api`; 

const CHAT_API = `${BASEURL}${CHAT_API_PREFIX}`; // added  by Shubham
const TICKET_API_ALLFAQTICKETS = `${BASEURL}${TICKET_API_PREFIX}/all-faq-tickets`; //added by Harman





const STUDENT_ROUTES = ['/student', '/student-home', "/student-create-ticket", "/student-my-tickets", "/common-faqs", "/user-profile"]
const SUPPORT_ROUTES = ['/support', '/support-home', "/support-my-tickets", "/common-faqs", "/user-profile","/fetch_all_support_data" ]
const ADMIN_ROUTES = ['/admin', '/admin-home', "/admin-create-faq", "/admin-validate-users", "/common-faqs", "/user-profile" , "/flag-ticket"]


const STUDENT_NAV_BUTTONS = [
  { id: 1, title: "Home", link: "/student-home", active: false },
  { id: 2, title: "Create Ticket", link: "/student-create-ticket", active: false },
  // { id: 6, title: "Discourse", link: "http://localhost:4200/", active: false },    //-edited by shubham.
  { id: 4, title: "FAQs", link: "/common-faqs", active: false },
  // { id: 5, title: "Logout", link: "#", active: false },
]

const SUPPORT_NAV_BUTTONS = [
  { id: 1, title: "Home", link: "/support-home", active: false },
  { id: 2, title: "My Tickets", link: "/support-my-tickets", active: false },
  // { id: 6, title: "Discourse", link: "http://localhost:4200/", active: false },    //-edited by shubham.
  { id: 3, title: "FAQs", link: "/common-faqs", active: false },
  // { id: 4, title: "Logout", link: "#", active: false },
]

const ADMIN_NAV_BUTTONS = [
  { id: 1, title: "Home", link: "/admin-home", active: false },
  { id: 2, title: "Validate Users", link: "/admin-validate-users", active: false },
  { id: 3, title: "Create FAQ", link: "/admin-create-faq", active: false },
  // { id: 6, title: "Discourse", link: "http://localhost:4200/", active: false },    //-edited by shubham.
  { id: 4, title: "FAQs", link: "/common-faqs", active: false },
  // { id: 5, title: "Logout", link: "#", active: false },
]

export {
  AUTH_API_LOGIN,
  AUTH_API_REGISTER,
  AUTH_API_NEWUSERS,
  STUDENT_API_PREFIX,
  SUPPORT_API_PREFIX,
  ADMIN_API_PREFIX,
  FAQ_API_PREFIX,
  TICKET_API_ALLTICKETS,
  TICKET_API_ALLFAQTICKETS, // added by Harman
  TICKET_API_PREFIX,
  STUDENT_API,
  SUPPORT_API,
  ADMIN_API,
  FAQ_API,
  TICKET_API,
  STUDENT_ROUTES,
  SUPPORT_ROUTES,
  ADMIN_ROUTES,
  STUDENT_NAV_BUTTONS,
  SUPPORT_NAV_BUTTONS,
  ADMIN_NAV_BUTTONS,
  // TICKET_API_ALL_SUPPORT_TICKETS, // added by yukti
  // SUPPORT_STAFF_FLAG_API // added  by yukti
  CHAT_API, // added  by Shubham
};
