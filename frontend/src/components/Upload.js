import React, { useState } from 'react';

function Upload() {
  const [results, setResults] = useState([]);

  const handleUpload = async (e) => {
    const formData = new FormData();
    formData.append('image', e.target.files[0]);

    const res = await fetch('/image-search', {
      method: 'POST',
      body: formData
    });
    const data = await res.json();
    setResults(data);
  };

  return (
    <div>
      <input
        type="file"
        onChange={handleUpload}
        className="mb-4 block text-sm text-gray-500 file:mr-4 file:py-2 file:px-4
          file:rounded-full file:border-0
          file:text-sm file:font-semibold
          file:bg-blue-50 file:text-blue-700
          hover:file:bg-blue-100"
      />
      <ul className="space-y-3">
        {results.map(item => (
          <li key={item.id} className="bg-gray-50 p-3 rounded shadow-sm">
            <span className="font-medium text-gray-800">{item.name}</span><br />
            <span className="text-gray-600 text-sm">{item.description}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default Upload;