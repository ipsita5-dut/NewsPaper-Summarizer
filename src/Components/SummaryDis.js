import React from 'react';

const SummaryDisplay = ({ summary }) => {
    return (
        <div className="mt-4">
            <h2>Summary</h2>
            <p>{summary}</p>
        </div>
    );
};

export default SummaryDisplay;