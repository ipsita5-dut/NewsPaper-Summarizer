// import React, { useState } from 'react';

// const NewsletterForm = ({ onSubmit }) => {
//     const [url, setUrl] = useState(''); // Declare the 'url' state

//     const handleSubmit = (e) => {
//         e.preventDefault(); // Prevent the default form submission
//         onSubmit(url); // Call the onSubmit function with the URL
//         setUrl(''); // Clear the input field after submission
//     };

//     return (
//         <form onSubmit={handleSubmit} className="mb-4">
//             <div className="form-group">
//                 <label htmlFor="newsletterUrl">Article URL</label>
//                 <input
//                     type="url"
//                     id="newsletterUrl"
//                     className="form-control"
//                     value={url} // Use the 'url' state here
//                     onChange={(e) => setUrl(e.target.value)} // Update the 'url' state
//                     required
//                 />
//             </div>
//             <button type="submit" className="btn btn-primary mt-2">Summarize</button>
//         </form>
//     );
// };

// export default NewsletterForm;

import React, { useState } from 'react';
import axios from 'axios';

const NewsletterForm = () => {
    const [url, setUrl] = useState('');
    const [summary, setSummary] = useState('');
    const [error, setError] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError(''); // Clear previous errors
        setSummary(''); // Clear previous summary
        try {
            const response = await axios.post('http://localhost:5001/summarize', { url });
            if (response.data.summary) {
                setSummary(response.data.summary);
            } else {
                setError('No summary returned from the server.');
            }
        } catch (error) {
            if (error.response) {
                // Server responded with a status other than 200
                setError(`Error : ${error.response.data.error || 'An error occurred.'}`);
            } else if (error.request) {
                // Request was made but no response received
                setError('No response from the server. Please check your connection.');
            } else {
                // Something happened in setting up the request
                setError('Error in setting up the request.');
            }
            console.error('Error summarizing article:', error);
        }
    };

    return (
        <div>
            <form onSubmit={handleSubmit} className="mb-4">
                <div className="form-group">
                    <label htmlFor="newsletterUrl">Article URL</label>
                    <input
                        type="url"
                        id="newsletterUrl"
                        className="form-control"
                        value={url}
                        onChange={(e) => setUrl(e.target.value)}
                        required
                    />
                </div>
                <button type="submit" className="btn btn-primary mt-2">Summarize</button>
            </form>
            {summary && <div className="summary"><h3>Summary:</h3><p>{summary}</p></div>}
            {error && <div className="error"><p>{error}</p></div>}
        </div>
    );
};

export default NewsletterForm;