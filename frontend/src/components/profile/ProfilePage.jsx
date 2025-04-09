import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./ProfilePage.css";
import {
  CalendarClock,
  DoorOpen,
  GraduationCap,
  Hourglass,
  LockKeyhole,
  Mail,
  MapPin,
} from "lucide-react";
import axios from "axios";
const isDevelopment = import.meta.env.VITE_IS_DEVELOPMENT === "true";

export default function ProfilePage({ profile, setProfile }) {
  const navigate = useNavigate();
  const [isEditing, setIsEditing] = useState(false);
  //   const [profile, setProfile] = useState(profileProp);
  //   const profile = profileProp;

  const [activeTab, setActiveTab] = useState("about");
  const [newSkill, setNewSkill] = useState("");
  //   const [newSkillLevel, setNewSkillLevel] = useState(50);
  //   const [newAdditionalSkill, setNewAdditionalSkill] = useState("");

  // New experience form state
  //   const [newExperience, setNewExperience] = useState({
  //     title: "",
  //     company: "",
  //     dates: "",
  //     location: "",
  //     description: "",
  //   });

  //   // New education form state
  //   const [newEducation, setNewEducation] = useState({
  //     degree: "",
  //     school: "",
  //     dates: "",
  //     description: "",
  //   });

  const handleInputChange = (e, section, index, field) => {
    const value = e.target.value;

    if (section === "profile") {
      if (field === "name") {
        setProfile({ ...profile, [field]: value.trimStart() });
        return;
      }
      setProfile({ ...profile, [field]: value });
    }
    // else if (section === "experience") {
    //   const updatedExperience = [...profile.experience];
    //   updatedExperience[index] = {
    //     ...updatedExperience[index],
    //     [field]: value,
    //   };
    //   setProfile({ ...profile, experience: updatedExperience });
    // } else if (section === "education") {
    //   const updatedEducation = [...profile.education];
    //   updatedEducation[index] = { ...updatedEducation[index], [field]: value };
    //   setProfile({ ...profile, education: updatedEducation });
    // } else if (section === "newExperience") {
    //   setNewExperience({ ...newExperience, [field]: value });
    // } else if (section === "newEducation") {
    //   setNewEducation({ ...newEducation, [field]: value });
    // }
  };

  //   const handleAddExperience = () => {
  //     if (newExperience.title && newExperience.company) {
  //       setProfile({
  //         ...profile,
  //         experience: [...profile.experience, newExperience],
  //       });
  //       setNewExperience({
  //         title: "",
  //         company: "",
  //         dates: "",
  //         location: "",
  //         description: "",
  //       });
  //     }
  //   };

  //   const handleAddEducation = () => {
  //     if (newEducation.degree && newEducation.school) {
  //       setProfile({
  //         ...profile,
  //         education: [...profile.education, newEducation],
  //       });
  //       setNewEducation({
  //         degree: "",
  //         school: "",
  //         dates: "",
  //         description: "",
  //       });
  //     }
  //   };

  //   const handleRemoveExperience = (index) => {
  //     const updatedExperience = [...profile.experience];
  //     updatedExperience.splice(index, 1);
  //     setProfile({ ...profile, experience: updatedExperience });
  //   };

  //   const handleRemoveEducation = (index) => {
  //     const updatedEducation = [...profile.education];
  //     updatedEducation.splice(index, 1);
  //     setProfile({ ...profile, education: updatedEducation });
  //   };

  //   const handleAddSkill = () => {
  //     if (newSkill.trim()) {
  //       setProfile({
  //         ...profile,
  //         skills: [...profile.skills, { name: newSkill, level: newSkillLevel }],
  //       });
  //       setNewSkill("");
  //       setNewSkillLevel(50);
  //     }
  //   };

  //   const handleRemoveSkill = (index) => {
  //     const updatedSkills = [...profile.skills];
  //     updatedSkills.splice(index, 1);
  //     setProfile({ ...profile, skills: updatedSkills });
  //   };

  function addNewSkill() {
    const tempNewSkill = newSkill.trim().toLowerCase();
    setNewSkill("");
    if (profile.skills.includes(tempNewSkill)) return;

    setProfile((prev) => ({
      ...prev,
      skills: [...prev.skills, tempNewSkill],
    }));
  }

  function removeSkill(remSkill) {
    let tempSkills = profile.skills.filter((skillIter) => {
      return skillIter.trim().toLowerCase() !== remSkill;
    });
    setProfile((prev) => ({
      ...prev,
      skills: tempSkills,
    }));
  }

  async function updateProfile() {
    const confirmation = window.confirm("Are you sure?");
    if (!confirmation) return;

    if (
      !/^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/.test(profile.email)
    ) {
      alert("Email not valid...");
      return;
    }

    if (isDevelopment) return;

    try {
      const updateProfileResponse = await axios.post(
        "/api/update_applicant_profile",
        profile
      );
      console.log(
        "Update Profile Response from profile page: ",
        updateProfileResponse
      );
    } catch (error) {
      console.log("Update Profile Error: ", error);
    } finally {
      setIsEditing(false);
    }
  }

  // const handleSaveProfile = async () => {
  //   const confirmation = window.confirm("Are you sure");
  //   if (!confirmation) return;
  //   console.log("Saving profile:", profile);

  //   setIsEditing(false);
  //   // alert("Profile updated successfully!");
  // };

  async function handleLogout() {
    const confirmation = window.confirm("Are you sure");
    if (!confirmation) return;

    await axios
      .get("/api/logout")
      .then((response) => {
        console.log(response.data);
        navigate("/");
      })
      .catch((error) => {
        console.log("Error => ", error);
      });
  }

  return (
    <div className="profile-page">
      <div className="profile-container">
        <div className="profile-main">
          <div className="profile-card">
            <div className="profile-cover">
              <button
                className={`profile-button ${
                  isEditing ? "save-button" : "edit-button"
                }`}
                onClick={() =>
                  isEditing ? updateProfile() : setIsEditing(true)
                }
              >
                {isEditing ? "Save Changes" : "Edit Profile"}
              </button>
            </div>
            <div className="profile-info-container">
              <div className="profile-avatar">
                <div className="avatar-placeholder">
                  {profile.name
                    .split(" ")
                    .map((name, index) => {
                      if (index < 2 && name.trim())
                        return name[0].toUpperCase();
                    })
                    .join("")}
                </div>
              </div>

              <div className="profile-info">
                {isEditing ? (
                  <div className="edit-fields">
                    <div className="field-group">
                      <label>Name:</label>
                      <input
                        type="text"
                        value={profile.name}
                        onChange={(e) =>
                          handleInputChange(e, "profile", null, "name")
                        }
                      />
                    </div>

                    <div className="field-group">
                      <label>Email:</label>
                      <input
                        type="email"
                        value={profile.email}
                        onChange={(e) =>
                          handleInputChange(e, "profile", null, "email")
                        }
                      />
                    </div>

                    <div className="field-group">
                      <label>Education:</label>
                      <input
                        type="text"
                        value={profile.education}
                        onChange={(e) =>
                          handleInputChange(e, "profile", null, "education")
                        }
                      />
                    </div>

                    <div className="field-group">
                      <label>Experience (Years):</label>
                      <input
                        type="number"
                        value={profile.experience}
                        onChange={(e) =>
                          handleInputChange(e, "profile", null, "experience")
                        }
                      />
                    </div>

                    <div className="field-group">
                      <label>Location:</label>
                      <input
                        type="text"
                        value={profile.location}
                        onChange={(e) =>
                          handleInputChange(e, "profile", null, "location")
                        }
                      />
                    </div>
                  </div>
                ) : (
                  <>
                    <h2>{profile.name}</h2>
                    <p className="profile-title">@{profile.username || "NA"}</p>
                    <div className="profile-details">
                      <p className="profile-detail">
                        <span className="icon">
                          <MapPin color="#F05555" />
                        </span>{" "}
                        {profile.location || "NA"}
                      </p>
                      <p className="profile-detail">
                        <span className="icon">
                          <Mail color="orange" />
                        </span>{" "}
                        {profile.email || "NA"}
                      </p>
                      <p className="profile-detail">
                        <span className="icon">
                          <Hourglass color="#00CF00" />
                        </span>
                        {profile.experience.toString() + " years" || "NA"}
                      </p>
                      <p className="profile-detail">
                        <span className="icon">
                          <GraduationCap color="#007FFF" />
                        </span>{" "}
                        {profile.education || "NA"}
                      </p>
                    </div>
                  </>
                )}
              </div>
            </div>
          </div>

          <div className="profile-content">
            <div className="profile-tabs">
              <button
                className={`tab-button ${
                  activeTab === "about" ? "active" : ""
                }`}
                onClick={() => setActiveTab("about")}
              >
                About
              </button>

              {/* <button
                className={`tab-button ${
                  activeTab === "experience" ? "active" : ""
                }`}
                onClick={() => setActiveTab("experience")}
              >
                Experience
              </button>

              <button
                className={`tab-button ${
                  activeTab === "education" ? "active" : ""
                }`}
                onClick={() => setActiveTab("education")}
              >
                Education
              </button> */}

              <button
                className={`tab-button ${
                  activeTab === "skills" ? "active" : ""
                }`}
                onClick={() => setActiveTab("skills")}
              >
                Skills
              </button>
            </div>

            <div className="tab-content">
              {activeTab === "about" && (
                <div className="about-section">
                  <h3>About Me</h3>
                  {isEditing ? (
                    <textarea
                      value={profile.about}
                      onChange={(e) =>
                        handleInputChange(e, "profile", null, "about")
                      }
                      className="about-textarea"
                    />
                  ) : (
                    <p>{profile.about}</p>
                  )}
                </div>
              )}

              {/* {activeTab === "experience" && (
                <div className="experience-section">
                  <div className="section-header">
                    <h3>Work Experience</h3>
                    {isEditing && (
                      <button
                        className="add-button"
                        onClick={() =>
                          (document.getElementById(
                            "add-experience-form"
                          ).style.display = "block")
                        }
                      >
                        + Add Experience
                      </button>
                    )}
                  </div>

                  {isEditing && (
                    <div
                      id="add-experience-form"
                      className="add-form"
                      style={{ display: "none" }}
                    >
                      <h4>Add New Experience</h4>
                      <div className="form-fields">
                        <div className="field-group">
                          <label>Job Title:</label>
                          <input
                            type="text"
                            value={newExperience.title}
                            onChange={(e) =>
                              handleInputChange(
                                e,
                                "newExperience",
                                null,
                                "title"
                              )
                            }
                          />
                        </div>

                        <div className="field-group">
                          <label>Company:</label>
                          <input
                            type="text"
                            value={newExperience.company}
                            onChange={(e) =>
                              handleInputChange(
                                e,
                                "newExperience",
                                null,
                                "company"
                              )
                            }
                          />
                        </div>

                        <div className="field-group">
                          <label>Dates:</label>
                          <input
                            type="text"
                            value={newExperience.dates}
                            onChange={(e) =>
                              handleInputChange(
                                e,
                                "newExperience",
                                null,
                                "dates"
                              )
                            }
                          />
                        </div>

                        <div className="field-group">
                          <label>Location:</label>
                          <input
                            type="text"
                            value={newExperience.location}
                            onChange={(e) =>
                              handleInputChange(
                                e,
                                "newExperience",
                                null,
                                "location"
                              )
                            }
                          />
                        </div>

                        <div className="field-group">
                          <label>Description:</label>
                          <textarea
                            value={newExperience.description}
                            onChange={(e) =>
                              handleInputChange(
                                e,
                                "newExperience",
                                null,
                                "description"
                              )
                            }
                          />
                        </div>
                      </div>
                      <div className="form-buttons">
                        <button
                          className="add-button"
                          onClick={handleAddExperience}
                        >
                          Add
                        </button>
                        <button
                          className="cancel-button"
                          onClick={() =>
                            (document.getElementById(
                              "add-experience-form"
                            ).style.display = "none")
                          }
                        >
                          Cancel
                        </button>
                      </div>
                    </div>
                  )}

                  <div className="experience-list">
                    {profile.experience.map((exp, index) => (
                      <div key={index} className="experience-item">
                        {isEditing ? (
                          <div className="edit-experience-form">
                            <div className="form-fields">
                              <div className="field-group">
                                <label>Job Title:</label>
                                <input
                                  type="text"
                                  value={exp.title}
                                  onChange={(e) =>
                                    handleInputChange(
                                      e,
                                      "experience",
                                      index,
                                      "title"
                                    )
                                  }
                                />
                              </div>

                              <div className="field-group">
                                <label>Company:</label>
                                <input
                                  type="text"
                                  value={exp.company}
                                  onChange={(e) =>
                                    handleInputChange(
                                      e,
                                      "experience",
                                      index,
                                      "company"
                                    )
                                  }
                                />
                              </div>

                              <div className="field-group">
                                <label>Dates:</label>
                                <input
                                  type="text"
                                  value={exp.dates}
                                  onChange={(e) =>
                                    handleInputChange(
                                      e,
                                      "experience",
                                      index,
                                      "dates"
                                    )
                                  }
                                />
                              </div>

                              <div className="field-group">
                                <label>Location:</label>
                                <input
                                  type="text"
                                  value={exp.location}
                                  onChange={(e) =>
                                    handleInputChange(
                                      e,
                                      "experience",
                                      index,
                                      "location"
                                    )
                                  }
                                />
                              </div>

                              <div className="field-group">
                                <label>Description:</label>
                                <textarea
                                  value={exp.description}
                                  onChange={(e) =>
                                    handleInputChange(
                                      e,
                                      "experience",
                                      index,
                                      "description"
                                    )
                                  }
                                />
                              </div>
                            </div>
                            <button
                              className="remove-button"
                              onClick={() => handleRemoveExperience(index)}
                            >
                              Remove
                            </button>
                          </div>
                        ) : (
                          <>
                            <div className="experience-header">
                              <h4>{exp.title}</h4>
                              <p className="company">{exp.company}</p>
                              <p className="dates-location">
                                <span>{exp.dates}</span> •{" "}
                                <span>{exp.location}</span>
                              </p>
                            </div>
                            <p className="experience-description">
                              {exp.description}
                            </p>
                          </>
                        )}
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {activeTab === "education" && (
                <div className="education-section">
                  <div className="section-header">
                    <h3>Education</h3>
                    {isEditing && (
                      <button
                        className="add-button"
                        onClick={() =>
                          (document.getElementById(
                            "add-education-form"
                          ).style.display = "block")
                        }
                      >
                        + Add Education
                      </button>
                    )}
                  </div>

                  {isEditing && (
                    <div
                      id="add-education-form"
                      className="add-form"
                      style={{ display: "none" }}
                    >
                      <h4>Add New Education</h4>
                      <div className="form-fields">
                        <div className="field-group">
                          <label>Degree:</label>
                          <input
                            type="text"
                            value={newEducation.degree}
                            onChange={(e) =>
                              handleInputChange(
                                e,
                                "newEducation",
                                null,
                                "degree"
                              )
                            }
                          />
                        </div>

                        <div className="field-group">
                          <label>School:</label>
                          <input
                            type="text"
                            value={newEducation.school}
                            onChange={(e) =>
                              handleInputChange(
                                e,
                                "newEducation",
                                null,
                                "school"
                              )
                            }
                          />
                        </div>

                        <div className="field-group">
                          <label>Dates:</label>
                          <input
                            type="text"
                            value={newEducation.dates}
                            onChange={(e) =>
                              handleInputChange(
                                e,
                                "newEducation",
                                null,
                                "dates"
                              )
                            }
                          />
                        </div>

                        <div className="field-group">
                          <label>Description:</label>
                          <textarea
                            value={newEducation.description}
                            onChange={(e) =>
                              handleInputChange(
                                e,
                                "newEducation",
                                null,
                                "description"
                              )
                            }
                          />
                        </div>
                      </div>
                      <div className="form-buttons">
                        <button
                          className="add-button"
                          onClick={handleAddEducation}
                        >
                          Add
                        </button>
                        <button
                          className="cancel-button"
                          onClick={() =>
                            (document.getElementById(
                              "add-education-form"
                            ).style.display = "none")
                          }
                        >
                          Cancel
                        </button>
                      </div>
                    </div>
                  )}

                  <div className="education-list">
                    {profile.education.map((edu, index) => (
                      <div key={index} className="education-item">
                        {isEditing ? (
                          <div className="edit-education-form">
                            <div className="form-fields">
                              <div className="field-group">
                                <label>Degree:</label>
                                <input
                                  type="text"
                                  value={edu.degree}
                                  onChange={(e) =>
                                    handleInputChange(
                                      e,
                                      "education",
                                      index,
                                      "degree"
                                    )
                                  }
                                />
                              </div>

                              <div className="field-group">
                                <label>School:</label>
                                <input
                                  type="text"
                                  value={edu.school}
                                  onChange={(e) =>
                                    handleInputChange(
                                      e,
                                      "education",
                                      index,
                                      "school"
                                    )
                                  }
                                />
                              </div>

                              <div className="field-group">
                                <label>Dates:</label>
                                <input
                                  type="text"
                                  value={edu.dates}
                                  onChange={(e) =>
                                    handleInputChange(
                                      e,
                                      "education",
                                      index,
                                      "dates"
                                    )
                                  }
                                />
                              </div>

                              <div className="field-group">
                                <label>Description:</label>
                                <textarea
                                  value={edu.description}
                                  onChange={(e) =>
                                    handleInputChange(
                                      e,
                                      "education",
                                      index,
                                      "description"
                                    )
                                  }
                                />
                              </div>
                            </div>
                            <button
                              className="remove-button"
                              onClick={() => handleRemoveEducation(index)}
                            >
                              Remove
                            </button>
                          </div>
                        ) : (
                          <>
                            <div className="education-header">
                              <h4>{edu.degree}</h4>
                              <p className="school">{edu.school}</p>
                              <p className="dates">{edu.dates}</p>
                            </div>
                            <p className="education-description">
                              {edu.description}
                            </p>
                          </>
                        )}
                      </div>
                    ))}
                  </div>
                </div>
              )} */}

              {activeTab === "skills" && (
                <div className="skills-section">
                  {/* <div className="additional-skills-section"> */}
                  <h3>Skills</h3>
                  {isEditing && (
                    <div className="skill-input-div">
                      <label htmlFor="skill-input">Add Skill:</label>
                      <input
                        id="skill-input"
                        type="text"
                        value={newSkill}
                        onChange={(e) => {
                          setNewSkill(e.target.value);
                        }}
                      />
                      <button disabled={!newSkill} onClick={addNewSkill}>
                        Add Skill
                      </button>
                    </div>
                  )}
                  <div className="tag-container">
                    {profile.skills.map((skill, index) => {
                      skill = skill.toLowerCase().trim();
                      return (
                        <div key={index} className="skill-tag">
                          {skill}
                          {isEditing && (
                            <button
                              className="remove-tag"
                              onClick={() => removeSkill(skill)}
                            >
                              ✕
                            </button>
                          )}
                        </div>
                      );
                    })}
                    {/* </div> */}
                  </div>
                </div>
              )}
            </div>
          </div>

          <div className="profile-sidebar">
            {/* <div className="profile-completion">
              <h3>Profile Completion</h3>
              <div className="progress-container">
                <div className="progress-bar">
                  <div className="progress" style={{ width: "85%" }}></div>
                </div>
                <span className="progress-text">85% Complete</span>
              </div>
              <ul className="completion-list">
                <li className="complete">✓ Personal Information</li>
                <li className="complete">✓ Professional Experience</li>
                <li className="complete">✓ Skills</li>
                <li className="complete">✓ Education</li>
                <li>○ Resume Upload</li>
                <li>○ Portfolio Links</li>
              </ul>
            </div> */}

            {/* <div className="resume-upload">
              <h3>Resume</h3>
              <div className="upload-area">
                <div className="upload-icon">📄</div>
                <p>Upload your resume to apply for jobs faster</p>
                <button className="upload-button">Upload Resume</button>
              </div>
            </div> */}

            <div className="account-settings">
              <h3>Account Settings</h3>
              <ul className="settings-list">
                {/* <li>
                  <button className="settings-button">
                    👤 Account Information
                  </button>
                </li>
                <li>
                  <button className="settings-button">
                    ✉️ Email Preferences
                  </button>
                </li> */}

                <li>
                  <div className="settings-button-container">
                    <LockKeyhole color="rgb(255, 217, 0)" />
                    <button className="settings-button">Change Password</button>
                  </div>
                </li>
                <li>
                  <div className="logout-button-container">
                    <DoorOpen color="red" />
                    <button
                      className="settings-button logout"
                      onClick={handleLogout}
                    >
                      Log Out
                    </button>
                  </div>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
