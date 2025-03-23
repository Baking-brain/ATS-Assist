import { useEffect, useState } from "react";
import "./nav-bar.css";
import { useLocation, useNavigate } from "react-router-dom";
import axios from "axios";
import { ChevronDown } from "lucide-react";
import getRefreshToken from "../refresh_token";
const isDevelopment = import.meta.env.VITE_IS_DEVELOPMENT === "true";

export default function NavBar({ username = "default username" }) {
  const [isOpen, setIsOpen] = useState(false);
  const [profile, setProfile] = useState({ username: "Default Username" });
  const navigate = useNavigate();
  const location = useLocation();

  async function handleLogout() {
    await axios
      .get("/api/logout")
      .then((response) => {
        console.log(response.data);
        navigate("/");
      })
      .catch((error) => {
        console.log("Error => ", error);
      });
  }

  //Get profile details upon login
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

    if (!isDevelopment) {
      get_profile();
    }
  }, []);

  if (location.pathname === "/") {
    return <nav className="navbar"></nav>;
  }

  return (
    <nav className="navbar">
      <div className="navbar-logo"></div>

      <div className="navbar-pages-con">
        <h4
          onClick={() => {
            navigate("/dashboard");
          }}
        >
          Home
        </h4>
        <h4
          onClick={() => {
            navigate("/search");
          }}
        >
          Search
        </h4>
      </div>

      <div className="navbar-profile" onClick={() => setIsOpen(!isOpen)}>
        <div className="navbar-profile-closed">
          <button className="navbar-profile-button" />
          <h3>{username}</h3>
          <ChevronDown />
        </div>
        {isOpen && (
          <div className="navbar-dropdown">
            <p>Edit Profile</p>
            <p onClick={handleLogout}>Log Out</p>
          </div>
        )}
      </div>
    </nav>
  );

  return (
    <nav className="navbar">
      <div className="navbar-logo"></div>
      <div>
        <input className="navbar-search" />
        <button
          onClick={() => {
            navigate("/search");
          }}
        >
          Search
        </button>
      </div>
      {/* <div className="navbar-search"></div> */}
      <div className="navbar-profile">
        <button
          onClick={() => setIsOpen(!isOpen)}
          className="navbar-profile-button"
        />
        {isOpen && (
          <div className="navbar-dropdown">
            <p>{username}</p>
            <a href="#">Edit Profile</a>
            <p onClick={handleLogout}>Log Out</p>
          </div>
        )}
      </div>
    </nav>
  );
}
