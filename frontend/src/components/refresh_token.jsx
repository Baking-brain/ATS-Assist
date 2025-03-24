import axios from "axios";

export default async function getRefreshToken() {
  await axios
    .get("/api/refresh_token")
    .then((response) => {
      console.log(response, "New Token Assigned");
      //   alert("New token assigned");
    })
    .catch((error) => {
      console.log("Refresh token error: ", error);
      // alert(error.response.data.detail);
      throw new Error(error.response.data.detail);
    });
}
