import React, { useEffect, useState } from 'react';
import { getBlocklistedAccounts } from '../utilities/Utilities.js';
export default function BlocklistPage(props) {

    const [blocklistedAccounts, setblocklistedAccounts] = useState({});

    useEffect(() => {
        getBlocklistedAccounts();
    });

    return (
        <div>
            
        </div>
    )
}
