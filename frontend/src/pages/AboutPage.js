import React from 'react'
import hticon from "../images/HackerTrackers.png";
import "./AboutPage.css";


export default function AboutPage (){
  return (
    <>
        <div className="about-section">
          <img src={hticon} width='200' height='200' />
          <h1>About Us</h1>
          <p>Some text about who we are and what we do.</p>
          <p>Resize the browser window to see that this page is responsive by the way.</p>
        </div>
    </>
  )
}
