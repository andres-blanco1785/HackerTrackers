import React, { useState } from 'react';
import { useNavigate } from 'react-router';
import { Button, Container, Input } from 'reactstrap';
import './InputPage.css';

export function InputPage() {

  const [transactionInput, setTransactionInput] = useState();
  const navigate = useNavigate();

  function onButtonClick() {
      navigate("/output", { state: transactionInput});
  }


  return (
    <div style={{ height: "100vh"}}>
      <Container fluid className="inputBox">
        <Input type="text"
          onChange={(e) => setTransactionInput(e.target.value)}
          value={transactionInput}></Input>

        <Button onClick={onButtonClick}>transactionID</Button>
      </Container>
    </div>
  )
}
