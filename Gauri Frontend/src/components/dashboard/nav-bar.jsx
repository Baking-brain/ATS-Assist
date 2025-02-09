import { useState } from "react";
import "./nav-bar.css"; 

export default function NavBar() {
  const [isOpen, setIsOpen] = useState(false);

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
            <p>User Name</p>
            <a href="#">Edit Profile</a>
          </div>
        )}
      </div>
    </nav>
  );
}
