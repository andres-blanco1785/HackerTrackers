import React, { useState } from "react";
import './App.css';

async function getTransactionInfo(n) {
  
  let sequence = await fetch(`http://127.0.0.1:5000/transaction/${n}`)
      .then(response => response.text())
      .then(result => { return result });
  
  return sequence;
}

function App() {

  const [transactionInput, setTransactionInput] = useState();
  const [transactionOutput, setTransactionOutput] = useState({});

  function onButtonClick() {
    setTransactionOutput(getTransactionInfo(transactionInput));
  }
  
  
  return (
    <div className="App">
      <input type="text" onChange={(e) => setTransactionInput(e.target.value)} value={transactionInput}/>
      <button onClick={onButtonClick}>testing</button>
      {/* <p>{transactionOutput.inspect}</p> */}
    </div>
  );
}

export default App;
