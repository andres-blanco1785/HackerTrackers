const backendURL = 'http://127.0.0.1:5000';

export async function getTransactionInfo(n) {
    let sequence = await fetch(`${backendURL}/transaction/${n}`)
        .then(response => response.json())
        .then(result => { return result});
  
    return sequence;
}

export async function getBackwardsTrace(n) {
    let trace = await fetch(`${backendURL}/fin_transaction/${n}`)
        .then(response => response.text())
        .then(data => { return data });
    return trace
}

// export async function getBlocklistedAccounts() {
//     return 
// }