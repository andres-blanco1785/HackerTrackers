import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router';
import { Alert, Button } from 'reactstrap';
import { useLocation } from "react-router-dom";
import { getTransactionInfo } from '../utilities/Utilities';
import Collapsible from "../components/Collapsible";
import './OutputPage.css';

export function OutputPage(props) {
	
	const [transactionOutput, setTransactionOutput] = useState({});
	const { state } = useLocation();
	const navigate = useNavigate();
  
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
					<Button onClick={() => {navigate("/input", { state: {}})}}>Go Back</Button>
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
