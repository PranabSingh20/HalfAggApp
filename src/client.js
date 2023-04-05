import React, {useState, useEffect} from 'react';
import './App.css';
import axios from "axios";

export default function Client() {
  const [studentId,setStudentId] = useState(0);
  const [output, setOutput] = useState([]);

  const [file, setFile] = useState(new Blob());
  const [errorMessage, setErrorMessage] = useState("");

  const [result, setResult] = useState();
  
  const handleFileChange = (event) => {
    setResult();
    setFile(event.target.files[0] || new Blob());
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    if(studentId == 0){
      return;
    }
    if(file && file.size == 0){
      return;
    }
    const formData = new FormData();
    formData.append("file", file);
    axios.post('http://localhost:5000/sign', formData, {
        params: {
          studentId: studentId
        }
    })
    .then((response) => {
      setResult(response.data);
    })
    .catch((error) => {
        setErrorMessage("An error occurred: " + error.message);
    });

  };


  const handleKeyPress = e => {
    const pattern = /^[0-9\b]+$/; // Regular expression to match only numbers
    if (!pattern.test(e.key)) {
      e.preventDefault();
    }
  };

  return (
    <div className="App">
      <div className="title">
        <h1>Half Aggregation of Schnorr Singature</h1>
      </div>
      <form onSubmit={handleSubmit} className="xyz">
        <div className="search-container">
          <div >Enter Roll No : { }
            <input className="id" onKeyPress={handleKeyPress} type='text' onChange={e=>{setStudentId(e.target.value);
            setResult();}} value={studentId?studentId :''} required></input> 
            <br/>
            <br/>
          </div>
        </div>
        <div >Select a file to sign   : { }
          <input type="file" onChange={handleFileChange} accept="application/pdf" placeholder="Choose File" required className='file'/>
        </div>
        <br/>
        <button type="submit" className='generate'>SIGN !</button>
        <br/>
        <br/>
        {result && <div className='note'>
          {result == "Successfully signed" ? 
          <div className="success-msg">
          <i className="fa fa-check"></i>
          {' '}{"Successfully signed "}{file.name}{" of roll no "}{studentId}
        </div> :
          <div className="warning-msg">
          <i className="fa fa-warning"></i>
          {' '}{result}
        </div>
            }
        </div>}

            

      </form>
   

      <div className="main-container">

      </div>
    </div>
  );
}

