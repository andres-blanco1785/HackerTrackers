import React from 'react';
import styled from 'styled-components'
import "./HomePage.css";
import 'react-slideshow-image/dist/styles.css';
import Button from '@material-ui/core/Button';
import { Link } from 'react-router-dom'
import slide1 from "../images/slide1.jpg";
import { Slide } from 'react-slideshow-image';
import {
  View,
} from 'react-native';



export function HomePage () {

    const Button = styled.button`
        width: 150px;
        background-color: #698672;
        color: black;
        transition-duration: 0.2s;
        padding: 20px 32px;
        border: none;
        text-align: center;
        text-decoration: none;
        font-size: 20px;
        font-family: "Monaco", monospace;
        &:hover{
            background-color: #78b281; /* Green */
            color: white;
        }
    `

    return (
      <>

          <div style={{'backgroundImage': `url(${slide1})`}}>
            <div>WELCOME TO OUR SPLASH PAGE</div>
            <Slide easing="ease">
              <div className="each-slide">
                  <div>
                      <span>Visualization of the network between different accounts and transactions.</span>
                  </div>
              </div>
              <div className="each-slide">
                <div >
                  <span>We aim to provide a trace of the source and destination of the funds in a crypto attack.</span>
                </div>
              </div>
              <div className="each-slide">
                <div >
                  <span>Slide 3</span>
                </div>
              </div>
            </Slide>
          </div>
          <div style={{padding: 20 ,}}/>
          <span className="begin">Begin Experience</span>

          <View
              style={{
                  borderBottomColor: '#698672',
                  borderBottomWidth: 3,
                  padding: 2,
              }}
            />
          <div className= "start">
              <Link to="/input">
                  <Button>
                      Start
                  </Button>
              </Link>
          </div>





      </>

  )
}
