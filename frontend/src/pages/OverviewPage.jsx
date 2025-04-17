import React from 'react';
import Card from '../components/Card';
import { stubData } from '../stubData';

import { useWebSocket } from '../WebSocket';

const OverviewPage = () => {
  const data = stubData.overview;

  const {clusters, numberClusters, numberDocuments,numberUntruestedClusters, untrusted_clusters, documents } = useWebSocket()

  return (
    <div>
      <h1 className="text-2xl font-semibold text-gray-900 mb-6">System Overview</h1>
  
      {/* Top Row */}
      <div className="grid grid-cols-1 gap-5 sm:grid-cols-3 mb-5">
        <Card title="Total Documents Processed">
          <p className="text-3xl font-bold text-gray-900">{numberDocuments}</p>
        </Card>
        <Card title="Total Clusters Created">
          <p className="text-3xl font-bold text-gray-900">{numberClusters}</p>
        </Card>
        <Card title="Untrusted Clusters">
          <p className="text-3xl font-bold text-gray-900">{numberUntruestedClusters}</p>
        </Card>
      </div>
  
{/* Second Row */}
<div className="grid grid-cols-1 gap-5  mb-5 w-full h-full">
  <Card title="Most Recent 5 Suspicous Documents" className="w-full h-full">

    <div className="mt-4 flex-row gap-5 overflow-x-auto w-full h-full">
      {documents
       .filter(doc => doc.cluster_id.some(id => id in untrusted_clusters))
      .sort((a,b) => { const idA = parseInt(a.document_id, 10); const idB = parseInt(b.document_id, 10);
  return idB - idA;
})
        .slice(0, 5) // Get the top 5 entries
        .map((document, index) => (
          <div
            key={index}
            className="mb-4 flex flex-col bg-red-50 border border-red-400 text-red-800 p-3 rounded-xl shadow-md hover:shadow-lg transition-shadow duration-300 w-full"
          >
            <div className="font-semibold text-red-700 text-sm">🚨 Suspicious Document</div>
            <div className="mt-2 text-xs"><strong>Document ID:</strong> {document.document_id}</div>
            <div className="mt-2 text-xs"><strong>Document Title:</strong> {document.title}</div>
            <div className="mt-2 text-xs"><strong>Document Content:</strong> {" "} 
            {document.content.length > 250 ? document.content.slice(0, 500) + "..." : document.content}</div>
          </div>
        ))}
    </div>
  </Card>
</div>
    </div>
  );
  


};

export default OverviewPage; 