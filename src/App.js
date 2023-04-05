import React from 'react';
import { BrowserRouter as Router, Routes, Route} from "react-router-dom";
import Server  from './server'
import Client from './client';

export default function App() {
  return(
    <Router>
      <Routes>
        <Route exact path="/" element={<Client/>} />
        <Route path="/client" element={<Client/>} />
        <Route path="/server" element={<Server/>} />
      </Routes>
    </Router>
  );
}
