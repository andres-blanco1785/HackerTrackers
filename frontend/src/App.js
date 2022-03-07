import React, {useEffect, useState} from "react";
import './App.css';
import Collapsible from "./Collapsible";


async function getTransactionInfo(n) {
  
  let sequence = await fetch(`http://127.0.0.1:5000/transaction/${n}`)
      .then(response => response.json())
      .then(result => { return result});


  console.log('sequence',sequence)

  return sequence;
}

function App() {

  const [transactionInput, setTransactionInput] = useState();
  const [transactionOutput, setTransactionOutput]= useState('');
  const [open, setOpen] = useState(true);
  const [listAccNum, setlistAccNum] = useState();


  function onButtonClick()
  {
      getTransactionInfo(transactionInput)
          .then((transactionJson)=>{
               setTransactionOutput(transactionJson)});
      // if(typeof transactionOutput.accounts !== 'undefined')
      // {
      //     setlistAccNum()
      // }



      //     .then(transactionResult => JSON.stringify(transactionResult, null, 2))
      //     .then((TransactionOutputString)=>{
      //     setTransactionOutput(TransactionOutputString)})
      // ;
  }
  useEffect(()=>{
      printTransactionInfo()
      },[transactionOutput]
  )

  function printTransactionInfo()
  {

      console.log("transactionOutput", transactionOutput);


      if(typeof transactionOutput.accounts !== 'undefined')
      {
          let numAccounts = transactionOutput.accounts.length;
          console.log(numAccounts );

          return(
              <>
                  <h2>Transaction accounts </h2>
                    {transactionOutput.accounts?.map((account, i) => (
                        <Collapsible label = {account.account.address}>
                            <p> postBalances: {transactionOutput.meta.postBalances[i]}</p>
                            <p> preBalances: {transactionOutput.meta.preBalances[i]}</p>
                            <p> Difference :{transactionOutput.meta.postBalances[i] - transactionOutput.meta.preBalances[i]} </p>
                        </Collapsible>

                    ))}

              </>



          )

      }





  }



  
  return (
    <div className="App">
      <input type="text"
             onChange={(e) => setTransactionInput(e.target.value)}
             value={transactionInput}/>
      <button onClick={onButtonClick}>transactionID</button>


      <p>{printTransactionInfo()}</p>

    </div>
  );
}

export default App;
