import React, { useState } from "react";
import "./App.css";
import axios from "axios";

function App() {
  const [jobDescription, setJobDescription] = useState("");
  const [resumeFiles, setResumeFiles] = useState([]);
  const [similarities, setSimilarities] = useState([]);
  const [error, setError] = useState("");

  const handleFileChange = (e) => {
    const files = Array.from(e.target.files);
    setResumeFiles(files);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const formData = new FormData();
    formData.append("job_description", jobDescription);
    resumeFiles.forEach((file, index) => {
      formData.append(`resume_file_${index}`, file);
    });

    try {
      const response = await axios.post("/resume_matcher", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      setSimilarities(response.data.similarities);
      setError("");
    } catch (err) {
      setError("An error occurred. Please try again.");
    }
  };

  return (
    <div className="App">
      <h1>Resume Matcher</h1>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>Job Description:</label>
          <textarea
            value={jobDescription}
            onChange={(e) => setJobDescription(e.target.value)}
            required
          />
        </div>
        <div className="form-group">
          <label>Upload Resumes:</label>
          <input
            type="file"
            accept=".pdf"
            multiple
            onChange={handleFileChange}
            required
          />
        </div>
        <button type="submit">Match Resumes</button>
      </form>
      {error && <p className="error">{error}</p>}
      {similarities.length > 0 && (
        <div className="results">
          <h2>Similarities:</h2>
          <ul>
            {similarities.map((similarity, index) => (
              <li key={index}>{`Resume ${index + 1}: ${similarity.toFixed(
                2
              )}`}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default App;
