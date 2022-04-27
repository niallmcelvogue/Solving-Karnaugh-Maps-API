import React, {useState, useEffect} from "react"
import axios from "axios";
import 'bootstrap/dist/css/bootstrap.min.css'
import 'react-toastify'
import {toast} from "react-toastify"
import 'react-toastify/dist/ReactToastify.css'


function Manual() {
    const [input, setInput] = useState('')
    const [noVar, setNoVar] = useState('')
    const [response, setResponse] = useState('')
    const [showSolutionArea, setShowSolutionArea] = useState(false)
    const Error = () => toast.error("An error has occurred")

    useEffect(() => {
        console.log(response)
    }, [response])

    const addInputHandler = (e) => {
        axios.post('http://localhost:8000/solve', {
            'input': input,
            'noVar': noVar,
            'type': e.target.id
        }, {withCredentials: true})
            .then(response => {
                console.log(response)
                if (response != null) {
                    setResponse(response.data.output[0])
                    setShowSolutionArea(true)
                } else {
                    Error()
                }
            })
    }

    function showSolution() {
        return (
            <div className='col py-3 px-lg-5 border bg-light' style={{marginTop: '60px'}}>
                <h5 className={'card text-white bg-dark mb-3'}>Output</h5>
                <div className='col py-3 px-lg-5 border bg-light' style={{marginTop: '60px'}}>
                    <h4>Prime Implicants: {response.PI}</h4>
                </div>
                <div className='col py-3 px-lg-5 border bg-light' style={{marginTop: '60px'}}>
                    <h4>Essential Prime Implicants: {response.EPI}</h4>
                </div>
                <div className='col py-3 px-lg-5 border bg-light' style={{marginTop: '60px'}}>
                    <h4>Optimised Solution: {response.optimisedSolution}</h4>
                </div>
            </div>
        )
    }
    return (
        <>
        <div className='col py-3 px-lg-5 border bg-light' style={{marginTop:'60px'}}>
             <input className={"mb-2 form-control titleIn"} onChange={event => setNoVar(event.target.value)}
                   placeholder={'Number of Variables'}/>
            <input className={"mb-2 form-control titleIn"} onChange={event => setInput(event.target.value)}
                   placeholder={'Input'}/>
            <button id = "SOP"className={"btn btn-outline-primary mx-2"}
                    style={{'borderRadius': '50px', 'fontWeight': 'Bold', 'marginBottom': '10px'}}
                    onClick={addInputHandler}>SOP
            </button>
            <button id ="POS"className={"btn btn-outline-primary mx-2"}
                    style={{'borderRadius': '50px', 'fontWeight': 'Bold', 'marginBottom': '10px'}}
                    onClick={addInputHandler}>POS
            </button>
            <button id = "NAND" className={"btn btn-outline-primary mx-2"}
                    style={{'borderRadius': '50px', 'fontWeight': 'Bold', 'marginBottom': '10px'}}
                    onClick={addInputHandler}>NAND
            </button>
            <button id = "NOR" className={"btn btn-outline-primary mx-2"}
                    style={{'borderRadius': '50px', 'fontWeight': 'Bold', 'marginBottom': '10px'}}
                    onClick={addInputHandler}>NOR
            </button>
            </div>
            <div className='col py-3 px-lg-5 border bg-light' style={{marginTop:'60px'}}>
                {showSolutionArea ? showSolution() : null}
            </div>
            </>
    );
}

export default Manual;
