import React from 'react';

const LogoSVG = () => (
    <svg width="100" height="100" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
        <rect width="100" height="100" rx="20" fill="#1E1E1E" />
        <path
            d="M20 40H80M20 60H80M30 20V80M50 20V80M70 20V80"
            stroke="#FF6B81"
            strokeWidth="6"
            strokeLinecap="round"
        />
        <circle cx="50" cy="50" r="30" stroke="#FF6B81" strokeWidth="4" strokeDasharray="10 5" />
    </svg>
);

export default LogoSVG;
