import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router';
import { Alert, Button, Spinner } from 'reactstrap';
import { useLocation } from "react-router-dom";
import { getBackwardsTrace } from '../utilities/Utilities';
import { getForwardsTrace } from '../utilities/Utilities';
import Collapsible from "../components/Collapsible";
import Flow from "../components/FlowGraph";
import './OutputPage.css';
import { MarkerType } from 'react-flow-renderer';
import ReactFlow, {
  addEdge,
  MiniMap,
  Controls,
  Background,
  useNodesState,
  useEdgesState,
} from 'react-flow-renderer';

export const initialNodes = [
  {
    id: '1',
    type: 'input',
    data: {
      label: (
        <>
          Welcome to <strong>React Flow!</strong>
        </>
      ),
    },
    position: { x: 250, y: 0 },
  },
  {
    id: '2',
    data: {
      label: (
        <>
          This is a <strong>default node</strong>
        </>
      ),
    },
    position: { x: 100, y: 100 },
  },
];

export const initialEdges = [
  { id: 'e1-2', source: '1', target: '2', label: 'this is an edge label' },

];


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
    const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
    const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);
    const onConnect = (params) => setEdges((eds) => addEdge(params, eds));

	const [Bnodes, setBNodes, onBNodesChange] = useNodesState([]);
	const [Bedges, setBEdges, onBEdgesChange] = useEdgesState([]);
	const onBConnect = (params) => setBEdges((eds) => addEdge(params, eds));

    const [Fnodes, setFNodes, onFNodesChange] = useNodesState([]);
	const [Fedges, setFEdges, onFEdgesChange] = useEdgesState([]);
	const onFConnect = (params) => setFEdges((eds) => addEdge(params, eds));

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

    function getGraphNodesEdge()
    {
        console.log("forwardsTraceInfo",forwardsTraceInfo);
        console.log("backwardsTraceInfo",backwardsTraceInfo);
        let backwardsNodes = [];
        let backwardsEdges = [];
        let x = 0;
        let y = 0;
        for(let i = 0; i < backwardsTraceInfo.Accounts.length; i++)
        {
            backwardsNodes[i] = Object();
            backwardsNodes[i].id = i.toString();
            backwardsNodes[i].data = Object();
            backwardsNodes[i].data.label = <a href={`https://explorer.solana.com/address/${backwardsTraceInfo.Accounts[i]}`} target="_blank" >Layer {i}: {backwardsTraceInfo.Accounts[i]}</a>;
            backwardsNodes[i].position = {x,y};
            y = y + 250;
            if(i !== backwardsTraceInfo.Accounts.length - 1)
            {
                backwardsEdges[i] = Object();
                backwardsEdges[i].id = "e"+ i.toString() + "-" + (i+1).toString();
                backwardsEdges[i].source = i.toString();
                backwardsEdges[i].target = (i+1).toString();
                // backwardsEdges[i].animated = true;
                // backwardsEdges[i].label= <a href={`https://explorer.solana.com/tx/${backwardsTraceInfo.Transactions[i+1]}`} target="_blank">{backwardsTraceInfo.Transactions[i+1]}</a>;

            }
        }

        setBNodes(backwardsNodes);
        setBEdges(backwardsEdges);
        console.log("BNodes",Bnodes);
        console.log("BEdges",Bedges);
    }

	useEffect(async () => {
		getTraceInformation(state);
	},[]);

    useEffect (() => {
		if(!isInvalidRequest && backwardsTraceInfo && forwardsTraceInfo )
            getGraphNodesEdge();
	}, [isInvalidRequest,backwardsTraceInfo, forwardsTraceInfo ]);



	return (
		<div>
			{/*<Flow nodes={nodes} edges={edges} onNodesChange={onNodesChange} onConnect={onConnect} onEdgesChange={onEdgesChange}>*/}
			{/*</Flow>*/}
			{isInvalidRequest ?
				<div>
					<Alert color="danger" className="errorBox">
						This transaction is INVALID, please try again
					</Alert>
					<Button onClick={() => {navigate("/input", { state: {}})}}>Go Back</Button>
				</div>
			:
			<div>
				{((typeof forwardsTraceInfo === 'undefined') || (typeof backwardsTraceInfo === 'undefined')) ?
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
                        <Flow nodes={Bnodes} edges={Bedges} onNodesChange={onBNodesChange} onConnect={onBConnect} onEdgesChange={onBEdgesChange}>
                        </Flow>

						{/*{backwardsTraceInfo.Accounts.map((account, i) => {*/}
						{/*	return (*/}
						{/*		<Collapsible key={i} label={<a href={`https://explorer.solana.com/address/${account}`} target="_blank" >Layer {i}: {account}</a>}>*/}
						{/*			<a href={`https://explorer.solana.com/tx/${backwardsTraceInfo.Transactions[i]}`} target="_blank">{backwardsTraceInfo.Transactions[i]}</a>*/}
						{/*		</Collapsible>*/}
						{/*)})}*/}
					</div>
				)}
			</div>
			}
		</div>
  )
}
