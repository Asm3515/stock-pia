import React, { useEffect, useState, useRef } from 'react';
import Chart from 'chart.js/auto';
import moment from 'moment';
import  plot1 from "./output0.png"
import  plot2 from "./output1.png"
import  plot3 from "./output3.png"
import "./History.css"

const History = () => {
  const [historicalData, setHistoricalData] = useState([]);
  const chartRef = useRef(null);
  const [chart, setChart] = useState(null);
  const [isDataFetched, setIsDataFetched] = useState(false);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch('http://127.0.0.1:5000/history', {
          method: 'GET'
        });
        const jsonData = await response.json();
        console.log('Retrieved Data:', jsonData);
        setHistoricalData(jsonData);
        setIsDataFetched(true);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchData();
  }, []);

  useEffect(() => {
    if (isDataFetched && historicalData.length > 0) {
      if (chart) {
        chart.destroy();
      }

      const ctx = chartRef.current.getContext('2d');
      const newChart = new Chart(ctx, {
        type: 'line',
        data: {
          labels: Object.keys(historicalData),
          datasets: [{
            label: 'Closing Price',
            data: Object.values(historicalData),
            borderColor: '#12372A',
            borderWidth: 2,
            fill: false,
            pointRadius: 0, // Hide data points
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            x: {
              type: 'time',
              time: {
                parser: 'YYYY-MM-DD',
                tooltipFormat: 'MMM DD, YYYY',
                unit: 'day',
                displayFormats: {
                  day: 'MMM DD, YYYY'
                }
              },
              title: {
                display: true,
                text: 'Date',
                color: 'black',
                font: {
                  weight: 'bold'
                }
              },
              ticks: {
                color: 'black',
                weight: 'bold'
              }
            },
            y: {
              title: {
                display: true,
                text: 'Price (USD)',
                color: 'black',
                font: {
                  weight: 'bold'
                }
              },
              ticks: {
                color: 'black',
                weight: 'bold'
              }
            }
          },
          plugins: {
            tooltip: {
              mode: 'index',
              intersect: false,
            }
          },
          elements: {
            line: {
              tension: 0.4, // Adjust line tension for smoother curve
            }
          }
        }
      });

      setChart(newChart);
    }
  }, [isDataFetched, historicalData, chart]);

  return (
    <div className="scrollable-container-proto">
      <h2>The below Plot shows the data of past 29 Years which is taken into consideration for anomly detection</h2>
      <div className='plot-image'><img src={plot1} alt = 'failed_loding'/></div>
      <h2>The below Plot shows the anamoly detected within the dataframe which have affected the market</h2>
      <div className='plot-image'><img src={plot2} alt = 'failed_loding'/></div>
      <h2>This Plot Showcase the Efficency of LSTM model in predicting the stock behaviour</h2>
      <div className='plot-image'><img src={plot3} alt = 'failed_loding'/></div>
    </div>
  );
};

export default History;
