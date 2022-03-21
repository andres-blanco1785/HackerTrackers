import React from "react";
import './App.css';
import { HashRouter, Route, Routes } from "react-router-dom";
import { Navbar, NavbarBrand, NavItem, NavLink, Nav } from 'reactstrap';
import InputPage from "./pages/InputPage";
import OutputPage from "./pages/OutputPage";
import HomePage from "./pages/HomePage";
import AboutPage from "./pages/AboutPage";
import ContactPage from "./pages/ContactPage";
import BlacklistPage from "./pages/BlacklistPage";

function App() {

  return (
    <div className="App">
      <HashRouter basename="/">
        <Navbar expand="md">
          <NavbarBrand href="/" className="mr-auto">
            <img src={require("./assets/HackerTrackers.png")} style={{width: 256}} alt="Navigation bar brand logo"/>	
          </NavbarBrand>
          <Nav className="me-auto"
          navbar>
            <NavItem>
              <NavLink href="/#/input">Start Tracing</NavLink>
            </NavItem>
            <NavItem>
              <NavLink href="/#/about">About</NavLink>
            </NavItem>
            <NavItem>
              <NavLink href="/#/contact">Contact</NavLink>
            </NavItem>
            <NavItem>
              <NavLink href="/#/blacklist">Blacklist</NavLink>
            </NavItem>
          </Nav>
        </Navbar>
        <Routes>
          <Route exact path="/" element={<HomePage />}/>
          <Route path="/input" element={<InputPage />}/>
          <Route path="/output" element={<OutputPage />}/>
          <Route path="/about" element={<AboutPage />}/>
          <Route path="/contact" element={<ContactPage />}/>
          <Route path="/blacklist" element={<BlacklistPage />}/>
        </Routes>
      </HashRouter>
    </div>
  );
}

export default App;
