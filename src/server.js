import React, {useState, useEffect} from 'react';
import './App.css';
import axios from "axios";

export default function Server() {
  const [users,setUsers] = useState(0);
  const [output, setOutput] = useState();
  const [result, setResult] = useState();
  const [signs, setSigns] = useState();
  const [reset, setReset] = useState();

  const handleReset = () => {
    setOutput();
    setResult();
    setSigns();
    axios.get('http://localhost:5000/reset', {
    })
    .then(response => {
      setReset(response.data);
    })
    .catch(error => {
        console.error(error);
    });
  };
  
  const handleSign = () => {
    setOutput();
    setResult();
    setReset();
    axios.get('http://localhost:5000/aggregate-sign', {
    })
    .then(response => {
      setSigns(response.data);
      console.log(response.data);
    })
    .catch(error => {
        console.error(error);
    });
  };

  const handleVerify = () => {
    setReset();
    setResult();
    if(signs?.length == 0)return;
    axios.get('http://localhost:5000/aggregate-verify', {
    })
    .then(response => {
      setOutput(response.data);
    })
    .catch(error => {
        console.error(error);
    });
  };

  const handleIndividual = () => {
    setReset();
    setOutput();
    if(signs?.length == 0)return;
    axios.get('http://localhost:5000/individual-verify', {
    })
    .then(response => {
      setResult(response.data);
    })
    .catch(error => {
        console.error(error);
    });
  };

  const [showList, setShowList] = useState(false);

  const toggleList = () => {
    setShowList(!showList);
  };

  return (
    <div className="App">
      <div className="title">
        <h1>Half Aggregation of Schnorr Singature</h1>
        
      </div>
      <div className="search-container">
        <div >Generate Aggregate Signature      {          }
          <button className='generate' onClick={handleSign}>AGGREGATE SIGN !</button>
          <br/>
          <br/>
          <div className='note'>
          {signs?.length > 0 &&
          <div className="success-msg">
          <i className="fa fa-check"></i>
          {' '}{"Successfully aggregated "}{signs.length - 1}{" signatures"}
        </div>
        }

        {signs?.length == 0 && <div className="warning-msg">
          <i className="fa fa-warning"></i>
          {' '}{"No signs to aggregate"}</div>}
        </div>

        {/* {signs?.length > 0 && <div><button onClick={toggleList} className='generate'>
          {showList ? 'Hide Signs' : 'Show Signs'}
        </button>
        {showList && (
          <ul>
            {signs?.map((item) => (
              <div key={item}>{item}</div>
            ))}
          </ul>
        )}</div>} */}

          <br/>
          <br/>
        </div>
      </div>

      <div className="search-container">
        <div >Verify Signature      {          }
          <button className='generate' style={{"marginLeft":"45px"}} onClick={handleVerify}>VERIFY AGGREGATE !</button>
          <button className='generate' style={{"marginLeft":"45px"}} onClick={handleIndividual}>VERIFY INDIVIDUAL !</button>
          <br/>
          <br/>
        </div>
      </div>

      {result && <div>
        {result.map((row, rowIndex) => (
        <div key={rowIndex} className='search-container'>
          <div className='note'>
            {row[2] ? <div className='success-msg'><i className="fa fa-check"></i> Roll no {row[0]} Verification for {row[1]} Passed</div> : <div className='warning-msg'><i className="fa fa-warning"></i> Roll no {row[0]} Verification for {row[1]} Failed</div>}
          </div>
        </div>
      ))}
        </div>}

      <div className="main-container">
      {output && <div className='note'>
          {output == "Verification Success" && signs?.length > 0 ? 
          <div className="success-msg">
          <i className="fa fa-check"></i>
          {' '}{output}
        </div> :
          <div className="warning-msg">
          <i className="fa fa-warning"></i>
          {' '}{output == "Verification Success" ? "No signs to verify" : output}
        </div>
            }
        </div>}
      </div>

      <div className='reset'>
        <button className='generate' onClick={handleReset}>RESET</button>
      </div>
    </div>
  );
}

