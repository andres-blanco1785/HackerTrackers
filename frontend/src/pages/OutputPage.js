import React, { useState, useEffect } from 'react';
import Collapsible from "../components/Collapsible";
import { Alert } from 'reactstrap';
import { useLocation } from "react-router-dom";
import { getTransactionInfo } from '../utilities/Utilities';
import './OutputPage.css';

export function OutputPage(props) {
  const { state } = useLocation();
  const [transactionOutput, setTransactionOutput] = useState({});
  
  function printTransactionInfo() {
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
		} else {
			return(
				<div>
					<Alert color="danger" className="errorBox">
						This transaction is INVALID, please try again
					</Alert>
				</div>
			)
		}
	}

  useEffect(()=>{
    getTransactionInfo(state)
      .then((transactionJson)=>{ setTransactionOutput(transactionJson) });
    printTransactionInfo()
    },[transactionOutput, state]
  )

  return (
    <div>
    	<p>{printTransactionInfo()}</p>
    </div>
  )
}
