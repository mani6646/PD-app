import './App.css';
import React, { useState } from 'react';
import SpiralModel from './components/SpiralModel';
import WaveModel from './components/WaveModel';

const App = () => {
  const [selectedModel, setSelectedModel] = useState(null);

  return (
    <div className='App'>
      <h1>Parkinson's Disease Prediction</h1>
      <div className='button-container'>
      <div className='model-button' onClick={() => setSelectedModel('spiral')}><button class="button-64"><span class="text">Spiral Model</span></button></div>
      <div className='model-button' onClick={() => setSelectedModel('wave')}><button class="button-64"><span class="text">Wave Model</span></button></div>
      </div>
      <div>
      {selectedModel === 'spiral' && <SpiralModel />}
      {selectedModel === 'wave' && <WaveModel />}
      </div>
    </div>
  );
};

export default App;
