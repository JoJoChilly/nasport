import React, { useState, useEffect } from 'react';
import './LoadingPage.css';
import LogoSVG from '../assets/logo.js';

const LoadingPage = ({ onComplete }) => {
    const [scanProgress, setScanProgress] = useState(0);
    const [aiProgress, setAiProgress] = useState(0);
    const [coverProgress, setCoverProgress] = useState(0);
    const [currentStage, setCurrentStage] = useState('scanning');

    // 加速模拟加载过程
    useEffect(() => {
        const scanTimer = setInterval(() => {
            setScanProgress(prev => {
                if (prev >= 100) {
                    clearInterval(scanTimer);
                    setCurrentStage('recognizing');
                    return 100;
                }
                return prev + 10; // 加速：从2%增加到10%
            });
        }, 100); // 加速：从300ms减少到100ms

        return () => clearInterval(scanTimer);
    }, []);

    useEffect(() => {
        if (currentStage === 'recognizing') {
            const aiTimer = setInterval(() => {
                setAiProgress(prev => {
                    if (prev >= 100) {
                        clearInterval(aiTimer);
                        setCurrentStage('matching');
                        return 100;
                    }
                    return prev + 10; // 加速：从1%增加到10%
                });
            }, 100); // 加速：从400ms减少到100ms

            return () => clearInterval(aiTimer);
        }
    }, [currentStage]);

    useEffect(() => {
        if (currentStage === 'matching') {
            const coverTimer = setInterval(() => {
                setCoverProgress(prev => {
                    if (prev >= 100) {
                        clearInterval(coverTimer);
                        setTimeout(() => onComplete(), 300); // 加速：从1000ms减少到300ms
                        return 100;
                    }
                    return prev + 10; // 加速：从2%增加到10%
                });
            }, 100); // 加速：从200ms减少到100ms

            return () => clearInterval(coverTimer);
        }
    }, [currentStage, onComplete]);

    return (
        <div className="loading-container">
            <div className="loading-content">
                <div className="logo-animation">
                    <div className="animated-logo">
                        <LogoSVG />
                    </div>
                    <div className="logo-glow"></div>
                </div>

                <div className="loading-text">
                    <h1>初始化您的媒体库</h1>
                    <h2>
                        {currentStage === 'scanning' && '正在扫描您的NAS设备...'}
                        {currentStage === 'recognizing' && '正在识别您的媒体内容...'}
                        {currentStage === 'matching' && '正在匹配封面信息...'}
                    </h2>
                </div>

                <div className="progress-section">
                    <div className="progress-item">
                        <div className="progress-label">
                            <span>扫描文件夹</span>
                            <span>{scanProgress}%</span>
                        </div>
                        <div className="progress-bar">
                            <div className="progress-fill" style={{ width: `${scanProgress}%` }}></div>
                        </div>
                    </div>

                    <div className="progress-item">
                        <div className="progress-label">
                            <span>AI识别内容</span>
                            <span>{aiProgress}%</span>
                        </div>
                        <div className="progress-bar">
                            <div className="progress-fill" style={{ width: `${aiProgress}%` }}></div>
                        </div>
                    </div>

                    <div className="progress-item">
                        <div className="progress-label">
                            <span>匹配封面</span>
                            <span>{coverProgress}%</span>
                        </div>
                        <div className="progress-bar">
                            <div className="progress-fill" style={{ width: `${coverProgress}%` }}></div>
                        </div>
                    </div>
                </div>

                <div className="loading-hints">
                    <p>首次加载可能需要几分钟</p>
                    <p>请耐心等待，不要关闭应用</p>
                </div>

                <div className="loading-animation">
                    <div className="dot"></div>
                    <div className="dot"></div>
                    <div className="dot"></div>
                    <div className="dot"></div>
                    <div className="dot"></div>
                </div>

                <button className="cancel-button">稍后再试</button>
            </div>
        </div>
    );
};

export default LoadingPage;
