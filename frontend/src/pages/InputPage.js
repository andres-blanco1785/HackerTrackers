import React, { useState, useEffect } from 'react';
import history from "../utilities/history";
import Collapsible from "../Collapsible";

export function InputPage() {

  const [transactionInput, setTransactionInput] = useState();
  const [transactionOutput, setTransactionOutput] = useState({});
  const [open, setOpen] = useState(true);
  const [listAccNum, setlistAccNum] = useState();

  async function getTransactionInfo(n) {
  
    let sequence = await fetch(`http://127.0.0.1:5000/transaction/${n}`)
        .then(response => response.json())
        .then(result => { return result});
  
  
    console.log('sequence',sequence)
  
    return sequence;
  }
  function printTransactionInfo() {
		console.log("transactionOutput", transactionOutput);
		if(typeof transactionOutput.accounts !== 'undefined') {
		let numAccounts = transactionOutput.accounts.length;
			console.log(numAccounts);
			return(
				<>
				<h2>Transaction accounts </h2>
					{transactionOutput.accounts?.map((account, i) => (
						<Collapsible label = {account.account.address}>
							<p> postBalances: {transactionOutput.meta.postBalances[i]}</p>
							<p> preBalances: {transactionOutput.meta.preBalances[i]}</p>
							<p> Difference :{transactionOutput.meta.postBalances[i] - transactionOutput.meta.preBalances[i]} </p>
						</Collapsible>
					))}
				</>
			)
		}
	}


  function onButtonClick()
  {
      getTransactionInfo(transactionInput)
        .then((transactionJson)=>{ setTransactionOutput(transactionJson) });
  }
  useEffect(()=>{
      printTransactionInfo()
      },[transactionOutput]
  )
  
  
  // async function onStartTracingClick() {
  //   const response = await axios.get(`http://127.0.0.1:5000/transaction/${transactionInput}`);
  //   history.push({
  //     pathname: "/#/output",
  //     state: response.data
  //   });
  //   setTransactionOutput(response.data);
  // }

  return (
    <div>
      <input type="text"
            onChange={(e) => setTransactionInput(e.target.value)}
            value={transactionInput}/>
      <button onClick={onButtonClick}>transactionID</button>


      <p>{printTransactionInfo()}</p>
    </div>
  )
}
