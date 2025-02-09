import { useState } from "react";
import "./nav-bar.css";
import { useNavigate } from "react-router-dom";
import axios from "axios";

export default function NavBar({ username = "default username" }) {
  const [isOpen, setIsOpen] = useState(false);
  const navigate = useNavigate();

  async function handleLogout() {
    await axios
      .get("/api/logout")
      .then((response) => {
        console.log(response.data);
        navigate("/");
      })
      .catch((error) => {});
  }

  return (
    <nav className="navbar">
      <div className="navbar-logo"></div>
      <div className="navbar-search"></div>
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
