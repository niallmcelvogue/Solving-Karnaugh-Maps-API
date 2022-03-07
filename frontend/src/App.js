import logo from './logo.svg';
import './App.css';
import React, {useState, useEffect} from "react";
import axios from "axios";
import 'bootstrap/dist/css/bootstrap.min.css'
function App() {
    const [input, setInput, response] = useState('')

     const addInputHandler = () => {
        console.log(input)
         axios.post('http://localhost:8000/solve', {
            'input': input}, {withCredentials:true})
            .then(function(response) {
                console.log(response.data)
                response = response.data
            })
         }
  return (
    <div className="App">
        <input className={"mb-2 form-control titleIn"} onChange={event => setInput(event.target.value)}
        placeholder={'Input'}/>
        <button className={"btn btn-outline-primary mx-2"} style={{'borderRadius':'50px', 'fontWeight':'Bold'}} onClick={addInputHandler}>Solve</button>
        <h5 className={'card text-white bg-dark mb-3'}>Output</h5>
        <div>
        </div>
    </div>
  );
}

export default App;
