import React, { useState } from 'react';
import './LoginPage.css';
import LogoSVG from '../assets/logo.js';
import { FaEye, FaEyeSlash } from 'react-icons/fa';
import { FaWeixin } from 'react-icons/fa';
import { FaMobile } from 'react-icons/fa';

const LoginPage = ({ onLogin }) => {
    const [quickConnectId, setQuickConnectId] = useState('');
    const [ipAddress, setIpAddress] = useState('');
    const [port, setPort] = useState('');
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [showPassword, setShowPassword] = useState(false);

    const handleSubmit = e => {
        e.preventDefault();
        // 处理登录逻辑
        onLogin();
    };

    return (
        <div className="login-container">
            <div className="logo-area">
                <LogoSVG />
                <h1>NasPort</h1>
            </div>

            <form onSubmit={handleSubmit} className="login-form">
                <div className="form-section">
                    <h2>连接信息</h2>

                    <div className="input-group">
                        <label>QuickConnect ID (远程连接)</label>
                        <input
                            type="text"
                            value={quickConnectId}
                            onChange={e => setQuickConnectId(e.target.value)}
                            placeholder="输入您的QuickConnect ID"
                        />
                    </div>

                    <div className="input-group ip-port-group">
                        <div className="ip-input">
                            <label>IP地址 (本地网络)</label>
                            <input
                                type="text"
                                value={ipAddress}
                                onChange={e => setIpAddress(e.target.value)}
                                placeholder="例如: 192.168.1.100"
                            />
                        </div>
                        <div className="port-input">
                            <label>端口</label>
                            <input
                                type="text"
                                value={port}
                                onChange={e => setPort(e.target.value)}
                                placeholder="例如: 5000"
                            />
                        </div>
                    </div>

                    <p className="hint-text">至少填写一项，同时填写可获得最佳连接效果</p>
                </div>

                <div className="form-section">
                    <h2>账号信息</h2>

                    <div className="input-group">
                        <label>账号</label>
                        <input
                            type="text"
                            value={username}
                            onChange={e => setUsername(e.target.value)}
                            placeholder="输入您的账号"
                        />
                    </div>

                    <div className="input-group password-group">
                        <label>密码</label>
                        <div className="password-input-container">
                            <input
                                type={showPassword ? 'text' : 'password'}
                                value={password}
                                onChange={e => setPassword(e.target.value)}
                                placeholder="输入您的密码"
                            />
                            <button
                                type="button"
                                className="toggle-password"
                                onClick={() => setShowPassword(!showPassword)}
                            >
                                {showPassword ? <FaEyeSlash /> : <FaEye />}
                            </button>
                        </div>
                    </div>
                </div>

                <div className="network-tip">
                    <p>提示: 在相同网络环境下使用IP+端口连接速度最快</p>
                </div>

                <button type="submit" className="login-button">
                    登录
                </button>

                <div className="alt-login-options">
                    <button type="button" className="social-login">
                        <FaWeixin /> 微信登录
                    </button>
                    <button type="button" className="social-login">
                        <FaMobile /> 手机号登录
                    </button>
                </div>
            </form>
        </div>
    );
};

export default LoginPage;
