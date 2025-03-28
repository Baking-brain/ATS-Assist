import { BrowserRouter, Routes, Route } from "react-router-dom";
import Dashboard from "./components/dashboard/dashboard.jsx";
import SearchPage from "./components/search/SearchPage.jsx";
import LoginPage from "./components/login-signup/LoginPage.jsx";
import NavBar from "./components/dashboard/nav-bar.jsx";
import ProfilePage from "./components/profile/ProfilePage.jsx";
import { useState } from "react";

function App() {
  const [profile, setProfile] = useState({
    name: "John Doe",
    username: "johndoe",
    email: "john.doe@example.com",
    location: "San Francisco, CA",
    about:
      "I'm a passionate frontend developer with 5+ years of experience building modern web applications. I specialize in React, TypeScript, and modern JavaScript frameworks. I enjoy creating intuitive user interfaces and solving complex problems.",
    experience: 4.0,
    education: "PHD",
    skills: [
      "Redux",
      "Next.js",
      "GraphQL",
      "Webpack",
      "Jest",
      "Git",
      "RESTful APIs",
      "Responsive Design",
      "Sass/SCSS",
      "Tailwind CSS",
    ],
  });

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
          <Route
            exact
            path="/profile"
            element={<ProfilePage setProfile={setProfile} profile={profile} />}
          />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
