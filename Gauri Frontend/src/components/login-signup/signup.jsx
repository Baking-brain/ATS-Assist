import React, { useState } from "react";
import "./signup.css"; // Ensure correct path for styles

const SignupLogin = () => {
  const [isSignup, setIsSignup] = useState(true);

  const toggleForm = () => {
    setIsSignup(!isSignup);
  };

  return (
    <div className="container">
      <div className="form-box">
        <h1>{isSignup ? "Sign Up" : "Log In"}</h1>
        <form>
          <div className="input-group">
            {isSignup && (
              <div className="input-field">
                <i className="fa-solid fa-user"></i>
                <input type="text" placeholder="Name" />
              </div>
            )}

            <div className="input-field">
              <i className="fa-solid fa-envelope"></i>
              <input type="email" placeholder="Email Id" />
            </div>

            <div className="input-field">
              <i className="fa-solid fa-lock"></i>
              <input type="password" placeholder="Password" />
            </div>
          </div>
          <div className="btn-field">
            <button type="button" className={isSignup ? "" : "disable"} onClick={toggleForm}>
              Sign Up
            </button>
            <button type="button" className={!isSignup ? "" : "disable"} onClick={toggleForm}>
              Log In
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default SignupLogin;
