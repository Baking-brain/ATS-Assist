import axios from "axios";

export default async function getRefreshToken() {
  await axios
    .get("/api/refresh_token")
    .then((response) => {
      console.log(response, "New Token Assigned");
      //   alert("New token assigned");
    })
    .catch((error) => {
      console.log("Error: ", error);
      alert(error.response.data.detail);
      return error.response.data.detail;
    });
}
