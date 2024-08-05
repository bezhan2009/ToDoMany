import './App.css';
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Registration from './pages/registration';


function App() {
  return (
    <Router>
      <Routes>
        <Route exact path="/registration" element={<Registration />} />
      </Routes>
    </Router>
  );
}

export default App;