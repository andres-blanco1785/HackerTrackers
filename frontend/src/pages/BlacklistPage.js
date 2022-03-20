import React, { useEffect, useState } from 'react';
import { getBlacklistedAccounts } from '../utilities/Utilities.js';

export default function BlocklistPage(props) {

    const [blacklistedAccounts, setBlacklistedAccounts] = useState([]);

    useEffect(() => {
        setBlacklistedAccounts(getBlacklistedAccounts());
        console.log()
    }, []);

    return (
        <div>
            this is a test
            {blacklistedAccounts.map((account, i) => {
                <p>account</p>
            })}
        </div>
    )
}
