import "./content-block.css"; // Import CSS

export default function ContentBlock({ buttons = false }) {
  return (
    <div className="content-block">
      <div className={`content-box ${buttons ? "square" : "full-height"}`} />
      {buttons && (
        <div className="button-container">
          <button className="content-button">Button 1</button>
          <button className="content-button">Button 2</button>
          <button className="content-button">Button 3</button>
        </div>
      )}
    </div>
  );
}
