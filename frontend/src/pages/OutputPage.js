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
	const [backwardsTraceInfo, setBackwardsTraceInfo] = useState(undefined);
	const [forwardsTraceInfo, setForwardsTraceInfo] = useState(undefined);

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
		
	}

	useEffect(async () => {
		getTraceInformation(state);
	});

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
				{((typeof forwardsTraceInfo === 'undefined') && (typeof backwardsTraceInfo === 'undefined')) ? 
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
