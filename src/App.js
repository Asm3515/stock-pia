import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Navbar from './Navbar/Navbar';
import SP500Live from './Home/SP500/SP500_Live';
import Home from './Home/Home';
import Nasdaq_Live from "./Home/NASDAQ/Nasdaq_live"
import History from './Home/HISTORY/History';

const App = () => {
  return (
    <Router>
      <div>
        <Navbar />
        <Routes>
  <Route path="/" element={<Home />} />
  <Route path="/sp500" element={<SP500Live />} />
  <Route path="/nasdaq" element={<Nasdaq_Live />} />
  <Route path="/history" element={<History />} />
  {/* Add more routes for other components if needed */}
</Routes>

      </div>
    </Router>
  );
};

export default App;
