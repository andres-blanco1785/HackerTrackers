import React, { useEffect, useState } from 'react';
import { Button } from 'reactstrap';
import { useNavigate } from 'react-router';
import Collapsible from '../components/Collapsible.js';
import { getBlacklistedAccounts } from '../utilities/Utilities.js';
import './BlacklistPage.css';

export default function BlacklistPage(props) {

    const navigate = useNavigate();
    const [blacklistedAccounts, setBlacklistedAccounts] = useState([]);

    async function fetchData() {
        const accountsOBJ = await getBlacklistedAccounts();
        const accountsJSON = JSON.parse(accountsOBJ);
        setBlacklistedAccounts(accountsJSON.blacklistedAccounts);
    }

    useEffect(async () => {
        fetchData();
    });

    return (
        <div>
            {(blacklistedAccounts.length === 0) ? 
                <div>
                    <h1>There are no blacklisted accounts currently!</h1>
                    <h2>Help report accounts by tracing fraudulent transactions</h2>
                    <Button onClick={() => {navigate("/input", { state: {}})}}>Go Trace!</Button>
                </div>
            :
                <div>
                    <h1>Blacklisted Accounts:</h1>
                    {blacklistedAccounts.map((obj, i) => {
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
