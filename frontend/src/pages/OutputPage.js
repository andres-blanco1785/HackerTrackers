import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router';
import { Alert, Button } from 'reactstrap';
import { useLocation } from "react-router-dom";
import { getBackwardsTrace } from '../utilities/Utilities';
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
	const [backwardsTraceInfo, setBackwardsTraceInfo] = useState({});
  
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
	async function getTrace(n) {

		const transactionJSON = await getBackwardsTrace(n)
			.then(setIsLoading(false));

		setBackwardsTraceInfo(transactionJSON);
		if(transactionJSON === "Bad Request") {
			setIsLoading(false);
			setInvalidRequest(true);
		}

		// console.log('transactionJSON: ', transactionJSON);
	}

	useEffect(()=>{
		getTrace(state);
	}, [])

	return (
		<div>
			{isLoading &&
				<p>LOADING</p>
			}
			{isInvalidRequest &&
				<div>
				<Alert color="danger" className="errorBox">
					This transaction is INVALID, please try again
				</Alert>
				<Button onClick={() => {navigate("/input", { state: {}})}}>Go Back</Button>
			</div>
			}
			{(!isLoading && (backwardsTraceInfo !== null) && (backwardsTraceInfo !== "Bad Request")) && 
				<div>
					<h1>Accounts Assosiated:</h1>
					{/* TODO: accounts and transactions need to be mapped
					{backwardsTraceInfo.accounts.map((account, i) => {
						<p key={i}>
							account
						</p>
						})} 
					*/}
				</div>
			}
		</div>
  )
}
