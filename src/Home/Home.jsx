import React from 'react';
import './Home.css';
import videoBg from '../Assets/video.mp4';
import { ScrollContainer, ScrollPage } from 'react-scroll-motion';
import { Animator, Sticky, ZoomIn, Fade, MoveOut, Move, batch } from 'react-scroll-motion';
import stm2 from '../Assets/stm2.jpeg';
import stm1 from '../Assets/stm1.jpeg';
import Typewriter from 'typewriter-effect';

const ZoomInScrollOut = batch(Sticky(), Fade(), ZoomIn());
const FadeUp = batch(Fade(), Sticky(), Move());

const Home = () => {
    return (
        <div className="hero--section">
            <div className="video-bg">
                <video src={videoBg} autoPlay loop muted />
            </div>
            <div className="content-container">
                <ScrollContainer>
                    <ScrollPage>
                        <Animator animation={batch(Sticky(), Fade(), MoveOut)}>
                            <p className="project--title">
                                <Typewriter
                                options={
                                    {
                                        loop: true,
                                        delay: 50,
                                        cursor: '|',
                                        cursorStyle: 'hide',
                                        autoStart: true,
                                        strings: ['STOCKTOPIA']
                                        
                                    }
                                }
                                />
                            </p>
                        </Animator>
                    </ScrollPage>
                    <ScrollPage style={{ backgroundImage: `url(${stm2})`, backgroundSize: 'cover' }}>
                        <Animator animation={ZoomInScrollOut}>
                            <div className="hero--section--content">
                                <h1 className="skills-section--heading"><Typewriter
                                options={
                                    {
                                        loop: true,
                                        delay: 50,
                                        cursor: '|',
                                        cursorStyle: 'hide',
                                        autoStart: true,
                                        strings: ['PROJECT INTRODUCTION']
                                        
                                    }
                                }
                                /></h1>
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
                            </div>
                        </Animator>
                    </ScrollPage>
                    <ScrollPage style={{ backgroundImage: `url(${stm1})`, backgroundSize: 'cover' }}>
                        <Animator animation={FadeUp}>
                            <div className="hero--section--content">
                                <h1 className="skills-section--heading">
                                <Typewriter
                                options={
                                    {
                                        loop: true,
                                        delay: 50,
                                        cursor: '|',
                                        cursorStyle: 'hide',
                                        autoStart: true,
                                        strings: ['DATA INTRODUCTION']
                                        
                                    }
                                }
                                />
                                </h1>
                                <h2 className="section--title">Description</h2>
                                <p className="hero--section-description">
                                    <ul>
                                        <li>Realtime Data is being collected from Yfinance Api</li>
                                        <li>Historical Data was stored in pandas dataframe and utilized for further analysis</li>
                                    </ul>
                                </p>
                                <h2 className="section--title">WORK DONE TILL DATE</h2>
                                <p className="hero--section-description">
                                    <ul>
                                        <li>Handling Realtime Data and Visualizing it in Realtime</li>
                                        <li>Conducting Historical Analysis and Finding connections</li>
                                        <li>Creating a Notification System which alerts when an anomaly is detected</li>
                                        <li>Implementing LSTM Model for Predictive Analysis</li>
                                    </ul>
                                </p>
                            </div>
                        </Animator>
                    </ScrollPage>
                </ScrollContainer>
            </div>
        </div>
    );
}

export default Home;
