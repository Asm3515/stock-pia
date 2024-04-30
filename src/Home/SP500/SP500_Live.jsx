import React, { useEffect, useState, useRef } from 'react';
import Chart from 'chart.js/auto';
import moment from 'moment';
import './SP500.css'; // Import CSS file
import Navbar from '../../Navbar/Navbar';
import Widget1_sp500 from "./Widget1_sp500";
import Widget2_sp500 from "./Widget2_sp500";
import 'chartjs-adapter-moment';

const SP500_Live = () => {
  const [latestData, setLatestData] = useState([]);
  const [alertMessage, setAlertMessage] = useState("");
  const [percentageChange, setPercentageChange] = useState('');
  const chartRef = useRef(null);
  const [chart, setChart] = useState(null);
  const [isDataFetched, setIsDataFetched] = useState(false);
  const alertCheckIntervalRef = useRef(null);

  const handlePercentageChange = (e) => {
    setPercentageChange(e.target.value); // Update the state with the user input
  };

  const submitPercentageChange = async () => {
    try {
      const response = await fetch(`http://127.0.0.1:5000/sp500/checkmarket/${percentageChange}`, {
        method: 'GET'
      });
      const jsonData = await response.json();
      console.log('Percentage Change Response:', jsonData);
      if (jsonData.message) {
        window.alert(jsonData.message); // Optionally show a message
      }
    } catch (error) {
      console.error('Error submitting percentage change:', error);
    }
  };

  // Setup to check for alerts based on the percentage change every 2 minutes
  useEffect(() => {
    if (percentageChange) {
      alertCheckIntervalRef.current = setInterval(() => {
        submitPercentageChange(); // Check the market based on the current threshold
      },5000); // Every 120000 ms (2 minutes)
    }

    return () => {
      if (alertCheckIntervalRef.current) {
        clearInterval(alertCheckIntervalRef.current); // Clear the interval on cleanup
      }
    };
  }, [percentageChange]); // Dependency on percentageChange

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch('http://127.0.0.1:5000/livedata', {
          method: 'GET'
        });
        const jsonData = await response.json();
        console.log('Retrieved Data:', jsonData);
        setLatestData(jsonData);
        setIsDataFetched(true);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    const fetchDataInterval = setInterval(fetchData, 60000);

    fetchData();

    return () => {
      clearInterval(fetchDataInterval);
      if (chart) {
        chart.destroy();
      }
    };
  }, []);

  useEffect(() => {
    if (isDataFetched && latestData.length > 0) {
      if (chart) {
        chart.destroy();
      }

      const ctx = chartRef.current.getContext('2d');
      const newChart = new Chart(ctx, {
        type: 'line',
        data: {
          labels: latestData.map(item => moment(item[0]).format('YYYY-MM-DD HH:mm:ss')),
          datasets: [{
            label: 'Price',
            data: latestData.map(item => item[1]),
            borderColor: '#12372A', // Change border color to #12372A
            backgroundColor: 'rgba(173, 188, 159, 0.2)', // Change fill color to rgba(173, 188, 159, 0.2)
            borderWidth: 1,
            fill: true,
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            x: {
              type: 'time',
              time: {
                parser: 'YYYY-MM-DD HH:mm:ss',
                tooltipFormat: 'YYYY-MM-DD HH:mm:ss',
                unit: 'minute',
                displayFormats: {
                  minute: 'h:mm a'
                }
              },
              title: {
                display: true,
                text: 'Time',
                color: 'black', // Change font color of x-axis label to black
                font: {
                  weight: 'bold' // Make x-axis label bold
                }
              },
              ticks: {
                color: 'black', // Change font color of y-axis ticks to black
                weight: 'bold'
              }
            },
            y: {
              title: {
                display: true,
                text: 'Price',
                color: 'black', // Change font color of y-axis label to black
                font: {
                  weight: 'bold' // Make y-axis label bold
                }
              },
              ticks: {
                color: 'black', // Change font color of y-axis ticks to black
                weight: 'bold'
              }
            }
          },
          plugins: {
            tooltip: {
              mode: 'nearest',
              intersect: false,
            }
          },
          elements: {
            line: {
              borderColor: '#12372A', // Change border color to #12372A
              borderWidth: 2,
              backgroundColor: '#12372A', // Change background color to #12372A
              fill: false
            }
          }
        }
      });

      setChart(newChart);
    }
  }, [isDataFetched, latestData, chart]);

  return (
    <div className="scrollable-container">
        
    <div className='Graph'>
      {isDataFetched && <canvas ref={chartRef} width={600} height={400}></canvas>}
      <h2 className='nametag_live'>SP500 Live Dashboard</h2>
      
    </div> 

    <div className="NotGraph">   
    <div className='Wid1'><Widget1_sp500/></div>
    <div className='Wid2'><Widget2_sp500/></div>
    </div> 
    {/* Input and Button for Setting Percentage Change */}
    <div>
        <input
          type="text"
          value={percentageChange}
          onChange={handlePercentageChange}
          placeholder="Enter Percentage Change"
        />
        <button onClick={submitPercentageChange}>Set Alert Threshold</button>
      </div>
    </div>
    
  );
};

export default SP500_Live;
