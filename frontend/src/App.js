import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css'
import 'react-toastify'
import {ToastContainer} from "react-toastify"
import 'react-toastify/dist/ReactToastify.css'
import {
  BrowserRouter,
  Routes,
  Route,
} from "react-router-dom";
import Home from './Home'
import Navigation from "./components/Navigation";
import Manual from "./components/Manual";
import UploadImage from "./components/UploadImage";
import {MyTable} from "./components/Table/TruthTable"
import PITable from "./components/Table/PrimeImplicantTable";

function App() {
    return(
        <BrowserRouter>
            <div className={"App"}>
                <ToastContainer closeButton={false} position="top-center" />
                <Navigation/>
                <Routes>
                    <Route path ='/Manual' element={<Manual/>}/>
                    <Route path ='/upload' element={<UploadImage/>}/>
                    <Route path ='/table' element={<MyTable/>}/>
                    <Route path = '/' element={<Home/>}/>
                </Routes>
            </div>
        </BrowserRouter>
    )
}

export default App;
