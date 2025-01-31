import React from 'react';
import './App.css'; // Import the CSS file

function App() {
  return (
    <div>
      <section className="header">
        <nav>
          <a href="/">
            <img src="images/logo.png" alt="ATS Assist" />
          </a>
          <div className="nav-links">
            <ul>
              <li><a href="login">LOGIN</a></li>
              <li><a href="#jumpp">ABOUT</a></li>
            </ul>
          </div>
        </nav>

        <div className="text-box">
          <h1>ATS Assist Resume Enhancer</h1>
          <p>Blah Blah Blah Blah BlahBlahBlahBlah Blah BlahBlah Blah BlahBlahBlahBlahBlahBlahBlahBlahBlahBlahBlah
            BlahBlahBlahBlahBlahBlahBlahBlahBlahBlahBlahBlahBlahBlahBlahBlahBlahBlahBlahBlahBlahBlahBlahBlah
            BlahBlahBlahBlahBlahBlahBlahBlahBlahBlahBlahBlahBlahBlahBlahBlahBlahBlahBlahBlahBlahBlahBlah
            [THIS IS THE INFO ABOUT THE WEBSITE]
          </p>

          <a href="#jump" className="btn">Know More</a>
        </div>
      </section>

      <section className="features" id="jump">
        <h1>Why Choose ATS ASSIST</h1>
        <p>Vocablearn has various features for improved and better user experience.</p>

        <div className="row">
          <div className="features-col">
            <h3>Word Review</h3>
            <img src="images/review1.png" alt="Word Review" />
            <p>The user can go through the words that they have mastered, hence can be revised.</p>
          </div>

          <div className="features-col">
            <h3>Score Viewing</h3>
            <img src="images/score.png" alt="Score Viewing" />
            <p>Based upon the progress and performance of the user, scores will be allotted and can be viewed in the form of graphs.</p>
          </div>

          <div className="features-col">
            <h3>Auto Word Adjustment</h3>
            <img src="images/auto1.png" alt="Auto Word Adjustment" />
            <p>According to the performance of the user, the difficulty level is altered by the model automatically.</p>
          </div>
        </div>
      </section>

      <section className="cta">
        <h1>New User?</h1>
        <a href="login" className="btn">Get Started</a>
      </section>

      <section className="footer" id="jumpp">
        <h4>About Us</h4>
        <p>gaurisasikumar04@gmail.com <br /> A. P. Shah Institute Of Technology</p>
        <div className="icons">
          <i className="fa fa-facebook"></i>
          <i className="fa fa-twitter"></i>
          <i className="fa fa-instagram"></i>
          <i className="fa fa-linkedin"></i>
        </div>
      </section>
    </div>
  );
}

export default App;
