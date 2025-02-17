import "./dashboard.css";
import NavBar from "./nav-bar.jsx";
import ResumeUpload from "./resume-upload.jsx";
import ContentBlock from "./content-block.jsx";
import { useEffect, useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import getRefreshToken from "../refresh_token.jsx";

export default function Dashboard() {
  const [profile, setProfile] = useState({ username: "Default Username" });
  const navigate = useNavigate();

  useEffect(() => {
    async function get_profile() {
      await axios
        .get("/api/get_profile")
        .then((response) => {
          console.log(response);
          setProfile(response.data.Profile);
        })
        .catch((error) => {
          const errMsg = error.response.data.detail;
          console.log("Error: ", error, errMsg);

          //If cookies not set
          if (errMsg.includes("not provided")) {
            alert("Session expired, please login again");
            navigate("/");
            return;
          }

          //If access token expired
          if (errMsg.includes("invalid or expired")) {
            const refreshTokenMsg = getRefreshToken();

            //If refresh token expired
            if (refreshTokenMsg == "Refresh token expired") {
              alert("Session expired, please login again");
              navigate("/");
              return;
            }
          }
        });
    }

    get_profile();
  }, []);

  // if (!profile.username) {
  //   return <h1>Loading...</h1>;
  // }

  return (
    <div className="dashboard">
      <NavBar username={profile.username} />
      <ResumeUpload />
      <main className="container">
        <div className="grid">
          <ContentBlock />
          <ContentBlock buttons />
        </div>
      </main>
    </div>
  );
}
