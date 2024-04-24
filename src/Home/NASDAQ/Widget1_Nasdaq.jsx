import React, { useState, useEffect } from 'react';

function Widget1_sp500() {

    const [sevenDaysData, setSevenDaysData] = useState({});
  
    useEffect(() => {
      
      // Fetch data for the last 7 days
      fetch('http://127.0.0.1:5000/nasdaq/7days')
        .then(response => response.json())
        .then(data => setSevenDaysData(data));
  
    }, []);
  
    return (
      <div >
        <div id="seven-days-data">
          <h2>Statistics for Last 7 Days</h2>
          <p>Average Price: {sevenDaysData.average_price}</p>
          <p>Average Volume Change: {sevenDaysData.average_volume_change}</p>
          <p>Expectation: {sevenDaysData.expectation}</p>
        </div>
  
      </div>
    );
}


export default Widget1_sp500;