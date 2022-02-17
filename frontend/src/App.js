import React, { useState } from "react";
import './App.css';

async function getFibSequence(n) {
  
  let sequence = await fetch(`http://127.0.0.1:5000/fibonacci/${n}`)
      .then(response => response.text())
      .then(result => { return result });
  
  return sequence;
}

function App() {

  const [fibInput, setFibInput] = useState();
  const [fibOutput, setFibOutput] = useState({});

  function onButtonClick() {
    setFibOutput(getFibSequence(fibInput));
  }
  
  
  return (
    <div className="App">
      <input type="number" onChange={(e) => setFibInput(e.target.value)} value={fibInput}/>
      <button onClick={onButtonClick}>testing</button>
      <p>{fibOutput.input}</p>
    </div>
  );
}

export default App;
