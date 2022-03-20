import React, { useEffect, useState } from 'react';
import { getBlocklistedAccounts } from '../utilities/Utilities.js';

export default function BlocklistPage(props) {

    const [blocklistedAccounts, setBlocklistedAccounts] = useState({});

    useEffect(async () => {
        const accounts = await getBlocklistedAccounts();
        setBlocklistedAccounts(JSON.parse(accounts));
    }, []);

    useEffect(() => {
        console.log("blacklistedAccounts: ", blocklistedAccounts.blocklistedAccounts);
    }, [blocklistedAccounts]);

    return (
        <div>
            this is a test
            {/* {(typeof blocklistedAccounts !== 'undefined') && 
            (
                blocklistedAccounts.blocklistedAccounts.map(({ account, transactions}) => {
                    <div>
                        <p key={account}>{account} : {transactions} </p>
                    </div>
                })
            )
            } */}
        </div>
    )
}
