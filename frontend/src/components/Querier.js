import React, { useState, useEffect } from 'react';


export default function Querier() {
    const [data, setData] = useState("click here")
    const [playerData, setPlayerData] = useState([])
    const [formSub, setFormSub] = useState("")
    const header = ['Player', 'Pos', 'Tm', 'PassingYds', 'PassingTD', 'Int', 'PassingAtt',
    'Cmp', 'RushingAtt', 'RushingYds', 'RushingTD', 'Rec', 'Tgt', 'ReceivingYds',
    'ReceivingTD', 'FL', 'PPRFantasyPoints', 'StandardFantasyPoints', 'HalfPPRFantasyPoints']

    function getPlayers(player) {
        const url = 'http://localhost:5000/players/' + player
        fetch(url, {mode: "cors", method: 'GET'})
           .then(response => response.json())
           .then(json => {

               const l = []
               for (let i = 1; i < 17; i++) {
                   l.push(json[i] + "  ")
                }
                setPlayerData(l)
           })
           .catch(err => {
               console.log(err)
          })
     }


    

    async function mySubmit(e){
        e.preventDefault()

        const players = getPlayers(formSub)
    }

    function change(e) {
        setFormSub(e.target.value)
    }
    
      

    return (
        <div className="querier">
            <form onSubmit={mySubmit}>
            <label>
                Player:
                <input type="text" name="name" onChange={change} />
            </label>
            <input type="submit" />
            </form>
            <div className="display-data">
                <p> {header + "   "}</p>
                <ol>
                {playerData.map(data => (
                    <li>{data}</li>
                ))}
                </ol>
                </div>
        </div>
    )
}