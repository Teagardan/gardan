import React from 'react';
import ReactDOM from 'react-dom/client';
import OrgChart from './orgChart';

const App = () => { 
  return (
    <React.StrictMode>
      <OrgChart />
    </React.StrictMode>
  );
};

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App />); 