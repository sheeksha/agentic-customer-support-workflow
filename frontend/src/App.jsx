import { useState } from "react";
import "./App.css";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

function App() {
  const [form, setForm] = useState({
    channel: "email",
    customerName: "",
    subject: "",
    message: "",
  });

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    setResult(null);

    if (!form.subject.trim() || !form.message.trim()) {
      setError("Subject and message are required.");
      setLoading(false);
      return;
    }

    try {
      const response = await fetch(`${API_BASE_URL}/process`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          channel: form.channel || "email",
          customer_name: form.customerName || "Guest",
          subject: form.subject,
          message: form.message,
        }),
      });

      if (!response.ok) {
        const text = await response.text();
        throw new Error(text || `Request failed with status ${response.status}`);
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      console.error(err);
      setError(err.message || "Something went wrong.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <header className="app-header">
        <h1>Agentic Customer Support Workflow</h1>
        <p>Multi-agent LLM pipeline for automated support responses</p>
      </header>

      <main className="app-main">
        <section className="card">
          <h2>Submit a Support Ticket</h2>
          <form onSubmit={handleSubmit} className="ticket-form">
            <div className="form-row">
              <label htmlFor="channel">Channel</label>
              <select
                id="channel"
                name="channel"
                value={form.channel}
                onChange={handleChange}
              >
                <option value="email">Email</option>
                <option value="web">Web</option>
                <option value="chat">Chat</option>
              </select>
            </div>

            <div className="form-row">
              <label htmlFor="customerName">Customer Name (optional)</label>
              <input
                id="customerName"
                name="customerName"
                type="text"
                placeholder="Jane Doe"
                value={form.customerName}
                onChange={handleChange}
              />
            </div>

            <div className="form-row">
              <label htmlFor="subject">Subject</label>
              <input
                id="subject"
                name="subject"
                type="text"
                placeholder="Example: Password reset not working"
                value={form.subject}
                onChange={handleChange}
                required
              />
            </div>

            <div className="form-row">
              <label htmlFor="message">Message</label>
              <textarea
                id="message"
                name="message"
                rows="5"
                placeholder="Describe the issue the customer is facing..."
                value={form.message}
                onChange={handleChange}
                required
              />
            </div>

            <button type="submit" disabled={loading} className="submit-btn">
              {loading ? "Running agents... (may take up to 1 minute)" : "Run Agent Workflow"}
            </button>

            {error && <p className="error-text">{error}</p>}
          </form>
        </section>

        {result && (
          <section className="results-grid">
            <div className="card">
              <h2>Triage Agent</h2>
              <p>
                <strong>Category:</strong> {result.triage.category}
              </p>
              <p>
                <strong>Priority:</strong> {result.triage.priority}
              </p>
              <p>
                <strong>Sentiment:</strong>{" "}
                {result.triage.sentiment || "N/A"}
              </p>
              {result.triage.notes && (
                <p>
                  <strong>Notes:</strong> {result.triage.notes}
                </p>
              )}
            </div>

            <div className="card">
              <h2>Retrieval Agent</h2>
              {result.retrieved_articles && result.retrieved_articles.length > 0 ? (
                <ul className="articles-list">
                  {result.retrieved_articles.map((article) => (
                    <li key={article.id} className="article-item">
                      <h3>{article.title}</h3>
                      {article.category && (
                        <p className="badge">{article.category}</p>
                      )}
                      <p className="article-content">{article.content}</p>
                    </li>
                  ))}
                </ul>
              ) : (
                <p>No relevant knowledge base articles found.</p>
              )}
            </div>

            <div className="card">
              <h2>Draft Response Agent</h2>
              <pre className="response-box">{result.draft.draft_text}</pre>
            </div>

            <div className="card">
              <h2>QA Agent (Final Response)</h2>
              <pre className="response-box highlight">
                {result.final.final_text}
              </pre>
            </div>
          </section>
        )}
      </main>

      <footer className="app-footer">
        <small>Built with FastAPI, React, and OpenAI agents.</small>
      </footer>
    </div>
  );
}

export default App;
