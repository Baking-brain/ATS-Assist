import { BrowserRouter, Routes, Route } from "react-router-dom";
import Dashboard from "./components/dashboard/dashboard.jsx";
import Login from "./components/login-signup/login.jsx";
import SignupLogin from "./components/login-signup/signup.jsx";
import SearchPage from "./components/search/search.jsx";

function App() {
  return (
    <div>
      {/* <Login /> */}
      <BrowserRouter>
        <Routes>
          <Route exact path="/" element={<SignupLogin />} />
          <Route exact path="/dashboard" element={<Dashboard />} />
          <Route exact path="/search" element={<SearchPage />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
