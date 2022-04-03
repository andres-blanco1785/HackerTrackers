import React, { useState } from 'react';
import { useNavigate } from 'react-router';
import { Button, Input, Label } from 'reactstrap';
import './InputPage.css';

/**
 * The Input Page presents the user with a single input box and button.
 * The input box is where they are permitted to enter in a transaction hash string
 * The button, when clicked, will redirect the user to the output page with the transaction hash string 
 */
export default function InputPage() {

  const [transactionInput, setTransactionInput] = useState();
  const navigate = useNavigate();

  function onButtonClick() {
    navigate("/output", { state: transactionInput});
    localStorage.setItem('transactionInput', transactionInput);
    localStorage.removeItem('forwardsTrace');
    localStorage.removeItem('backwardsTrace');
  }

  return (
    <div className="inputPage">
      <div className="inputGroup">
        <Label for="transactionInput">Transaction ID:</Label>
        <Input type="text" className="inputTextBox"
          id="transactionInput"
          onChange={(e) => setTransactionInput(e.target.value)}
          value={transactionInput}
        />
        <Button color="light" onClick={onButtonClick}>Start Tracing!</Button>
      </div>
    </div>
  )
}
