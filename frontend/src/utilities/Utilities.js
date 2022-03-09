const backendURL = 'http://127.0.0.1:5000';

export async function getTransactionInfo(n) {
    let sequence = await fetch(`${backendURL}/transaction/${n}`)
        .then(response => response.json())
        .then(result => { return result});
  
  
    console.log('sequence',sequence)
  
    return sequence;
  }