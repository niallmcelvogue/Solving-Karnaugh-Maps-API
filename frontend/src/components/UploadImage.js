import React, {useState} from 'react';
import ImageUploader from 'react-images-upload';
import {toast} from 'react-toastify';
import axios from 'axios';
import {PITable} from "./Table/PrimeImplicantTable";

const UploadImage = props => {
    const [data, setData] = useState([])
    const [postImage, setPostImage] = useState({myFile: '',})
    const [response, setResponse] = useState('')
    const [showButton, setShowButton] = useState(false)
    const [showSolutionArea, setShowSolutionArea] = useState(false)
    const Error = () => toast.error('An error has occurred')

    const convertBase64 = (file) => {
    return new Promise((resolve, reject) => {
      const fileReader = new FileReader();
      fileReader.readAsDataURL(file)
      fileReader.onload = () => {
        resolve(fileReader.result);
      }
      fileReader.onerror = (error) => {
        reject(error);
      }
    })
  }

   const handleFileUpload = async (e) => {
        if(typeof e[0] != 'undefined') {
            const file = e[0]
            const base64 = await convertBase64(file)
            setPostImage({...postImage, myFile: base64})
            setShowButton(true)
        }
        else {
            setResponse('')
            setPostImage({...postImage, myFile: ''})
            setShowButton(false)
        }
        setResponse('')
       setShowSolutionArea(false)
  }

  const addInputHandler = (e) => {
        console.log(e.target.id)
        axios.post('http://localhost:8000/extract', {
            'input': postImage.myFile,
            'type': e.target.id
        }, {withCredentials: true})
            .then(response => {
                let data = response.data[1]
                console.log(data)
                if (response != null) {
                    setResponse(response.data[0].optimisedSolution)
                    setData(response.data[1])
                } else {
                    Error()
                }
                setShowSolutionArea(true)
            })
            .catch(error =>{
                console.log(error)
                Error()
                }
            )
    }


function ShowSolveButton() {
    return (
        <>
                <button id="SOP" className={"btn btn-outline-primary mx-2"}
                    style={{'borderRadius': '50px', 'fontWeight': 'Bold', 'marginBottom': '10px'}}
                    onClick={addInputHandler}>SOP
            </button>
            <button id="POS" className={"btn btn-outline-primary mx-2"}
                    style={{'borderRadius': '50px', 'fontWeight': 'Bold', 'marginBottom': '10px'}}
                    onClick={addInputHandler}>POS
            </button>
            <button id="NAND" className={"btn btn-outline-primary mx-2"}
                    style={{'borderRadius': '50px', 'fontWeight': 'Bold', 'marginBottom': '10px'}}
                    onClick={addInputHandler}>NAND
            </button>
            <button id="NOR" className={"btn btn-outline-primary mx-2"}
                    style={{'borderRadius': '50px', 'fontWeight': 'Bold', 'marginBottom': '10px'}}
                    onClick={addInputHandler}>NOR
            </button>
        </>
            )
}

return (
    <div>
        <div className='col py-3 px-lg-5 border bg-light'>
          <ImageUploader
          {...props}
          style={{marginTop:'60px'}}
          withIcon={true}
          onChange={(e) => handleFileUpload(e)}
          imgExtension={['.jpg', '.png']}
          maxFileSize={5242880}
          singleImage={true}
          withPreview={true}
          label={'Max file size: 5mb, accepted: jpg | png'}
        />
            {showButton ? <ShowSolveButton/> : null}
        </div>
        <div className='col py-3 px-lg-5 border bg-light'>
            {showSolutionArea ? <h5 className={'card text-white bg-dark mb-3'}>Optimised Solution</h5> : null}
            <h4>{response}</h4>
        </div>
    </div>
  );
};

export default UploadImage;