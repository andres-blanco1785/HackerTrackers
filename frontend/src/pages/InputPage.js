import React, { useState } from 'react';
import { useNavigate } from 'react-router';

export function InputPage() {

  const [transactionInput, setTransactionInput] = useState();
  const navigate = useNavigate();

  

  function onButtonClick() {
      navigate("/output", { state: transactionInput});
  }


  return (
    <div>
      <input type="text"
            onChange={(e) => setTransactionInput(e.target.value)}
            value={transactionInput}/>
      <button onClick={onButtonClick}>transactionID</button>
    </div>
  )
}
