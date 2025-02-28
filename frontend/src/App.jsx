import React, { useState } from 'react';
import LoginPage from './pages/LoginPage';
import LoadingPage from './pages/LoadingPage';
import MainPage from './pages/MainPage';
import './App.css';

const App = () => {
    const [appState, setAppState] = useState('login'); // 'login', 'loading', 'main'

    const handleLogin = () => {
        setAppState('loading');
    };

    const handleLoadingComplete = () => {
        setAppState('main');
    };

    return (
        <div className="app">
            {appState === 'login' && <LoginPage onLogin={handleLogin} />}
            {appState === 'loading' && <LoadingPage onComplete={handleLoadingComplete} />}
            {appState === 'main' && <MainPage />}
        </div>
    );
};

export default App;
