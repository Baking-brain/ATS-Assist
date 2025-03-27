import { BrowserRouter, Routes, Route } from "react-router-dom";
import Dashboard from "./components/dashboard/dashboard.jsx";
import SearchPage from "./components/search/SearchPage.jsx";
import LoginPage from "./components/login-signup/LoginPage.jsx";
import NavBar from "./components/dashboard/nav-bar.jsx";
import ProfilePage from "./components/profile/CreateProfile.jsx";
import { useState } from "react";

function App() {
  const [profile, setProfile] = useState({ username: "Default Username" });

  return (
    <div>
      {/* <Login /> */}
      <BrowserRouter>
        <NavBar setProfile={setProfile} profile={profile} />
        <Routes>
          <Route
            exact
            path="/"
            element={<LoginPage setProfile={setProfile} />}
          />
          <Route exact path="/dashboard" element={<Dashboard />} />
          <Route exact path="/search" element={<SearchPage />} />
          <Route exact path="/profile" element={<ProfilePage />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
