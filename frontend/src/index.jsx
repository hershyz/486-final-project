import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css'; // Import Tailwind CSS
import App from './App'; // Ensure this points to App.jsx
import { WebSocketProvider } from './WebSocket';

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <WebSocketProvider>
      <App />
    </WebSocketProvider>

  </React.StrictMode>,
) 