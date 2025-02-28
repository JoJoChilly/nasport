import React, { useState } from 'react';
import './MainPage.css';
import { FaSearch, FaHome, FaHistory, FaUser } from 'react-icons/fa';

// 模拟数据
const mockData = [
    {
        id: 1,
        coverImage: 'https://via.placeholder.com/300x450',
        chineseTitle: '黑客帝国',
        englishTitle: 'The Matrix',
        type: '科幻',
        year: 1999,
        progress: 0.7,
        inProgress: true,
    },
    {
        id: 2,
        coverImage: 'https://via.placeholder.com/300x450',
        chineseTitle: '星际穿越',
        englishTitle: 'Interstellar',
        type: '科幻/冒险',
        year: 2014,
        progress: 0,
        inProgress: false,
    },
    {
        id: 3,
        coverImage: 'https://via.placeholder.com/300x450',
        chineseTitle: '盗梦空间',
        englishTitle: 'Inception',
        type: '科幻/动作',
        year: 2010,
        progress: 0.3,
        inProgress: true,
    },
    {
        id: 4,
        coverImage: 'https://via.placeholder.com/300x450',
        chineseTitle: '肖申克的救赎',
        englishTitle: 'The Shawshank Redemption',
        type: '剧情',
        year: 1994,
        progress: 0,
        inProgress: false,
    },
    {
        id: 5,
        coverImage: 'https://via.placeholder.com/300x450',
        chineseTitle: '千与千寻',
        englishTitle: 'Spirited Away',
        type: '动画',
        year: 2001,
        progress: 0,
        inProgress: false,
    },
    {
        id: 6,
        coverImage: 'https://via.placeholder.com/300x450',
        chineseTitle: '指环王：王者归来',
        englishTitle: 'The Lord of the Rings: The Return of the King',
        type: '奇幻/冒险',
        year: 2003,
        progress: 0,
        inProgress: false,
    },
];

const MainPage = () => {
    const [activeTab, setActiveTab] = useState('全部');
    const [activeNav, setActiveNav] = useState('home');

    const categories = ['全部', '电影', '剧集', '音乐', '书籍'];

    return (
        <div className="main-container">
            <header className="main-header">
                <h1>我的影音库</h1>
                <button className="search-button">
                    <FaSearch />
                </button>
            </header>

            <div className="category-tabs">
                {categories.map(category => (
                    <button
                        key={category}
                        className={`tab ${activeTab === category ? 'active' : ''}`}
                        onClick={() => setActiveTab(category)}
                    >
                        {category}
                    </button>
                ))}
            </div>

            <div className="content-grid">
                {mockData.map(item => (
                    <div key={item.id} className="content-card">
                        <div className="cover-container">
                            <img src={item.coverImage} alt={item.chineseTitle} className="cover-image" />
                            {item.inProgress && (
                                <div className="progress-overlay">
                                    <div className="continue-badge">继续观看</div>
                                    <div className="watch-progress">
                                        <div
                                            className="progress-indicator"
                                            style={{ width: `${item.progress * 100}%` }}
                                        ></div>
                                    </div>
                                </div>
                            )}
                        </div>
                        <div className="content-info">
                            <h3 className="chinese-title">{item.chineseTitle}</h3>
                            <p className="english-title">{item.englishTitle}</p>
                            <p className="content-meta">
                                {item.type} · {item.year}
                            </p>
                        </div>
                    </div>
                ))}
            </div>

            <nav className="bottom-nav">
                <button
                    className={`nav-item ${activeNav === 'home' ? 'active' : ''}`}
                    onClick={() => setActiveNav('home')}
                >
                    <FaHome />
                    <span>首页</span>
                </button>
                <button
                    className={`nav-item ${activeNav === 'history' ? 'active' : ''}`}
                    onClick={() => setActiveNav('history')}
                >
                    <FaHistory />
                    <span>历史</span>
                </button>
                <button
                    className={`nav-item ${activeNav === 'profile' ? 'active' : ''}`}
                    onClick={() => setActiveNav('profile')}
                >
                    <FaUser />
                    <span>我的</span>
                </button>
            </nav>
        </div>
    );
};

export default MainPage;
