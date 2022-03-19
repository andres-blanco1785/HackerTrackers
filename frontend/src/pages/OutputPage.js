import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router';
import { Alert, Button } from 'reactstrap';
import { useLocation } from "react-router-dom";
import { getBackwardsTrace, getTransactionInfo } from '../utilities/Utilities';
import Collapsible from "../components/Collapsible";
import './OutputPage.css';

export default function OutputPage(props) {
	
	const [transactionOutput, setTransactionOutput] = useState({});
	const [isLoading, setIsLoading] = useState(true);
	const [isInvalidRequest, setInvalidRequest] = useState(false);
	const [backwardsTraceInfo, setBackwardstraceInfo] = useState({});

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
					<Button onClick={() => {navigate("/input", { state: {}})}}>Go Back</Button>
				</>
			)
		}
	}

	async function testing(n) {

		const transactionJSON = await getBackwardsTrace(n)
			.then(setIsLoading(false));

		setBackwardstraceInfo(transactionJSON);
		if(transactionJSON === "Bad Request") {
			setIsLoading(false);
			setInvalidRequest(true);
		}


		// console.log('transactionJSON: ', transactionJSON);
	}

	useEffect(()=>{
		testing(state);
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
					{/* {backwardsTraceInfo.accounts.map((account, i) => {
						<p key={i}>
							account
						</p>
					})} */}
				</div>
			}
		</div>
  )
}
