import React, { useState } from 'react';
import NewsletterForm from '../Components/NewsLetterForm';
import SummaryDisplay from '../Components/SummaryDis';

const Home = () => {
    const [summary, setSummary] = useState('');

    const handleFormSubmit = async (url) => {
        try {

            const response = await fetch('http://127.0.0.1:5001/summarize', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ url }),
            });

            if (!response.ok) {
                throw new Error('Failed to fetch summary');
            }

            const data = await response.json();
            setSummary(data.summary);
            } catch (error) {
                console.error('Error:', error);
                setSummary('Error fetching summary. Please try again.');
            }
        };

    return (
        <div className="container mt-4">
            <h1>Welcome to the Newsletter Summarizer</h1>
            <NewsletterForm onSubmit={handleFormSubmit} />
            <SummaryDisplay summary={summary} />
        </div>
    );
};

export default Home;