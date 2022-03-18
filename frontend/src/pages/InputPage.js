import React, { useState } from 'react';
import { useNavigate } from 'react-router';
import { Button, Form, Input, Label } from 'reactstrap';
import './InputPage.css';

export function InputPage() {

  const [transactionInput, setTransactionInput] = useState();
  const navigate = useNavigate();

  function onButtonClick() {
    navigate("/output", { state: transactionInput});
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
