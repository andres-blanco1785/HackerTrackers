import React, { useEffect, useState } from 'react';
import { Button } from 'reactstrap';
import { useNavigate } from 'react-router';
import Collapsible from '../components/Collapsible.js';
import { getBlocklistedAccounts } from '../utilities/Utilities.js';
import './BlocklistPage.css';

export default function BlocklistPage(props) {

    const [blocklistedAccounts, setBlocklistedAccounts] = useState([]);
    const navigate = useNavigate();

    async function fetchData() {
        const accountsOBJ = await getBlocklistedAccounts();
        const accountsJSON = JSON.parse(accountsOBJ);
        setBlocklistedAccounts(accountsJSON.blacklistedAccounts);
    }

    useEffect(async () => {
        fetchData();
    }, []);

    return (
        <div>
            {(blocklistedAccounts.length === 0) ? 
                <div>
                    <h1>There are no blocklisted accounts currently!</h1>
                    <h2>Help report accounts by tracing fraudulent transactions</h2>
                    <Button onClick={() => {navigate("/input", { state: {}})}}>Go Trace!</Button>
                </div>
            :
                <div>
                    <h1>Blocklisted Accounts:</h1>
                    {blocklistedAccounts.map((obj, i) => {
                        return (
                            <div key={i}>
                                <Collapsible label={<a href={`https://explorer.solana.com/address/${obj.account}`} target="_blank" >{obj.account}</a>}>
                                    <h3> Transactions:</h3>
                                    <a href={`https://explorer.solana.com/tx/${obj.transactions}`} target="_blank">{obj.transactions}</a>
                                    
                                </Collapsible>
                            </div>
                        )
                    })}
                </div>
            }
        </div>
    )
}
