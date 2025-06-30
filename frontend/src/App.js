import React, { useRef, useState } from 'react';
import { FaCamera } from 'react-icons/fa';
import './index.css';

function App() {
  const [input, setInput] = useState('');
  const [imageFile, setImageFile] = useState(null);
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const dropRef = useRef();

  const BACKEND_URL = "https://ai-commerce-agent-x0sj.onrender.com";

  const handleSend = async () => {
    if (!input.trim() && !imageFile) return;

    const userMsg = {
      role: 'user',
      text: input,
      image: imageFile?.name || null
    };
    setMessages([...messages, userMsg]);
    setInput('');
    setImageFile(null);
    setLoading(true);

    const formData = new FormData();
    formData.append('query', input);
    if (imageFile) formData.append('image', imageFile);

    try {
      const res = await fetch(`${BACKEND_URL}/hybrid-search`, {
        method: 'POST',
        body: formData
      });
      const data = await res.json();
      setMessages(prev => [
        ...prev,
        {
          role: 'bot',
          text: data.reply || 'Here are the best matches I found!',
          results: data.results || []
        }
      ]);
    } catch {
      setMessages(prev => [...prev, { role: 'bot', text: 'Something went wrong. Try again later.' }]);
    } finally {
      setLoading(false);
    }
  };

  const handleFile = file => {
    if (file && file.type.startsWith('image/')) {
      setImageFile(file);
    }
  };

  const handleDrop = e => {
    e.preventDefault();
    if (e.dataTransfer.files.length) {
      handleFile(e.dataTransfer.files[0]);
    }
  };

  const handleDragOver = e => e.preventDefault();

  return (
    <div className="min-h-screen bg-darkGold text-white flex flex-col items-center px-4 py-8">
      <div className="absolute top-0 left-0 w-full h-2 bg-gradient-to-r from-gold to-transparent" />
      <div className="flex flex-col items-center mb-6">
        <img src="/logo.png" alt="Comma Logo" className="h-24 mb-2" />
        <h1 className="text-4xl font-bold text-gold">Comma, Your AI Commerce Assistant</h1>
        <p className="text-md text-lightGold mt-2 text-center">
            Ask anything or upload an image with a prompt to find matching products.
        </p>
      </div>

      <div
  ref={dropRef}
  onDrop={handleDrop}
  onDragOver={handleDragOver}
  className="w-full max-w-5xl h-[80vh] bg-dark border border-gold shadow-lg rounded-xl p-6 flex flex-col"
>
  <div className="flex-1 overflow-y-auto pr-2 mb-2">
    {messages.map((msg, idx) => (
      <div key={idx} className={`mb-3 ${msg.role === 'user' ? 'text-right' : 'text-left'}`}>
        <div className={`inline-block px-5 py-4 rounded-lg shadow-sm max-w-[95%] ${msg.role === 'user'
    ? 'bg-blue-200 text-black'
    : 'bg-[#1a1a1a] border border-gold text-white'
  }`}>
          <p className="font-semibold">{msg.role === 'user' ? 'You' : 'Comma'}:</p>
          <p className="whitespace-pre-line">{msg.text}</p>
          {msg.image && (
            <p className="text-sm text-gray-400 mt-1">
              📎 {msg.image}
            </p>
          )}
          {msg.results?.length > 0 && (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-3">
              {msg.results.map((item, i) => (
                <div key={i} className="bg-dark border border-gold p-3 rounded-md shadow-sm">
                  {item.image_path && (
                    <img
                      src={`${BACKEND_URL}/${item.image_path}`}
                      alt={item.name}
                      className="w-full h-32 object-contain mb-2"
                    />
                  )}
                  <p className="font-bold text-gold">{item.name}</p>
                  <p className="text-sm text-gray-200">{item.description}</p>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    ))}
    {loading && <p className="italic text-gold">Thinking…</p>}
  </div>


        <div className="flex items-center gap-2 mt-auto">
          <input
            type="text"
            value={input}
            onChange={e => setInput(e.target.value)}
            onKeyDown={e => {
                if (e.key == 'Enter') {
                    handleSend();
                }
            }}
            className="flex-1 border rounded px-3 py-2 text-black"
            placeholder="Type your query..."
          />
          <input
            type="file"
            accept="image/*"
            id="file-input"
            onChange={e => handleFile(e.target.files[0])}
            className="hidden"
          />
          <label htmlFor="file-input" className="group flex items-center justify-center h-10 px-3 bg-dark border border-gold rounded hover:bg-gold transition">
            <FaCamera className="text-gold group-hover:text-dark transition" size={18} />
          </label>
          <button
            onClick={handleSend}
            className="ml-2 h-10 px-4 bg-gold text-dark font-semibold rounded hover:bg-deepGold transition">
            Send
          </button>
        </div>

        {imageFile && (
          <div className="text-sm text-gold mt-1 flex justify-between items-center">
            <span>📎 {imageFile.name}</span>
            <button onClick={() => setImageFile(null)} className="text-red-500 ml-2 hover:underline">Remove</button>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
