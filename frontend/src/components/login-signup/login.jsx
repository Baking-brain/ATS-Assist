import React from "react";
import "./login.css"; // Ensure correct path for styles

const Login = () => {
  return (
    <div className="container">
      <div className="form-box">
        <h1>Log In</h1>
        <form>
          <div className="input-group">
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
            <button type="submit">Log In</button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default Login;
