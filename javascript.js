const axios = require("axios");
const url = "http://api.proomptify.com/generate";
const headers = {"Content-Type": "application/json", "Authorization": "Bearer YOUR_API_KEY"};
const data = {text: "Generate content using Proomptify."};

axios.post(url, data, {headers}).then(response => console.log(response.data)).catch(error => console.error(error));
