import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import "./SearchPage.css";
import {
  Building,
  GraduationCap,
  Hourglass,
  IndianRupee,
  MapPin,
} from "lucide-react";
import getRefreshToken from "../refresh_token";
import axios from "axios";
const isDevelopment = import.meta.env.VITE_IS_DEVELOPMENT === "true";

// Mock search results
const mockJobs = [
  {
    id: 1,
    title: "Senior Frontend Developer",
    company: "TechCorp Inc.",
    location: "San Francisco, CA",
    salary: "$120,000 - $150,000",
    description:
      "We're looking for an experienced frontend developer with expertise in React, TypeScript and modern web technologies.",
    requirements: ["React", "TypeScript", "JavaScript", "HTML", "CSS"],
  },
  {
    id: 2,
    title: "UX/UI Designer",
    company: "DesignHub",
    location: "Remote",
    salary: "$80,000 - $100,000",
    description:
      "Join our design team to create beautiful and intuitive user interfaces for our flagship product.",
    requirements: [
      "Figma",
      "Adobe XD",
      "UI Design",
      "User Research",
      "Prototyping",
    ],
  },
  {
    id: 3,
    title: "DevOps Engineer",
    company: "CloudNine Solutions",
    location: "New York, NY",
    salary: "$130,000 - $160,000",
    description:
      "Seeking a skilled DevOps engineer to optimize our cloud infrastructure and deployment processes.",
    requirements: ["AWS", "Docker", "Kubernetes", "CI/CD", "Linux"],
  },
  {
    id: 4,
    title: "Backend Developer",
    company: "DataStream Analytics",
    location: "Boston, MA",
    salary: "$110,000 - $140,000",
    description:
      "Build scalable backend services for our growing data analytics platform.",
    requirements: ["Python", "Node.js", "SQL", "MongoDB", "API Design"],
  },
];

const mockCandidates = [
  {
    id: 1,
    name: "Alex Johnson",
    username: "alexjohnson",
    experience: 0.0,
    education: "",
    skills: ["hello", "heelo2"],
  },
  {
    id: 2,
    name: "Sarah Williams",
    username: "sarahwilliams",
    experience: "5 years",
    education: "B.A. Graphic Design",
    skills: [
      "Figma",
      "Adobe XD",
      "User Research",
      "Wireframing",
      "Prototyping",
    ],
  },
  {
    id: 3,
    name: "David Chen",
    username: "davidchen",
    experience: "6 years",
    education: "B.S. Computer Engineering",
    skills: ["JavaScript", "React", "Python", "Django", "PostgreSQL"],
  },
  {
    id: 4,
    name: "Priya Patel",
    username: "priyapatel",
    experience: "4 years",
    education: "Ph.D. Statistics",
    skills: ["Python", "R", "Machine Learning", "SQL", "TensorFlow"],
  },
];

export default function SearchPage() {
  const [searchString, setSearchString] = useState("");
  const [searchType, setSearchType] = useState("jobs");
  const [isLoading, setIsLoading] = useState(false);
  const [displayData, setDisplayData] = useState([]);
  const navigate = useNavigate();

  const handleSearch = () => {
    setIsLoading(true);

    // Simulate search delay
    let results = displayData;

    // Filter by search query if provided
    if (searchString.trim()) {
      const query = searchString.toLowerCase();

      if (searchType === "jobs") {
        results = results.filter(
          (job) =>
            job.title.toLowerCase().includes(query) ||
            job.company.toLowerCase().includes(query) ||
            job.requirements.some((skill) =>
              skill.toLowerCase().includes(query)
            )
        );
      } else {
        results = results.filter(
          (candidate) =>
            candidate.name.toLowerCase().includes(query) ||
            candidate.skills.some((skill) =>
              skill.toLowerCase().includes(query)
            )
        );
      }
      setDisplayData(results);
    }
  };

  const renderdisplayData = () => {
    if (isLoading) {
      return (
        <div className="loading-container">
          <div className="loading-spinner"></div>
          <p>Searching...</p>
        </div>
      );
    }

    if (displayData.length === 0) {
      return (
        <div className="no-results">
          <h3>No results found</h3>
        </div>
      );
    }

    return (
      <>
        <div className="results-header">
          {!searchString && searchType === "applicants" ? (
            <h2>Other applicants like you</h2>
          ) : (
            <h2>{displayData.length} Results</h2>
          )}
        </div>

        <div className="results-container">
          {displayData.map((item) => {
            if (searchType === "jobs") {
              return <JobCard key={item.id} job={item} />;
            } else {
              return <CandidateCard key={item.id} candidate={item} />;
            }
          })}
        </div>
      </>
    );
  };

  async function getSimilarApplicants() {
    try {
      const getSimilarApplicantsResponse = await axios.get(
        "/api/get_similar_applicants"
      );
      // console.log(getSimilarApplicantsResponse);
      setDisplayData(getSimilarApplicantsResponse.data.Applicants);
      setIsLoading(false);
    } catch (getSimilarApplicantsError) {
      const errMsg = getSimilarApplicantsError.response.data.detail;
      console.log("Profile fetch error: \n", getSimilarApplicantsError, errMsg);

      //If cookies not set
      if (errMsg.includes("not provided")) {
        alert("Session not started, please login again");
        navigate("/");
        return;
      }

      //If access token expired
      if (errMsg.includes("invalid or expired")) {
        try {
          const refreshTokenMsg = await getRefreshToken();
        } catch (refreshError) {
          console.log("Refresh error: ", refreshError);

          //If refresh token expired
          if (refreshError.message == "Refresh token expired") {
            alert("Session expired, please login again");
            navigate("/");
            return;
          }
        }
      }
    }
  }

  async function getSimilarJobs() {
    try {
      const getSimilarJobs = await axios.get("/api/get_similar_jobs");
      // console.log(getSimilarJobs);
      setDisplayData(getSimilarJobs.data.Jobs);
      setIsLoading(false);
    } catch (getSimilarJobsError) {
      const errMsg = getSimilarJobsError.response.data.detail;
      console.log("Profile fetch error: \n", getSimilarJobsError, errMsg);

      //If cookies not set
      if (errMsg.includes("not provided")) {
        alert("Session not started, please login again");
        navigate("/");
        return;
      }

      //If access token expired
      if (errMsg.includes("invalid or expired")) {
        try {
          const refreshTokenMsg = await getRefreshToken();
        } catch (refreshError) {
          console.log("Refresh error: ", refreshError);

          //If refresh token expired
          if (refreshError.message == "Refresh token expired") {
            alert("Session expired, please login again");
            navigate("/");
            return;
          }
        }
      }
    }
  }
  useEffect(() => {
    setSearchString("");
    if (isDevelopment) {
      setDisplayData(searchType === "jobs" ? mockJobs : mockCandidates);
      setTimeout(() => {
        setIsLoading(false);
      }, 300);
    } else {
      if (searchType === "applicants") {
        getSimilarApplicants();
        return;
      } else if (searchType === "jobs") {
        getSimilarJobs();
        return;
      }
    }
    // Set initial results based on the search mode
    // setDisplayData(searchType === "jobs" ? mockJobs : mockCandidates);
    // setIsLoading(false);
  }, [searchType]);

  useEffect(() => {
    async function getSearchedData() {
      await axios
        .get("/api/get_search_results", {
          params: { search_string: searchString, search_type: searchType },
        })
        .then((response) => {
          setDisplayData(response.data);
        })
        .catch((error) => {
          console.log("Search Error=> ", error);
        });
    }

    //Check for development
    if (isDevelopment) {
      handleSearch();
      setIsLoading(false);
    } else {
      //Return if no search query
      if (!searchString.trim()) {
        //Returning similar based on search type
        if (searchType === "jobs") {
          getSimilarJobs();
          return;
        } else {
          getSimilarApplicants();
          return;
        }
      }

      //Temporary=> Return if searching for jobs(not implemented yet)
      if (searchType === "jobs") {
        return;
      } else {
        getSearchedData();
      }
    }
  }, [searchString]);

  return (
    <div id="search">
      <div className="container">
        <div className="search-tabs">
          <button
            className={`tab ${searchType === "jobs" ? "active" : ""}`}
            onClick={() => {
              setIsLoading(true);
              setSearchType("jobs");
            }}
          >
            Search Jobs
          </button>
          <button
            className={`tab ${searchType === "applicants" ? "active" : ""}`}
            onClick={() => {
              setIsLoading(true);
              setSearchType("applicants");
            }}
          >
            Search Applicants
          </button>
        </div>

        <div className="search-box">
          <p className="search-info">
            Search for{" "}
            {searchType === "jobs" ? "jobs by skills" : "applicants by skills"}
          </p>
          <div className="search-input-container">
            <input
              type="text"
              className="search-input"
              placeholder={`Enter skill`}
              value={searchString}
              onChange={(e) => setSearchString(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter") handleSearch();
              }}
            />
            <button
              className="search-button"
              onClick={handleSearch}
              disabled={isLoading}
            >
              {isLoading ? "..." : "Search"}
            </button>
          </div>
        </div>

        {/* Search Results */}
        <div className="search-results">{renderdisplayData()}</div>
      </div>
    </div>
  );
}

const JobCard = ({ job }) => {
  return (
    <div className={`job-card ${job.featured ? "featured" : ""}`}>
      <div className="job-card-header">
        <div>
          <h3 className="job-title">{job.title}</h3>
          <div className="job-meta">
            <span className="company">
              <span className="icon">
                <Building color="#7c3aed" />
                <p>{job.company}</p>
              </span>
            </span>
            <span className="location">
              <span className="icon">
                <MapPin color="#7c3aed" />
                <p>{job.location}</p>
              </span>
            </span>
          </div>
        </div>
      </div>
      <div className="job-card-content">
        <p className="job-description">{job.description}</p>
        <div className="job-skills">
          {job.requirements.map((skill, index) => (
            <span key={index} className="skill-tag">
              {skill}
            </span>
          ))}
        </div>
      </div>
      <div className="job-card-footer">
        <div className="job-details">
          <span className="salary">
            <span className="icon">
              <IndianRupee />
              <p>{job.salary}</p>
            </span>
          </span>
        </div>
        <button className="apply-button">Apply Now</button>
      </div>
    </div>
  );
};

const CandidateCard = ({ candidate }) => {
  return (
    <div className={`candidate-card ${candidate.featured ? "featured" : ""}`}>
      <div className="candidate-card-header">
        <div className="candidate-info">
          <h3 className="candidate-name">{candidate.name}</h3>
          <p className="candidate-username">@{candidate.username}</p>
        </div>
      </div>
      <div className="candidate-card-content">
        <div className="candidate-details">
          <div className="detail-item">
            <span className="icon">
              <GraduationCap color="#7c3aed" />
            </span>
            <span>{candidate.education || "Not Provided"}</span>
          </div>
          <div className="detail-item">
            <span className="icon">
              <Hourglass color="#7c3aed" />
            </span>
            <span>{candidate.experience} years experience</span>
          </div>
        </div>
        <div className="candidate-skills">
          {candidate.skills.length
            ? candidate.skills.map((skill, index) => (
                <span key={index} className="skill-tag">
                  {skill}
                </span>
              ))
            : "Skills not provided"}
        </div>
      </div>
      <div className="candidate-card-footer">
        <button className="view-profile-button">View Profile</button>
      </div>
    </div>
  );
};
