import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import "./signup.css"; // Ensure correct path for styles

const SignupLogin = () => {
  const [isSignup, setIsSignup] = useState(false);
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [cnfpassword, setCnfPassword] = useState("");
  const [errorMsg, setErrorMsg] = useState("");
  const [isValidPassword, setIsValidPassword] = useState(false);
  const navigate = useNavigate();

  const toggleForm = () => {
    setUsername("");
    setPassword("");
    setCnfPassword("");
    setIsSignup(!isSignup);
  };

  async function handleSignup() {
    if (!(password == cnfpassword)) {
      alert("Passwords do not match");
      return;
    }
    await axios
      .post("/api/create_applicant", { username: username, password: password })
      .then((response) => {
        console.log("Success: ", response);
        alert("Signup Successfull");
        toggleForm();
      })
      .catch((error) => {
        console.log("Error: ", error);
      });
  }
  async function handleLogin() {
    await axios
      .post("/api/login", { username: username, password: password })
      .then((response) => {
        console.log(response.data);
        navigate("/dashboard");
      })
      .catch((error) => {
        const errMsg = error.response.statusText;
        console.log(errMsg);
        if (errMsg == "Unauthorized") {
          alert("Username or Password Wrong");
          setUsername("");
          setPassword("");
          setCnfPassword("");
          return;
        }
      });
  }

  function validatePassword() {
    if (!password) {
      setErrorMsg("");
      setIsValidPassword(false);
      return;
    }

    if (password.length < 8) {
      setErrorMsg("Password must have 8 characters");
      setIsValidPassword(false);
      return;
    }

    const regx = /([!-/]|[:-@])/;
    const regx2 = /[\d]/;
    if (!regx.test(password)) {
      setErrorMsg("Password must have special characters");
      setIsValidPassword(false);
      return;
    }
    if (!regx2.test(password)) {
      setErrorMsg("Password must have numeric characters");
      setIsValidPassword(false);
      return;
    }
    if (password !== cnfpassword) {
      setErrorMsg("Password do not match");
      setIsValidPassword(false);
      return;
    }
    setErrorMsg("");
    setIsValidPassword(true);

    setErrorMsg("");
    setIsValidPassword(true);
  }

  useEffect(() => {
    validatePassword();
  }, [password, cnfpassword]);

  return (
    <div className="container">
      <div className="form-box">
        <div className="btn-field">
          <button
            type="button"
            className={isSignup ? "" : "disable"}
            onClick={toggleForm}
          >
            Sign Up
          </button>
          <button
            type="button"
            className={!isSignup ? "" : "disable"}
            onClick={toggleForm}
          >
            Log In
          </button>
        </div>
        {/* <h1>{isSignup ? "Sign Up" : "Log In"}</h1> */}
        <form>
          <div className="input-group">
            <div className="input-field">
              <i className="fa-solid fa-envelope"></i>
              <input
                type="text"
                placeholder="Username"
                value={username}
                onChange={(e) => {
                  setUsername(e.target.value);
                }}
              />
            </div>

            <div className="input-field">
              <i className="fa-solid fa-lock"></i>
              <input
                type="password"
                placeholder="Password"
                value={password}
                onChange={(e) => {
                  setPassword(e.target.value);
                  // validatePassword();
                }}
              />
            </div>

            {isSignup && (
              <div className="input-field">
                <i className="fa-solid fa-user"></i>
                <input
                  type="password"
                  placeholder="Confirm Password"
                  value={cnfpassword}
                  onChange={(e) => {
                    setCnfPassword(e.target.value);
                    // validatePassword();
                  }}
                />
              </div>
            )}

            {isSignup && <div className="error-msg">{errorMsg}</div>}
          </div>
          <div className="btn-field">
            {isSignup ? (
              <button
                type="button"
                onClick={handleSignup}
                className={
                  !(username && password && cnfpassword && isValidPassword)
                    ? "disable"
                    : ""
                }
                disabled={
                  !(username && password && cnfpassword && isValidPassword)
                }
              >
                Sign Up
              </button>
            ) : (
              <button
                type="button"
                onClick={handleLogin}
                className={!(username && password) ? "disable" : ""}
                disabled={!(username && password)}
              >
                Log In
              </button>
            )}
          </div>
        </form>
      </div>
    </div>
  );
};

export default SignupLogin;
