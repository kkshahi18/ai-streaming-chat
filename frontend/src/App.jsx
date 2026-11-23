
import { useRef, useState } from "react";
import "./App.css";
import { readChatStream } from "./stream.js";

const API_URL = "http://127.0.0.1:8000/chat/stream";

export default function App() {
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const controllerRef = useRef(null);

  async function sendMessage(e) {
    e.preventDefault();

    const prompt = question.trim();
    if (!prompt || controllerRef.current) return;

    const controller = new AbortController();
    controllerRef.current = controller;

    const answerId = crypto.randomUUID();

    setMessages(prev => [
      ...prev,
      { id: crypto.randomUUID(), role: "user", text: prompt },
      { id: answerId, role: "assistant", text: "" }
    ]);

    setQuestion("");
    setLoading(true);

    const appendAnswer = text => {
      if (controllerRef.current !== controller) return;
      setMessages(prev =>
        prev.map(msg =>
          msg.id === answerId
            ? { ...msg, text: msg.text + text }
            : msg
        )
      );
    };

    try {
      const response = await fetch(API_URL, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ message: prompt }),
        signal: controller.signal
      });

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }

      if (!response.body) {
        throw new Error("Streaming is not supported");
      }

      await readChatStream(response.body, appendAnswer, controller.signal);

    } catch (error) {
      if (error.name === "AbortError") {
        appendAnswer("\n\n[Generation stopped]");
      } else {
        appendAnswer(`\n\nError: ${error.message}`);
      }
    } finally {
      if (controllerRef.current === controller) {
        controllerRef.current = null;
        setLoading(false);
      }
    }
  }

  function stopGeneration() {
    controllerRef.current?.abort();
  }

  function clearChat() {
    controllerRef.current?.abort();
    controllerRef.current = null;
    setLoading(false);
    setMessages([]);
  }

  return (
    <div className="app">
      <aside className="sidebar">
        <h2>AI Streaming Chat</h2>
        <button onClick={clearChat}>
          + New Chat
        </button>
        <p>Powered by Gemini + FastAPI</p>
      </aside>

      <main className="main">
        <header>
          <h1>AI Assistant</h1>
          <span>Streaming Answers</span>
        </header>

        <section className="messages">
          {messages.length === 0 && (
            <div className="welcome">
              <h2>How can I help you?</h2>
              <p>Ask anything to start a conversation.</p>
            </div>
          )}

          {messages.map(msg => (
            <div
              key={msg.id}
              className={`message ${msg.role}`}
            >
              <strong>
                {msg.role === "user" ? "You" : "AI"}
              </strong>

              <p>
                {msg.text ||
                  (loading ? "Thinking..." : "")}
              </p>
            </div>
          ))}
        </section>

        <form onSubmit={sendMessage} className="input-area">
          <input
            value={question}
            onChange={e => setQuestion(e.target.value)}
            placeholder="Ask your question..."
            disabled={loading}
          />

          {loading ? (
            <button
              type="button"
              onClick={stopGeneration}
            >
              Stop
            </button>
          ) : (
            <button type="submit">
              Send
            </button>
          )}
        </form>
      </main>
    </div>
  );
}
