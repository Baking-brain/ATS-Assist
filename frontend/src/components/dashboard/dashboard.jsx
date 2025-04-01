import "./dashboard.css";
import ResumeUpload from "./resume-upload.jsx";
import ContentBlock from "./content-block.jsx";
import { useEffect, useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import getRefreshToken from "../refresh_token.jsx";
const isDevelopment = import.meta.env.VITE_IS_DEVELOPMENT === "true";

export default function Dashboard({ setProfile, profile }) {
  // const [profile, setProfile] = useState({ username: "Default Username" });
  const [aiInsight, setAiInsight] = useState(null);
  const [suggestedSkills, setSuggestedSkills] = useState([]);
  const [toAddSkills, setToAddSkills] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();

  async function getAiInsight() {
    if (isDevelopment) return;
    setIsLoading(true);

    try {
      const getAiInsightResponse = await axios.get(
        "/api/file_upload?action_type=ai_insights"
      );
      console.log("Ai Insight Response: ", getAiInsightResponse);
      setAiInsight(getAiInsightResponse.data.ai_insight);
      setSuggestedSkills([]);
      setToAddSkills([]);
    } catch (error) {
      console.log("AI Insight Error: ", error);
    } finally {
      setIsLoading(false);
    }
  }

  async function suggestSkills() {
    if (isDevelopment) return;
    setIsLoading(true);
    setToAddSkills([]);

    try {
      const suggestSkillsResponse = await axios.get(
        "/api/file_upload?action_type=suggest_skills"
      );
      console.log("Suggest Skills Response: ", suggestSkillsResponse);
      setSuggestedSkills(suggestSkillsResponse.data.suggest_skills);
      setAiInsight(null);
    } catch (error) {
      console.log("Suggest Skills Error: ", error);
    } finally {
      setIsLoading(false);
    }
  }

  async function updateProfile() {
    if (isDevelopment) return;
    setIsLoading(true);

    let tempProfileSkills = profile.skills;
    for (let toAddSkill of toAddSkills) {
      if (!tempProfileSkills.includes(toAddSkill.trim().toLowerCase())) {
        tempProfileSkills.push(toAddSkill.trim().toLowerCase());
      }
    }

    // console.log("New Profile Skills: ", tempProfileSkills);
    profile.skills = tempProfileSkills;
    setProfile((prev) => ({ ...prev, skills: tempProfileSkills }));

    try {
      const updateProfileResponse = await axios.post(
        "/api/update_applicant_profile",
        profile
      );
      console.log("Update Profile Response: ", updateProfileResponse);
    } catch (error) {
      console.log("Suggest Skills Error: ", error);
    } finally {
      setIsLoading(false);
    }
  }

  function addToToAdd(skill) {
    let tempSuggestions = suggestedSkills.filter((skillIter) => {
      return skillIter !== skill;
    });
    setSuggestedSkills(tempSuggestions);
    setToAddSkills([...toAddSkills, skill]);
  }

  function removeFromToAdd(skill) {
    let tempSuggestions = toAddSkills.filter((skillIter) => {
      return skillIter !== skill;
    });
    setToAddSkills(tempSuggestions);
    setSuggestedSkills([...suggestedSkills, skill]);
  }

  // //Get profile details upon login
  // useEffect(() => {
  //   async function get_profile() {
  //     await axios
  //       .get("/api/get_profile")
  //       .then((response) => {
  //         console.log(response);
  //         setProfile(response.data.Profile);
  //       })
  //       .catch((error) => {
  //         const errMsg = error.response.data.detail;
  //         console.log("Error: ", error, errMsg);

  //         //If cookies not set
  //         if (errMsg.includes("not provided")) {
  //           alert("Session expired, please login again");
  //           navigate("/");
  //           return;
  //         }

  //         //If access token expired
  //         if (errMsg.includes("invalid or expired")) {
  //           const refreshTokenMsg = getRefreshToken();

  //           //If refresh token expired
  //           if (refreshTokenMsg == "Refresh token expired") {
  //             alert("Session expired, please login again");
  //             navigate("/");
  //             return;
  //           }
  //         }
  //       });
  //   }

  //   if (!isDevelopment) {
  //     get_profile();
  //   }
  // }, []);

  if (isLoading) {
    return (
      <div id="dashboard">
        <div className="loading-container">
          <div className="loading-spinner"></div>
          <p>Fetching Results...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="dashboard">
      {/* <NavBar username={profile.username} /> */}
      <ResumeUpload />
      <main className="container">
        <div className="grid">
          <ContentBlock
            buttons
            getAiInsight={getAiInsight}
            suggestSkills={suggestSkills}
          />
          <ContentBlock
            aiInsight={aiInsight}
            suggestedSkills={suggestedSkills}
            toAddSkills={toAddSkills}
            addToToAdd={addToToAdd}
            removeFromToAdd={removeFromToAdd}
            updateProfile={updateProfile}
          />
        </div>
      </main>
    </div>
  );
}
