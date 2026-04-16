import React, { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState("summary");

  const uploadFile = async () => {
    if (!file) {
      alert("Please upload a file!");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    setLoading(true);
    setResult(null);

    try {
      const res = await axios.post(
        "http://127.0.0.1:8000/process",
        formData
      );
      setResult(res.data);
    } catch (err) {
      alert("Backend error ");
    }

    setLoading(false);
  };

  return (
    <div className="app">

      {/* HEADER */}
      <h1 className="title"> PadhLeBro</h1>

      {/* UPLOAD CARD */}
      <div className="upload-card">
        <p>Upload Audio / Notes / Image</p>
        <input type="file" onChange={(e) => setFile(e.target.files[0])} />
        <button onClick={uploadFile}>Process </button>
      </div>

      {/* LOADING UI */}
      {loading && (
        <div className="loader-container">
          <div className="spinner"></div>
          <p>AI is analyzing your lecture...</p>
        </div>
      )}

      {/* OUTPUT */}
      {!loading && result && (
        <div className="output-card">

          {/* TABS */}
          <div className="tabs">
            <button onClick={() => setActiveTab("summary")}>
              Summary
            </button>
            <button onClick={() => setActiveTab("keypoints")}>
              Keypoints
            </button>
          </div>

          {/* SUMMARY */}
          {activeTab === "summary" && (
            <div className="content">
              {result.summary}
            </div>
          )}

          {/* KEYPOINTS */}
          {activeTab === "keypoints" && (
            <div className="content">
              {result.keypoints.map((kp, i) => (
                <p key={i}>• {kp}</p>
              ))}
            </div>
          )}

          {/* ACTIONS */}
          <div className="actions">
            <button
              onClick={() =>
                navigator.clipboard.writeText(result.summary)
              }
            >
               Copy
            </button>

            <button
              onClick={() => {
                const blob = new Blob([result.summary], {
                  type: "text/plain",
                });
                const link = document.createElement("a");
                link.href = URL.createObjectURL(blob);
                link.download = "summary.txt";
                link.click();
              }}
            >
               Download
            </button>
          </div>

        </div>
      )}
    </div>
  );
}

export default App;