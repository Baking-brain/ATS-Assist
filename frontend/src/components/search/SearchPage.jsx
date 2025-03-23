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
const isDevelopment = import.meta.env.VITE_IS_DEVELOPMENT === "true";

// Mock search results
const mockJobs = [
  {
    id: 1,
    title: "Senior Frontend Developer",
    company: "TechCorp Inc.",
    location: "San Francisco, CA",
    type: "Full-time",
    salary: "$120,000 - $150,000",
    description:
      "We're looking for an experienced frontend developer with expertise in React, TypeScript and modern web technologies.",
    posted: "2 days ago",
    skills: ["React", "TypeScript", "JavaScript", "HTML", "CSS"],
    featured: true,
  },
  {
    id: 2,
    title: "UX/UI Designer",
    company: "DesignHub",
    location: "Remote",
    type: "Contract",
    salary: "$80,000 - $100,000",
    description:
      "Join our design team to create beautiful and intuitive user interfaces for our flagship product.",
    posted: "1 week ago",
    skills: ["Figma", "Adobe XD", "UI Design", "User Research", "Prototyping"],
    featured: false,
  },
  {
    id: 3,
    title: "DevOps Engineer",
    company: "CloudNine Solutions",
    location: "New York, NY",
    type: "Full-time",
    salary: "$130,000 - $160,000",
    description:
      "Seeking a skilled DevOps engineer to optimize our cloud infrastructure and deployment processes.",
    posted: "3 days ago",
    skills: ["AWS", "Docker", "Kubernetes", "CI/CD", "Linux"],
    featured: true,
  },
  {
    id: 4,
    title: "Backend Developer",
    company: "DataStream Analytics",
    location: "Boston, MA",
    type: "Full-time",
    salary: "$110,000 - $140,000",
    description:
      "Build scalable backend services for our growing data analytics platform.",
    posted: "4 days ago",
    skills: ["Python", "Node.js", "SQL", "MongoDB", "API Design"],
    featured: false,
  },
];

const mockCandidates = [
  {
    id: 1,
    name: "Alex Johnson",
    experience: "8 years",
    education: "M.S. Computer Science",
    skills: ["React", "Node.js", "TypeScript", "AWS", "Docker"],
  },
  {
    id: 2,
    name: "Sarah Williams",
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
    experience: "6 years",
    education: "B.S. Computer Engineering",
    skills: ["JavaScript", "React", "Python", "Django", "PostgreSQL"],
  },
  {
    id: 4,
    name: "Priya Patel",
    experience: "4 years",
    education: "Ph.D. Statistics",
    skills: ["Python", "R", "Machine Learning", "SQL", "TensorFlow"],
  },
];

export default function SearchPage() {
  const [searchString, setSearchString] = useState("");
  const [searchMode, setSearchMode] = useState("jobs");
  const [isLoading, setIsLoading] = useState(false);
  const [displayData, setDisplayData] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    // Set initial results based on the search mode
    setDisplayData(searchMode === "jobs" ? mockJobs : mockCandidates);
    setIsLoading(false);
    setSearchString("");
  }, [searchMode]);

  const handleSearch = () => {
    setIsLoading(true);

    // Simulate search delay
    let results = searchMode === "jobs" ? mockJobs : mockCandidates;

    // Filter by search query if provided
    if (searchString.trim()) {
      const query = searchString.toLowerCase();

      if (searchMode === "jobs") {
        results = results.filter(
          (job) =>
            job.title.toLowerCase().includes(query) ||
            job.company.toLowerCase().includes(query) ||
            job.skills.some((skill) => skill.toLowerCase().includes(query))
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
    }

    console.log("Searching... ", results);

    setDisplayData(results);
    setIsLoading(false);
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
          <h2>{displayData.length} Results</h2>
        </div>

        <div className="results-container">
          {displayData.map((item) => {
            if (searchMode === "jobs") {
              return <JobCard key={item.id} job={item} />;
            } else {
              return <CandidateCard key={item.id} candidate={item} />;
            }
          })}
        </div>
      </>
    );
  };

  useEffect(() => {
    async function getdisplayData() {
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
    if (isDevelopment) {
      handleSearch();
    } else {
      getdisplayData();
    }
  }, [searchString]);

  return (
    <div id="search">
      <div className="container">
        <div className="search-tabs">
          <button
            className={`tab ${searchMode === "jobs" ? "active" : ""}`}
            onClick={() => setSearchMode("jobs")}
          >
            Search Jobs
          </button>
          <button
            className={`tab ${searchMode === "candidates" ? "active" : ""}`}
            onClick={() => setSearchMode("candidates")}
          >
            Search Candidates
          </button>
        </div>

        <div className="search-box">
          <p className="search-info">
            Search for{" "}
            {searchMode === "jobs" ? "jobs by skills" : "candidates by skills"}
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
          {job.skills.map((skill, index) => (
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
        </div>
      </div>
      <div className="candidate-card-content">
        <div className="candidate-details">
          <div className="detail-item">
            <span className="icon">
              <GraduationCap color="#7c3aed" />
            </span>
            <span>{candidate.education}</span>
          </div>
          <div className="detail-item">
            <span className="icon">
              <Hourglass color="#7c3aed" />
            </span>
            <span>{candidate.experience} experience</span>
          </div>
        </div>
        <div className="candidate-skills">
          {candidate.skills.map((skill, index) => (
            <span key={index} className="skill-tag">
              {skill}
            </span>
          ))}
        </div>
      </div>
      <div className="candidate-card-footer">
        <button className="view-profile-button">View Profile</button>
      </div>
    </div>
  );
};
