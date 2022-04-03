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
	 * if isInvalidRequest is true, it will render an alert to the user that the input is invalid
	 */
	const [isInvalidRequest, setInvalidRequest] = useState(false);
	const [backwardsTraceInfo, setBackwardsTraceInfo] = useState(JSON.parse(localStorage.getItem('backwardsTraceInfo')));
	const [forwardsTraceInfo, setForwardsTraceInfo] = useState(JSON.parse(localStorage.getItem('forwardsTraceInfo')));

	/**
	 * this function will fetch data from the api endpoints (/fin_transaction & /forwards-trace)
	 * and populate the backwardsTraceInfo object
	 * @param {*} n transaction hash 
	 */
	async function getTraceInformation(n) {
		const forwardsTraceOBJ = await getForwardsTrace(n);
		const backwardsTraceOBJ = await getBackwardsTrace(n);
		
		if((forwardsTraceOBJ === "Bad Request") || (backwardsTraceOBJ === "Bad Request")) {
			setInvalidRequest(true);
			return
		}
		
		const backwardsTraceJSON = JSON.parse(backwardsTraceOBJ);
		const forwardsTraceJSON = JSON.parse(forwardsTraceOBJ);
		setForwardsTraceInfo(forwardsTraceJSON);
		setBackwardsTraceInfo(backwardsTraceJSON);
		localStorage.setItem('forwardsTrace', JSON.stringify(forwardsTraceJSON));
		localStorage.setItem('backwardsTrace', JSON.stringify(backwardsTraceJSON));
		
	}

	useEffect(async () => {
		if(((localStorage.getItem('forwardsTrace') === null) && 
			(localStorage.getItem('backwardsTrace') === null)) &&
			(state == localStorage.getItem('transactionInput'))) {
			getTraceInformation(state);
		} else {
			setForwardsTraceInfo(JSON.parse(localStorage.getItem('forwardsTrace')));
			setBackwardsTraceInfo(JSON.parse(localStorage.getItem('backwardsTrace')));
		}
	}, []);

	return (
		<div>
			{isInvalidRequest ?
				<div>
					<Alert color="danger" className="errorBox">
						This transaction is INVALID, please try again
					</Alert>
					<Button onClick={() => {navigate("/input", { state: {}})}}>Go Back</Button>
				</div>
			:
			<div>
				{((forwardsTraceInfo === null) || (backwardsTraceInfo === null)) ?
					<Spinner>
					Loading...
					</Spinner>
				:(
					<div>
						<h1>Forwards Trace:</h1>
						{forwardsTraceInfo.Accounts.map((account, i) => {
							return (
								<Collapsible key={i} label={<a href={`https://explorer.solana.com/address/${account}`} target="_blank" >Layer {i}: {account}</a>}>
									<a href={`https://explorer.solana.com/tx/${forwardsTraceInfo.Transactions[i]}`} target="_blank">{forwardsTraceInfo.Transactions[i]}</a>
								</Collapsible>
						)})}
						<h1>Backwards Trace:</h1>
						{backwardsTraceInfo.Accounts.map((account, i) => {
							return (
								<Collapsible key={i} label={<a href={`https://explorer.solana.com/address/${account}`} target="_blank" >Layer {i}: {account}</a>}>
									<a href={`https://explorer.solana.com/tx/${backwardsTraceInfo.Transactions[i]}`} target="_blank">{backwardsTraceInfo.Transactions[i]}</a>
								</Collapsible>
						)})}
					</div>
				)}
			</div>
			}
		</div>
  )
}
