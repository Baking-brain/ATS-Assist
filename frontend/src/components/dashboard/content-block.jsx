import "./content-block.css";

export default function ContentBlock({ buttons = false }) {
  return (
    <div className="content-block">
      <div className={`content-box ${buttons ? "square" : "full-height"}`} />
      {buttons && (
        <div className="button-container">
          {/* <button className="content-button">Grammar</button> */}
          <button className="content-button">AI Insights</button>
          <button className="content-button">Suggest Skills</button>
        </div>
      )}
    </div>
  );
}
