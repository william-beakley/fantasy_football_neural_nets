import './App.css';
import React, { useState, useEffect } from 'react';
import Querier from './components/Querier';



function App() {
  return (
    <div className="App">
      <header className="App-header">
        <Querier/>
      </header>
    </div>
  );
}

export default App;
