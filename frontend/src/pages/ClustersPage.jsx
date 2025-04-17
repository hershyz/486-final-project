import React, { useState, useEffect } from 'react';
import Card from '../components/Card';
import { stubData } from '../stubData';

import { useWebSocket } from '../WebSocket';

const ClustersPage = () => {
  //const data = stubData.clusters;

  const {clusters} = useWebSocket()

  const sortedClusters = Object.entries(clusters)
    .map(([key, value]) => ({
      cluster: key,
      ...value,
    }))
    .sort((a, b) => b.Score - a.Score); // Sorting clusters by Score

    return (
      <div>
      <h1 className="text-2xl font-semibold text-gray-900 mb-6">Cluster Explorer</h1>
    
      <Card>
        <div className="space-y-4">
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
            {/* Suspicious Clusters */}
            <div>
              <h2 className="text-xl font-semibold text-red-600 mb-4">Suspicious Clusters</h2>
              {Object.entries(clusters).sort((a, b) => { const idA = parseInt(a[0], 10); const idB = parseInt(b[0], 10); return idB - idA;})
                .filter(([id, cluster]) => cluster.Suspicous)
                .slice(0, 10) // Top 10 suspicious clusters
                .map(([key, cluster], index) => (
                  <div
                    key={index}
                    className="p-4 border rounded-lg shadow-md bg-red-100 border-red-500 mb-4"
                  >
                    <div className="font-semibold text-lg">
                      <strong>Cluster {key}</strong> (Score: {cluster.Score})
                    </div>
                    <div className="mt-2">
                      <strong>Keywords:</strong> {cluster.keywords.join(', ')}
                    </div>
                    <div className="mt-2">
                      <strong>Status:</strong>{' '}
                      <span className="font-bold text-red-600">Suspicious</span>
                    </div>
                  </div>
                ))}
            </div>
    
            {/* Non-Suspicious Clusters */}
            <div>
              <h2 className="text-xl font-semibold text-green-600 mb-4">Non-Suspicious Clusters</h2>
              {Object.entries(clusters).sort((a, b) => { const idA = parseInt(a[0], 10); const idB = parseInt(b[0], 10); return idB - idA;})
                 .filter(([id, cluster]) => cluster.Suspicous !== true)
                .slice(0, 10) // Top 10 non-suspicious clusters
                .map(([key, cluster], index) => (
                  <div
                    key={index}
                    className="p-4 border rounded-lg shadow-md bg-green-100 border-green-500 mb-4"
                  >
                    <div className="font-semibold text-lg">
                      <strong>Cluster {key}</strong> (Score: {cluster.Score})
                    </div>
                    <div className="mt-2">
                      <strong>Keywords:</strong> {cluster.keywords.join(', ')}
                    </div>
                    <div className="mt-2">
                      <strong>Status:</strong>{' '}
                      <span className="font-bold text-green-600">Non-Suspicious</span>
                    </div>
                  </div>
                ))}
            </div>
          </div>
        </div>
      </Card>
    </div>
    
    );
  
};

export default ClustersPage; 