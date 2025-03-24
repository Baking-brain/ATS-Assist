import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./LoginPage.css";
import { Lock, User, User2 } from "lucide-react";
import axios from "axios";

export default function LoginSignup() {
  const [isLoginActive, setIsLoginActive] = useState(true);
  const [loginUsername, setLoginUsername] = useState("");
  const [loginPassword, setLoginPassword] = useState("");
  const [signupName, setSignupName] = useState("");
  const [signupUsername, setSignupUsername] = useState("");
  const [signupPassword, setSignupPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");
  const navigate = useNavigate();

  const toggleForm = () => {
    setIsLoginActive(!isLoginActive);
    setErrorMessage("");
  };

  async function handleLogin(e) {
    e.preventDefault();
    setIsLoading(true);

    // Simulate login process
    await axios
      .post("/api/login", {
        username: loginUsername,
        password: loginPassword,
      })
      .then((response) => {
        console.log(response.data);
        setIsLoading(false);
        navigate("/dashboard");
      })
      .catch((error) => {
        console.error(error.response.data);
        setLoginUsername("");
        setLoginPassword("");
        setIsLoading(false);
        setErrorMessage(error.response.data.status);
      });
  }

  const handleSignup = (e) => {
    e.preventDefault();
    setIsLoading(true);
    setErrorMessage("");

    // Password validation
    if (signupPassword !== confirmPassword) {
      setErrorMessage("Passwords don't match");
      setIsLoading(false);
      return;
    }

    // Simulate signup process
    console.log("Signup Clicked");
  };

  return (
    <div className="auth-container">
      <div className="auth-card">
        <div className="auth-header">
          <h1>ATS-Assist</h1>
          <p>Analyse and improve your resume</p>
        </div>

        <div className="auth-tabs">
          <button
            className={`auth-tab ${isLoginActive ? "active" : ""}`}
            onClick={() => setIsLoginActive(true)}
          >
            Login
          </button>
          <button
            className={`auth-tab ${!isLoginActive ? "active" : ""}`}
            onClick={() => setIsLoginActive(false)}
          >
            Sign Up
          </button>
        </div>

        {errorMessage && <div className="auth-error">{errorMessage}</div>}

        {isLoginActive ? (
          <form className="auth-form" onSubmit={handleLogin}>
            <div className="form-group">
              <label htmlFor="login-username">Username</label>
              <div className="input-icon">
                <span className="input-icon-wrapper">
                  <User />
                </span>
                <input
                  id="login-username"
                  type="text"
                  value={loginUsername}
                  onChange={(e) => setLoginUsername(e.target.value)}
                  placeholder="Enter your username"
                  required
                />
              </div>
            </div>

            <div className="form-group">
              <label htmlFor="login-password">Password</label>
              <div className="input-icon">
                <span className="input-icon-wrapper">
                  <Lock />
                </span>
                <input
                  id="login-password"
                  type="password"
                  value={loginPassword}
                  onChange={(e) => setLoginPassword(e.target.value)}
                  placeholder="Enter your password"
                  required
                />
              </div>
            </div>

            {/* <div className="forgot-password">
              <a href="#">Forgot Password?</a>
            </div> */}

            <button type="submit" className="auth-button" disabled={isLoading}>
              {isLoading ? <span className="loading-spinner"></span> : "Login"}
            </button>
          </form>
        ) : (
          <form className="auth-form" onSubmit={handleSignup}>
            <div className="form-group">
              <label htmlFor="signup-name">Full Name</label>
              <div className="input-icon">
                <span className="input-icon-wrapper">
                  <User />
                </span>
                <input
                  id="signup-name"
                  type="text"
                  value={signupName}
                  onChange={(e) => setSignupName(e.target.value)}
                  placeholder="Enter your full name"
                  required
                />
              </div>
            </div>

            <div className="form-group">
              <label htmlFor="signup-username">Username</label>
              <div className="input-icon">
                <span className="input-icon-wrapper">
                  <User />
                </span>
                <input
                  id="signup-username"
                  type="text"
                  value={signupUsername}
                  onChange={(e) => setSignupUsername(e.target.value)}
                  placeholder="Enter your username"
                  required
                />
              </div>
            </div>

            <div className="form-group">
              <label htmlFor="signup-password">Password</label>
              <div className="input-icon">
                <span className="input-icon-wrapper">
                  <Lock />
                </span>
                <input
                  id="signup-password"
                  type="password"
                  value={signupPassword}
                  onChange={(e) => setSignupPassword(e.target.value)}
                  placeholder="Create a password"
                  required
                />
              </div>
            </div>

            <div className="form-group">
              <label htmlFor="confirm-password">Confirm Password</label>
              <div className="input-icon">
                <span className="input-icon-wrapper">
                  <Lock />
                </span>
                <input
                  id="confirm-password"
                  type="password"
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                  placeholder="Confirm your password"
                  required
                />
              </div>
            </div>

            <button type="submit" className="auth-button" disabled={isLoading}>
              {isLoading ? (
                <span className="loading-spinner"></span>
              ) : (
                "Sign Up"
              )}
            </button>
          </form>
        )}

        <div className="auth-footer">
          {isLoginActive ? (
            <p>
              Don't have an account?{" "}
              <button className="toggle-link" onClick={toggleForm}>
                Sign up
              </button>
            </p>
          ) : (
            <p>
              Already have an account?{" "}
              <button className="toggle-link" onClick={toggleForm}>
                Login
              </button>
            </p>
          )}
        </div>
      </div>
    </div>
  );
}
