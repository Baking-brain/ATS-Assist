import { useEffect, useState } from "react";
import "./nav-bar.css";
import { useLocation, useNavigate } from "react-router-dom";
import axios from "axios";
import { ChevronDown } from "lucide-react";
import getRefreshToken from "../refresh_token";
const isDevelopment = import.meta.env.VITE_IS_DEVELOPMENT === "true";

export default function NavBar({ setProfile, profile }) {
  const [isOpen, setIsOpen] = useState(false);

  const navigate = useNavigate();
  const location = useLocation();

  async function handleLogout() {
    const confirmation = window.confirm("Are you sure");
    if (!confirmation) return;

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
      try {
        const profileResponse = await axios.get("/api/get_profile");
        console.log("Navbar profile fetch: ", profileResponse);
        setProfile(profileResponse.data.Profile);
      } catch (profileFetchError) {
        const errMsg = profileFetchError.response.data.detail;
        console.log("Profile fetch error: ", profileFetchError, errMsg);

        //If cookies not set
        if (errMsg.includes("not provided")) {
          alert("Session not started, please login again");
          navigate("/");
          return;
        }

        // console.log(
        //   "Entering access token expired block. Boolean value: ",
        //   errMsg.includes("invalid or expired")
        // );

        //If access token expired
        if (errMsg.includes("invalid or expired")) {
          // console.log("Making new access token request");

          try {
            const refreshTokenMsg = await getRefreshToken();
          } catch (refreshError) {
            console.log("Refresh error: ", refreshError);

            //If refresh token expired
            if (refreshError.message == "Refresh token expired") {
              alert("Session expired, please login again");
              navigate("/");
              return;
            }
          }
        }
      }
      // await axios
      //   .get("/api/get_profile")
      //   .then((response) => {
      //     console.log(response);
      //     setProfile(response.data.Profile);
      //   })
      //   .catch((error) => {
      //     const errMsg = error.response.data.detail;
      //     console.log("Profile fetch error: ", error, errMsg);

      //     //If cookies not set
      //     if (errMsg.includes("not provided")) {
      //       alert("Session not started, please login again");
      //       navigate("/");
      //       return;
      //     }

      //     console.log(
      //       "Entering access token expired block. Boolean value: ",
      //       errMsg.includes("invalid or expired")
      //     );

      //     //If access token expired
      //     if (errMsg.includes("invalid or expired")) {
      //       console.log("Making new access token request");

      //       const refreshTokenMsg = getRefreshToken();

      //       console.log(
      //         "Refresh token expired. Boolean value: ",
      //         refreshTokenMsg == "Refresh token expired",
      //         refreshTokenMsg
      //       );

      //       //If refresh token expired
      //       if (refreshTokenMsg == "Refresh token expired") {
      //         alert("Session expired, please login again");
      //         navigate("/");
      //         return;
      //       }
      //     }
      //   });
    }

    if (!isDevelopment && location.pathname !== "/") {
      get_profile();
    }
  }, [location.pathname]);

  if (location.pathname === "/") {
    return <nav className="navbar"></nav>;
  }

  return (
    <nav className="navbar">
      {/* <div className="navbar-logo"></div> */}

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

      <div
        tabIndex={0}
        className="navbar-profile"
        onClick={() => setIsOpen(!isOpen)}
        onBlur={() => {
          setIsOpen(false);
        }}
      >
        <div className="navbar-profile-closed">
          <div className="navbar-profile-button">
            <p>
              {profile.name
                .split(" ")
                .map((name) => {
                  return name[0];
                })
                .join("")}
            </p>
          </div>
          <h3>{profile.username}</h3>
          <ChevronDown />
        </div>
        {isOpen && (
          <div className="navbar-dropdown">
            <p
              onClick={() => {
                navigate("/profile");
              }}
            >
              Edit Profile
            </p>
            <p onClick={handleLogout}>Log Out</p>
          </div>
        )}
      </div>
    </nav>
  );
}
