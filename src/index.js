import React, { useState } from 'react';
import axios from 'axios';
import { Container, Form, Button, Alert } from 'react-bootstrap';
import Dropzone from 'react-dropzone';

function App() {
  const [jobDescription, setJobDescription] = useState('');
  const [resumeFile, setResumeFile] = useState(null);
  const [similarity, setSimilarity] = useState(null);
  const [errorMessage, setErrorMessage] = useState('');

  const handleJobDescriptionChange = (e) => {
    setJobDescription(e.target.value);
  };

  const handleFileDrop = (acceptedFiles) => {
    setResumeFile(acceptedFiles[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Check if both job description and resume file are provided
    if (!jobDescription || !resumeFile) {
      setErrorMessage('Please provide both a job description and a resume file.');
      return;
    }

    // Create a FormData object for the file upload
    const formData = new FormData();
    formData.append('job_description', jobDescription);
    formData.append('resume_file', resumeFile);

    try {
      // Send the job description and resume file to the Flask backend
      const response = await axios.post('/resume_matcher', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });

      setSimilarity(response.data.similarity.toFixed(2));
      setErrorMessage('');
    } catch (error) {
      console.error(error);
      setErrorMessage('An error occurred while processing your request.');
    }
  };

  return (
    <Container className="mt-5">
      <h1>Resume Matcher</h1>
      <Form onSubmit={handleSubmit}>
        <Form.Group controlId="jobDescription">
          <Form.Label>Job Description</Form.Label>
          <Form.Control
            as="textarea"
            rows={4}
            value={jobDescription}
            onChange={handleJobDescriptionChange}
          />
        </Form.Group>

        <Form.Group controlId="resumeFile">
          <Form.Label>Upload Resume</Form.Label>
          <Dropzone onDrop={handleFileDrop}>
            {({ getRootProps, getInputProps }) => (
              <div {...getRootProps()} className="dropzone">
                <input {...getInputProps()} />
                <p>Drag &amp; drop a resume file here, or click to select one</p>
              </div>
            )}
          </Dropzone>
        </Form.Group>

        <Button variant="primary" type="submit">
          Match Resume
        </Button>
      </Form>

      {similarity !== null && (
        <Alert className="mt-3" variant="success">
          Matching Score: {similarity}
        </Alert>
      )}

      {errorMessage && (
        <Alert className="mt-3" variant="danger">
          {errorMessage}
        </Alert>
      )}
    </Container>
  );
}

export default App;
