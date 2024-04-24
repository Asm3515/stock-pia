import React, { useEffect, useState } from 'react';

const Home = () => {
    return (
        <div className="scrollable-container">
            <section id="AboutMe" className="about--section">
                <div className="hero--section--content--box about--section--box">
                    <div className="hero--section--content">
                        <h1 className="skills-section--heading">PROJECT INTRODUCTION</h1>
                        <h2 className="section--title">Description</h2>
                        <p className="hero--section-description">
                            Stockpia is a real-time stock data dashboard that provides users with a comprehensive view of stock
                            performance and detects anomalies. It visualizes stock data and generates alerts when a stock price
                            significantly deviates from a predefined range, indicating a potential market fluctuation.
                        </p>

                        <h2 className="section--title">Problem Statements</h2>
                        <p className="hero--section-description">
                            In the rapidly fluctuating world of stock trading, timely information and data analysis are crucial. The
                            problem lies in the fragmentation of information sources and the lack of real-time, personalized
                            notifications for market movements, which can lead to missed opportunities or uninformed decisions.
                        </p>

                        <h1 className="skills-section--heading">DATA INTRODUCTION</h1>
                        <h2 className="section--title">Description</h2>
                        <p className="hero--section-description">
                            <ul>
                                <li>Realtime Data is being collected from Yfinance Api</li>
                                <li>Historical Data was stoed in pandas datafranme and utilise for further analysis</li>
                                <li>Content3</li>
                                <li>Content4</li>
                                <li>Content5</li>
                            </ul>
                        </p>

                        <h2 className="section--title">WORK DONE TILL DATE</h2>
                        <p className="hero--section-description">
                            <ul>
                                <li>Handling Realtime Data and Visualising it in Realtime</li>
                                <li>Conducting Historical Analysis and Finding connections</li>
                                <li>Creating an Notification System which alerts when anamoly is detected</li>
                                <li>Implementing LSTM Model for Predictive Analysis</li>
                            </ul>
                        </p>
                    </div>
                </div>
            </section>
        </div>
    );
}

export default Home;
