import React from "react";
import './App.css';
import { HashRouter, Route, NavLink, Routes } from "react-router-dom";
import { InputPage } from "./pages/InputPage";
import { OutputPage } from "./pages/OutputPage";
import { HomePage } from "./pages/HomePage";
import { AboutPage } from "./pages/AboutPage";
import { ContactPage } from "./pages/ContactPage";



function App() {

  return (
    <div className="App">
      <HashRouter basename="/">
      <NavLink to="/input">Start Tracing</NavLink>
      <NavLink to="/about">About</NavLink>
      <NavLink to="/contact">Contact</NavLink>
        <Routes>
          <Route exact path="/" element={<HomePage />}/>
          <Route path="/input" element={<InputPage />}/>
          <Route path="/output" element={<OutputPage />}/>
          <Route path="/about" element={<AboutPage />}/>
          <Route path="/contact" element={<ContactPage />}/>
        </Routes>
      </HashRouter>
    </div>
  );
}

export default App;
