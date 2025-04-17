import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import OverviewPage from './pages/OverviewPage';
import ClustersPage from './pages/ClustersPage';
import SystemPage from './pages/SystemPage';

function App() {
  return (
    // Using BrowserRouter for standard routing
    <Router>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<OverviewPage />} />
          <Route path="clusters" element={<ClustersPage />} />
          <Route path="system" element={<SystemPage />} />
        </Route>
      </Routes>
    </Router>
  );
}

export default App; 