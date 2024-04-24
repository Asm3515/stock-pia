import React, { useState, useEffect } from 'react';

function Widget2_sp500() {
  const [latestData, setLatestData] = useState({});
  const [sevenDaysData, setSevenDaysData] = useState({});
  const [oneMonthData, setOneMonthData] = useState({});
  const [comparisonData, setComparisonData] = useState({});

  useEffect(() => {
    
    // Fetch data for the last 1 month
    fetch('http://127.0.0.1:5000/1month')
      .then(response => response.json())
      .then(data => setOneMonthData(data));

  }, []);

  return (
    <div className="App">

      <div id="one-month-data">
        <h2>Statistics for Last 1 Month</h2>
        <p>Average Price: {oneMonthData.average_price}</p>
        <p>Average Volume Change: {oneMonthData.average_volume_change}</p>
        <p>Expectation: {oneMonthData.expectation}</p>
      </div>
    </div>
  );
}

export default Widget2_sp500;
