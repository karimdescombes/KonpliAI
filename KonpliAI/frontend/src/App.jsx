import { useEffect, useState } from "react";

function App() {
  const [status, setStatus] = useState("...");

  useEffect(() => {
    fetch("https://konpliai-backend.azurewebsites.net/health")
      .then((res) => res.json())
      .then((data) => setStatus(data.status))
      .catch(() => setStatus("error"));
  }, []);

  return (
    <div style={{ fontFamily: "Arial", padding: "2rem" }}>
      <h1>KoNpLiAI Frontend</h1>
      <p>Backend status: <strong>{status}</strong></p>
    </div>
  );
}

export default App;
