import { useState, useEffect } from "react";
import axios from "axios";
import ReactMarkdown from 'react-markdown'

export default function ChatWindow() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [sessionId, setSessionId] = useState("");
  const endpoint = "http://localhost:8000/chat_session/"

  useEffect(() => {
    // Retrieve or create a session ID for this tab
    let storedSessionId = sessionStorage.getItem("session_id");
    if (!storedSessionId) {
      storedSessionId = "session-" + Math.random().toString(36).substr(2, 9);
      sessionStorage.setItem("session_id", storedSessionId);
    }
    setSessionId(storedSessionId);
    console.log(sessionId);

    // Load conversation history
    axios.get(endpoint+`${sessionStorage.getItem("session_id")}/`, {
      headers: {
        "X-Requested-With": "XMLHttpRequest",
      },
    })
      .then((response) => {
        if (response.data.conversation) {
          setMessages(response.data.conversation.map(chat => ({ role: chat.role, text: chat.content[0].text })));
        }
      })
      .catch((error) => console.error("Error loading conversation:", error));
  }, []);

  const sendMessage = () => {
    if (!input.trim()) return;
    setMessages([...messages, { role: "user", text: input }]);
    setInput("");
    axios.post(endpoint +`${sessionStorage.getItem("session_id")}/`, new URLSearchParams({ message: input }), {
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
    })
    .then((response) => {
      if (response.data.conversation) {
        setMessages(response.data.conversation.map(chat => ({ role: chat.role, text: chat.content[0].text })));
      }
    })
    .catch((error) => console.error("Error loading conversation:", error));
  };

  return (
    <div className="chat-container">
      <div className="card">
        <ul className="list-none messages-list">
          <li className="message">
            <div className="message-text">
              <div className="message-sender">AI Chatbot</div>
              <div className="message-content">Hello! How can I assist you today?</div>
            </div>
          </li>

          {messages.map((msg, index) => (
            <li
              key={index}
              className={`message ${msg.role === "user" ? "sent" : "received"}`}
            >
              <div className="message-text">
                <div className="message-sender">
                  {msg.role === "user" ? "You" : "AI Chatbot"}
                </div>
                <ReactMarkdown className="message-content">{msg.text}</ReactMarkdown>
              </div>
            </li>
          ))}
        </ul>
      </div>
      <form className="message-form">
        <input
          type="text"
          className="message-input"
          placeholder="Type a message..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && sendMessage()}
        />
        <button
          className="btn-send"
          onClick={(e) => {
            e.preventDefault();
            sendMessage();
          }}
        >
          Send
        </button>
      </form>
    </div>
  );
}