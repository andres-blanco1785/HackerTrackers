import React, { useState, useEffect } from 'react';
import Collapsible from "../components/Collapsible";
import { useLocation } from "react-router-dom";
import { getTransactionInfo } from '../utilities/Utilities';

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
		}
	}

  useEffect(()=>{
    getTransactionInfo(state)
      .then((transactionJson)=>{ setTransactionOutput(transactionJson) });
    printTransactionInfo()
    },[transactionOutput]
  )

  return (
    <div>
      OUTPUT PAGE
    <p>{printTransactionInfo()}</p>
    </div>
  )
}
