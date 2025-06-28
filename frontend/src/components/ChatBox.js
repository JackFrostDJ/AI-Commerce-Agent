import React, { useState } from 'react';

function ChatBox() {
  const [msg, setMsg] = useState('');
  const [res, setRes] = useState('');

  const handleSend = async () => {
    if (!msg.trim()) return;
    const response = await fetch('/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: msg })
    });
    const data = await response.json();
    setRes(data.reply);
  };

  return (
    <div>
      <div className="flex gap-2 mb-4">
        <input
          value={msg}
          onChange={e => setMsg(e.target.value)}
          placeholder="Type your question here..."
          className="flex-1 border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-400"
        />
        <button
          onClick={handleSend}
          className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded"
        >
          Send
        </button>
      </div>
      <div className="bg-gray-100 p-4 rounded text-gray-800 min-h-[80px] whitespace-pre-line">
        {res || "Ask me anything about our products!"}
      </div>
    </div>
  );
}

export default ChatBox;
