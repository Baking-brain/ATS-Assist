import { useEffect, useState } from "react";
import "./content-block.css";
import { Check, SquarePlus, SquareX } from "lucide-react";

export default function ContentBlock({
  buttons = false,
  aiInsight = null,
  suggestedSkills = null,
  toAddSkills = null,
  getAiInsight = () => {},
  suggestSkills = () => {},
  addToToAdd = () => {},
  removeFromToAdd = () => {},
  updateProfile = () => {},
}) {
  //   const text_output = ` 🔹 Skills & Experience Relevance: 8/10
  // Abhimanyu has showcased a strong set of technical skills that align well with the job requirements for a data science role. His past experiences, such as the ATS Assist and Property Price Prediction projects, demonstrate his proficiency in data analysis, machine learning, and natural language processing. To improve, Abhimanyu could provide more details on how his projects and experiences have had a professional impact.

  // ⚡ Suggested Improvements:

  // 1. Include specific examples of how the projects or experiences have made an impact, such as the number of users, percentage increase in accuracy, or any other relevant metrics.
  // 2. Tailor the skills section to the specific job description, highlighting the most relevant skills first.

  // 🔹 Education & Certifications: 7/10
  // Abhimanyu's educational background in Computer Science and Engineering with a focus on Data Science is relevant to the role. However, the GPA could be more prominently displayed, and the certifications could benefit from a brief description of what was learned or achieved.

  // ⚡ Suggested Improvements:

  // 1. Make the GPA more visible by including it in the main education section instead of a parenthesis.
  // 2. Add a short description of the certifications, explaining what was learned or accomplished.

  // 🔹 Achievement Impact: 6/10
  // While Abhimanyu has listed several achievements, they could benefit from more quantifiable data to demonstrate the impact. Adding specific metrics or percentages would strengthen the resume.

  // ⚡ Suggested Improvements:

  // 1. Include quantifiable data for achievements, such as the number of participants in the Hackathons, rankings, or any other relevant metrics.
  // 2. Provide context for non-technical achievements, like how the district-level camp for disaster management contributed to the community.

  // 🔹 Resume Structure & Presentation: 8/10
  // The resume is generally well-organized and easy to read. However, there is room for improvement in terms of consistency in formatting and headings.

  // ⚡ Suggested Improvements:

  // 1. Standardize the format for headings and bullet points throughout the resume.
  // 2. Use consistent spacing and indentation for bullet points.

  // 🔹 Grammar & Clarity: 8/10
  // Abhimanyu's resume is mostly clear and free of grammar errors. However, there are a few minor issues that could be improved.

  // ✍️ Feedback:
  // ✅ Identified grammar/spelling issues

  // - In the "Email Client with user authentication (Developing)" project, replace "for a smooth backend" with "for a smooth back-end."
  // - In the "Achievements/Activities" section, replace "Hackwave- Participated" with "Hackwave: Participated."

  // ⚡ Suggested fixes:

  // 1. Review the resume for consistency in capitalization and punctuation.
  // 2. Double-check for any spelling errors or awkward phrasing.

  // ---

  // 📊 Total Score: 37/50
  // 📈 Match Percentage: 74%
  // ✅ Final Recommendation: Shortlist`;

  useEffect(() => {
    function getScores() {
      if (!aiInsight) return;
      let scorearr = [];

      aiInsight.split("\n").forEach((chunk) => {
        chunk = chunk.trim();
        if (
          (chunk.includes("&") && chunk.includes(":") && chunk.includes("/")) ||
          (chunk.includes("Achievement Impact") &&
            chunk.includes(":") &&
            chunk.includes("/"))
        ) {
          chunk = chunk.split(" ");
          scorearr.push(Number(chunk[chunk.length - 1].split("/")[0]));
        }
      });

      console.log("Score arr: ", scorearr);
    }
    getScores();
  }, [aiInsight]);

  return (
    <div className="content-block">
      <div className={`content-box ${buttons ? "square" : "full-height"}`}>
        {aiInsight && (
          <div>
            {aiInsight.split("\n").map((chunk) => {
              if (!chunk) return <br />;
              return <div>{chunk}</div>;
            })}
          </div>
        )}
        {/* {buttons || (
          <div>
            {text_output.split("\n").map((chunk) => {
              if (!chunk) return <br />;
              return <div>{chunk}</div>;
            })}
          </div>
        )} */}
        {suggestedSkills?.length > 0 && (
          <div className="tag-container">
            <h2>Suggested Keywords</h2>
            {suggestedSkills.map((skill) => {
              return (
                <div className="skill-tag">
                  <h3>{skill}</h3>
                  <div
                    className="add-btn"
                    onClick={() => {
                      addToToAdd(skill);
                    }}
                  >
                    <SquarePlus
                      size={28}
                      style={{ color: "green", padding: "0px" }}
                    />
                  </div>
                </div>
              );
            })}
          </div>
        )}
        {toAddSkills?.length > 0 && (
          <div className="tag-container">
            <h2>Add To Profile</h2>
            {toAddSkills.map((skill) => {
              return (
                <div className="skill-tag">
                  <h3>{skill}</h3>
                  <div
                    className="add-btn"
                    onClick={() => {
                      removeFromToAdd(skill);
                    }}
                  >
                    <SquareX
                      size={28}
                      style={{ color: "rgb(255, 71, 71)", padding: "0px" }}
                    />
                  </div>
                  {/* <button></button> */}
                </div>
              );
            })}
            <button className="confirm-to-add" onClick={updateProfile}>
              Add To Profile
            </button>
          </div>
        )}
      </div>
      {buttons && (
        <div className="button-container">
          {/* <button className="content-button">Grammar</button> */}
          <button className="content-button" onClick={getAiInsight}>
            AI Insights
          </button>
          <button className="content-button" onClick={suggestSkills}>
            Suggest Skills
          </button>
        </div>
      )}
    </div>
  );
}
