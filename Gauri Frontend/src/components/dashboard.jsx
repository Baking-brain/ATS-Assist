import "./dashboard.css"; // Import the new CSS file
import NavBar from "./nav-bar.jsx";
import ResumeUpload from "./resume-upload.jsx";
import ContentBlock from "./content-block.jsx";

export default function Dashboard() {
  return (
    <div className="dashboard">
      <NavBar />
      <ResumeUpload />
      <main className="container">
        <div className="grid">
          <ContentBlock />
          <ContentBlock buttons />
        </div>
      </main>
    </div>
  );
}

