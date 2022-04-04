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
          CxegPrfn2ge5dNiQberUrQJkHCcimeR4VXkeawcFBBka
        </>
      ),
    },
      style:{
        background: '#cfb357',
        color: '#2f4c59',
        border: '1px solid #222138',
        width: 350,
      },
    position: { x: 250, y: 0 },
  },
  {
    id: '2',
    data: {
      label: (
        <>
          CxegPrfn2ge5dNiQberUrQJkHCcimeR4VXkeawcFBBka
        </>
      ),
    },
    position: { x: 100, y: 100 },
  },
];

export const initialEdges = [
  { id: 'e1-2', source: '1', target: '2', label: '2zCz2GgSoSS68eNJENWrYB48dMM1zmH8SZkgYneVDv2G4gRsVfwu5rNXtK5BKFxn7fSqX9BvrBc1rdPAeBEcD6Es' },

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
	const [isLoading, setIsLoading] = useState(true);
	const [isInvalidRequest, setInvalidRequest] = useState(false);
	const [backwardsTraceInfo, setBackwardsTraceInfo] = useState(JSON.parse(localStorage.getItem('backwardsTraceInfo')));
	const [forwardsTraceInfo, setForwardsTraceInfo] = useState(JSON.parse(localStorage.getItem('forwardsTraceInfo')));


	const [Bnodes, setBNodes, onBNodesChange] = useNodesState([]);
	const [Bedges, setBEdges, onBEdgesChange] = useEdgesState([]);
	const onBConnect = (params) => setBEdges((eds) => addEdge(params, eds));

    const [Fnodes, setFNodes, onFNodesChange] = useNodesState([]);
	const [Fedges, setFEdges, onFEdgesChange] = useEdgesState([]);
	const onFConnect = (params) => setFEdges((eds) => addEdge(params, eds));


    const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
    const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);
    const onConnect = (params) => setEdges((eds) => addEdge(params, eds));


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

    function getGraphNodesEdgeBackwards()
    {
        console.log("backwardsTraceInfo",backwardsTraceInfo);
        let backwardsNodes = [];
        let backwardsEdges = [];
        let x = 100;
        let y = 0;
        for(let i = 0; i < backwardsTraceInfo.Accounts.length; i++)
        {
            backwardsNodes[i] = Object();
            backwardsNodes[i].id = i.toString();
            backwardsNodes[i].data = Object();
            backwardsNodes[i].data.label = <a href={`https://explorer.solana.com/address/${backwardsTraceInfo.Accounts[i]}`} target="_blank" >Layer {i}: {backwardsTraceInfo.Accounts[i]}</a>;
            backwardsNodes[i].position = {x,y};
            backwardsNodes[i].style =
                {
                    background: '#549c9c',
                    color: '#2f4c59',
                    border: '1px solid #222138',
                    width: 350,
                };

            y = y + 250;
            if(i !== backwardsTraceInfo.Accounts.length - 1)
            {
                backwardsEdges[i] = Object();
                backwardsEdges[i].id = "e"+ i.toString() + "-" + (i+1).toString();
                backwardsEdges[i].source = i.toString();
                backwardsEdges[i].target = (i+1).toString();
                // backwardsEdges[i].animated = true;
                backwardsEdges[i].label= <a href={`https://explorer.solana.com/tx/${backwardsTraceInfo.Transactions[i+1]}`} target="_blank">{backwardsTraceInfo.Transactions[i+1]}</a>;

            }
        }

        setBNodes(backwardsNodes);
        setBEdges(backwardsEdges);
    }

    function getGraphNodesEdgeForwards()
    {
        console.log("forwardsTraceInfo",forwardsTraceInfo);
        let forwardsNodes = [];
        let forwardsEdges = [];
        let x = 0;
        let x0 = 20;
        let x1 = 20;
        let x2 = 20;
        let x3 = 20;
        let y = 100;
        let map = {};
        let position;

        for(let i = 0 ; i< forwardsTraceInfo.Transactions.length; i++)
        {
            forwardsEdges[i] = Object();
            forwardsEdges[i].id = i;
            forwardsEdges[i].source = forwardsTraceInfo.Transactions[i][1];
            forwardsEdges[i].target = forwardsTraceInfo.Transactions[i][2];
            forwardsEdges[i].label= <a href={`https://explorer.solana.com/tx/${forwardsTraceInfo.Transactions[i][0]}`} target="_blank">{forwardsTraceInfo.Transactions[i][0]}</a>;
            map[forwardsTraceInfo.Transactions[i][1]] = forwardsTraceInfo.Transactions[i][3];
            map[forwardsTraceInfo.Transactions[i][2]] = forwardsTraceInfo.Transactions[i][3]+1;
        }

        console.log("map", map);

        for(let i = 0; i < forwardsTraceInfo.Accounts.length; i++)
        {
            if(map[forwardsTraceInfo.Accounts[i]] === 1)
            {
                y = 10;
                x = x0;
                position = {x,y};
                x0 = x0 + 300;
            }
            else if(map[forwardsTraceInfo.Accounts[i]] === 2)
            {
                y = 250;
                x = x1;
                position = {x,y};
                x1 = x1 + 300;
            }
            else if(map[forwardsTraceInfo.Accounts[i]] == 3)
            {
                y = 500;
                x = x2;
                position = {x,y};
                x2 = x2 + 300;
            }
            else
            {
                y = 750;
                x = x3;
                position = {x,y};
                x3 = x3 + 150;
            }

            forwardsNodes[i] = Object();
            forwardsNodes[i].id = forwardsTraceInfo.Accounts[i];
            forwardsNodes[i].data = Object();
            forwardsNodes[i].data.label = <a href={`https://explorer.solana.com/address/${forwardsTraceInfo.Accounts[i]}`} target="_blank" >Layer {map[forwardsTraceInfo.Accounts[i]]}: {forwardsTraceInfo.Accounts[i]}</a>;
            forwardsNodes[i].position = position;
            forwardsNodes[i].style =
                {
                    background: '#549c9c',
                    color: '#2f4c59',
                    border: '1px solid #222138',
                    width: 350,
                };

        }
        console.log("console.log(forwardsNodes);",forwardsNodes);
        console.log("console.log(forwardsEdges);",forwardsEdges);
        setFNodes(forwardsNodes);
        setFEdges(forwardsEdges);


    }

	useEffect(async () => {

		getTraceInformation(state);
	},[]);

    useEffect (() => {
		if(!isInvalidRequest && backwardsTraceInfo )
            getGraphNodesEdgeBackwards();
	}, [isInvalidRequest,backwardsTraceInfo ]);

    useEffect (() => {
		if(!isInvalidRequest  && forwardsTraceInfo )
            getGraphNodesEdgeForwards();
	}, [isInvalidRequest, forwardsTraceInfo ]);

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
				{((forwardsTraceInfo === null) || (backwardsTraceInfo === null)) ?
					<Spinner>
					Loading...
					</Spinner>
				:(
					<div>
						<h1>Forwards Trace:</h1>
                        <Flow nodes={Fnodes} edges={Fedges} onNodesChange={onFNodesChange} onConnect={onFConnect} onEdgesChange={onFEdgesChange}>
                        </Flow>
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
