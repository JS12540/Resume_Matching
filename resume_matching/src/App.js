import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [jobDescription, setJobDescription] = useState('');
  const [resumeFile, setResumeFile] = useState(null);
  const [similarity, setSimilarity] = useState(null);
  const [error, setError] = useState(null);

  const handleFileChange = (acceptedFiles) => {
    // Assuming you want to work with a single file, you can access it as acceptedFiles[0]
    setResumeFile(acceptedFiles[0]);
  };

  const handleSubmit = async () => {
    const formData = new FormData();
    formData.append('job_description', jobDescription);
    formData.append('resume_file', resumeFile);

    try {
      const response = await axios.post('http://127.0.0.1:8000/resume_matcher', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });

      // Update similarity and error based on the response from your backend
      setSimilarity(response.data.similarity);
      setError(null);
    } catch (error) {
      console.error('API request error:', error);
      setError('An error occurred while processing your request.');
      setSimilarity(null);
    }
  };

  return (
    <div className="container mx-auto mt-10">
      <div className="w-full max-w-md mx-auto">
        <h2 className="text-2xl font-semibold mb-4">Resume Matcher</h2>
        <div className="mb-4">
          <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="jobDescription">
            Job Description:
          </label>
          <textarea
            className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
            id="jobDescription"
            placeholder="Enter job description"
            value={jobDescription}
            onChange={(e) => setJobDescription(e.target.value)}
          />
        </div>
        <div className="mb-4">
          <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="resumeFile">
            Upload Resume:
          </label>
          <input
            type="file"
            id="resumeFile"
            accept=".pdf"
            onChange={(e) => handleFileChange(e.target.files)}
          />
        </div>
        <button
          className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
          onClick={handleSubmit}
        >
          Submit
        </button>
        {similarity !== null && <p className="mt-4">Similarity: {similarity}</p>}
        {error !== null && <p className="mt-4 text-red-500">{error}</p>}
      </div>
    </div>
  );
}

export default App;
