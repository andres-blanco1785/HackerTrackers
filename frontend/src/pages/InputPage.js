import React, { useState } from 'react';
import history from "../utilities/history";
import axios from 'axios';

//this is the input page and 
export function InputPage() {

  const [transactionInput, setTransactionInput] = useState();
  const [transactionOutput, setTransactionOutput] = useState({});

  // const fetchData = async () => {
    
  //   setTransactionOutput(response.data);
  // };
  
  async function onStartTracingClick() {
    const response = await axios.get(`http://127.0.0.1:5000/transaction/${transactionInput}`);
    history.push({
      pathname: "/#/output",
      state: response.data
    });
    setTransactionOutput(response.data);
  }

  return (
    <div>
        <input type="text" onChange={(e) => setTransactionInput(e.target.value)} value={transactionInput}/>
        <button onClick={onStartTracingClick}>Start Tracing!</button>
        {transactionOutput.accounts &&
            <div>
            {transactionOutput.accounts.map((account, index ) => {
                return (
                    <div key={index}>
                        account # {index}: {account.account.address}
                    </div>
                )
            })}
            </div>
        }
    </div>
  )
}
