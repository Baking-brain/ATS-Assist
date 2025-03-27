import React, { useEffect, useState } from "react";
import axios from "axios";
import "./search.css";
const isDevelopment = import.meta.env.VITE_IS_DEVELOPMENT === "true";

function Item({ username, skills }) {
  return (
    <div className="item">
      <h1>{username}</h1>
      <ol className="skill">
        {skills.map((skill, index) => {
          if (index >= 3) return;
          return (
            <div key={index}>
              {index + 1}: {skill}
            </div>
          );
        })}
      </ol>
    </div>
  );
}

export default function Search() {
  const [displayData, setDisplayData] = useState([
    {
      username: "test1",
      skills: ["Skill1", "Skill2", "Skill3", "Skill1", "Skill2"],
    },
    {
      username: "test2",
      skills: ["Skill1", "Skill2"],
    },
    {
      username: "test3",
      skills: ["Skill1", "Skill2"],
    },
  ]);
  const [searchType, setSearchType] = useState("applicant");
  const [searchString, setSearchString] = useState("");

  useEffect(() => {
    async function getSearchResults() {
      await axios
        .get("/api/get_search_results", {
          params: { search_string: searchString, search_type: searchType },
        })
        .then((response) => {
          setDisplayData(response.data);
        })
        .catch((error) => {
          console.log("Error=> ", error);
        });
    }
    if (!isDevelopment) {
      getSearchResults();
    }
  }, [searchString]);

  return (
    <div id="search-con">
      <input
        className="navbar-search center"
        placeholder="Search"
        value={searchString}
        onChange={(e) => {
          setSearchString(e.target.value);
        }}
      ></input>
      <div className="radio-buttons">
        <label>
          <input
            type="radio"
            name="role"
            value="applicant"
            checked={searchType === "applicant"}
            onChange={(e) => {
              setSearchType(e.target.value);
            }}
          />
          Applicant
        </label>
        <label>
          <input
            type="radio"
            name="role"
            value="job"
            checked={searchType === "job"}
            onChange={(e) => {
              setSearchType(e.target.value);
            }}
          />
          Job
        </label>
      </div>
      <div id="item-con">
        {displayData.map((data, index) => {
          return (
            <Item key={index} username={data.username} skills={data.skills} />
          );
        })}
      </div>
    </div>
  );
}
