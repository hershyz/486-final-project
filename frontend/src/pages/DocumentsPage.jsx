import React from 'react';
import Card from '../components/Card';
import { stubData } from '../stubData';

const DocumentsPage = () => {
  const data = stubData.documents;

  // Basic handler for search button click (does nothing functional)
  const handleSearch = () => {
    console.log('Search button clicked (no action)');
  };


  function tokenize(text) {
    return text
      .toLowerCase()
      .replace(/[^a-z0-9\s]/g, '')
      .split(/\s+/)   
      .filter(Boolean);     
  }

  return (
    <div>
      <h1 className="text-2xl font-semibold text-gray-900 mb-6">Document Explorer</h1>
      
      {/* Search Area */}
      <div className="mb-5">
        <Card>
          <div className="flex items-center space-x-2">
            <input 
              type="text" 
              placeholder="Search Title/Content..." 
              className="flex-grow px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
            />
            <button 
              onClick={handleSearch}
              className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            >
              Search
            </button>
          </div>
        </Card>
      </div>

      {/* Content Area */}
      <Card>
        {data.documentList.length === 0 ? (
            <p className="text-sm text-gray-700">{data.statusMessage}</p>
          ) : (
            <div>
              {/* TODO: Implement document list rendering here when data is available */}
              <p>Document list would go here.</p> 
            </div>
        )}
      </Card>

    </div>
  );
};

export default DocumentsPage; 