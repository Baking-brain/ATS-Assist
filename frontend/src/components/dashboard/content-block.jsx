import { useState } from "react";
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
  return (
    <div className="content-block">
      <div className={`content-box ${buttons ? "square" : "full-height"}`}>
        {aiInsight && <p className="ai-insight-display">{aiInsight}</p>}
        {suggestedSkills?.length && (
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
                  {/* <button></button> */}
                </div>
              );
            })}
          </div>
        )}
        {toAddSkills?.length && (
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
