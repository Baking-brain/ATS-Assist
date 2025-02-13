import { BrowserRouter, Routes, Route } from "react-router-dom";
import Dashboard from "./components/dashboard/dashboard.jsx";
import Login from "./components/login-signup/login.jsx";
import SignupLogin from "./components/login-signup/signup.jsx";

function App() {
  return (
    <div>
      {/* <Login /> */}
      <BrowserRouter>
        <Routes>
          <Route exact path="/" element={<SignupLogin />} />
          <Route exact path="/dashboard" element={<Dashboard />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
