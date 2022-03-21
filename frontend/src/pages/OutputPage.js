import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router';
import { Alert, Button, Spinner } from 'reactstrap';
import { useLocation } from "react-router-dom";
import { getBackwardsTrace } from '../utilities/Utilities';
import { getForwardsTrace } from '../utilities/Utilities';
import Collapsible from "../components/Collapsible";
import './OutputPage.css';

/**
 * The output page, once rendered (in useEffect function), triggers API calls with 
 * the transaction signature to receive both the forwards and backwards trace
 * 
 * 
 */

export default function OutputPage(props) {
	
	const { state } = useLocation();
	const navigate = useNavigate();

	/**
	 * if isLoading is true, it will render a loading screen (will be changed later)
	 * if isInvalidRequest is true, it will render an alert to the user that the input is invalid
	 */
	const [isLoading, setIsLoading] = useState(true);
	const [isInvalidRequest, setInvalidRequest] = useState(false);
	const [backwardsTraceInfo, setBackwardsTraceInfo] = useState(undefined);
	const [forwardsTraceInfo, setForwardsTraceInfo] = useState(undefined);
  
	// AT THE MOMENT THIS IS NOT BEING USED BUT CAN BE UTILIZED FOR ANOTHER PURPOSE
	// function printTransactionInfo() {
	// 	if(typeof transactionOutput.accounts !== 'undefined') {
	// 	let numAccounts = transactionOutput.accounts.length;
	// 		console.log(numAccounts);
	// 		return(
	// 			<>
	// 				<h2>Transaction accounts </h2>
	// 				{transactionOutput.accounts?.map((account, i) => (
	// 					<Collapsible label = {account.account.address}>
	// 						<p> postBalances: {transactionOutput.meta.postBalances[i]}</p>
	// 						<p> preBalances: {transactionOutput.meta.preBalances[i]}</p>
	// 						<p> Difference :{transactionOutput.meta.postBalances[i] - transactionOutput.meta.preBalances[i]} </p>
	// 					</Collapsible>
	// 				))}
	// 				<Button onClick={() => {navigate("/input", { state: {}})}}>Go Back</Button>
	// 			</>
	// 		)
	// 	}
	// }

	/**
	 * this function will fetch data from the api endpoint (/fin_transaction)
	 * and populate the backwardsTraceInfo object
	 * @param {*} n transaction hash 
	 */
	async function getTraceBack(n) {

		const backwardsTraceOBJ = await getBackwardsTrace(n);
		const backwardsTraceJSON = JSON.parse(backwardsTraceOBJ);
		
		setBackwardsTraceInfo(backwardsTraceJSON);
		if(backwardsTraceJSON === "Bad Request") {
			setIsLoading(false);
			setInvalidRequest(true);
		}
	}

	async function getTraceForwards(n) {
		const forwardsTraceOBJ = await getForwardsTrace();
		const forwardsTraceJSON = JSON.parse(forwardsTraceOBJ);

		setForwardsTraceInfo(forwardsTraceJSON);
		if(forwardsTraceJSON === "Bad Request") {
			setIsLoading(false);
			setInvalidRequest(true);
		}
	}


	useEffect(async ()=>{
		setIsLoading(true);
		getTraceBack(state);
	}, [])

	return (
		<div>
			{isInvalidRequest &&
				<div>
				<Alert color="danger" className="errorBox">
					This transaction is INVALID, please try again
				</Alert>
				<Button onClick={() => {navigate("/input", { state: {}})}}>Go Back</Button>
			</div>
			}
			<div>
				
				{typeof backwardsTraceInfo === 'undefined' ? 
					<Spinner>
						Loading...
					</Spinner>
				:(
					<div>
						<h1>Backwards Trace:</h1>
						{backwardsTraceInfo.Accounts.map((account, i) => {
							return (
                                <Collapsible key={i} label={<a href={`https://explorer.solana.com/address/${account}`} target="_blank" >Layer {i}: {account}</a>}>
                                    <a href={`https://explorer.solana.com/tx/${backwardsTraceInfo.Transactions[i]}`} target="_blank">{backwardsTraceInfo.Transactions[i]}</a>
                                </Collapsible>
						)})}
						
					</div>
				)}

				{typeof forwardsTraceInfo === 'undefined' ? 
					<></>
				:(
					<div>
						<h1>Forwards Trace:</h1>
						{forwardsTraceInfo.Accounts.map((account, i) => {
							return (
                                <Collapsible key={i} label={<a href={`https://explorer.solana.com/address/${account}`} target="_blank" >Layer {i}: {account}</a>}>
                                    <a href={`https://explorer.solana.com/tx/${forwardsTraceInfo.Transactions[i]}`} target="_blank">{forwardsTraceInfo.Transactions[i]}</a>
                                </Collapsible>
						)})}
						
					</div>
				)}
			</div>
		</div>
  )
}
