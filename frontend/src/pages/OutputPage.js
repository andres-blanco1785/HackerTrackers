import React from 'react'

export function OutputPage(props){
    
  return (
    <div>
      OutputPage
      {props.transactionOutput.accounts &&
            <div>
            {props.transactionOutput.accounts.map((account, index ) => {
                return (
                    <div key={index}>
                        account # {index}: {account.account.address}
                    </div>
                )
            })}
            </div>
        }
    </div>
  )
}
