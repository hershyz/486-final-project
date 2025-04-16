import React from 'react';
import Card from '../components/Card';
import { stubData } from '../stubData';

const OverviewPage = () => {
  const data = stubData.overview;

  return (
    <div>
      <h1 className="text-2xl font-semibold text-gray-900 mb-6">System Overview</h1>
      
      {/* Top Row */}
      <div className="grid grid-cols-1 gap-5 sm:grid-cols-3 mb-5">
        <Card title="Total Documents Processed">
          <p className="text-3xl font-bold text-gray-900">{data.totalDocumentsProcessed}</p>
        </Card>
        <Card title="Total Clusters Created">
          <p className="text-3xl font-bold text-gray-900">{data.totalClustersCreated}</p>
        </Card>
        <Card title="Untrusted Clusters">
          <p className="text-3xl font-bold text-gray-900">{data.untrustedClustersCount}</p>
        </Card>
      </div>

      {/* Second Row */}
      <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 mb-5">
        <Card title="Cluster Size Distribution">
          <p className="text-sm text-gray-700">{data.clusterSizeDistribution}</p>
        </Card>
        <Card title="Document Initial Assessment Ratio">
          <p className="text-sm text-gray-700">{data.documentInitialAssessmentRatio}</p>
        </Card>
      </div>

      {/* Third Row */}
      <Card title="Currently Untrusted Clusters">
         <p className="text-sm text-gray-700">{data.currentlyUntrustedClusters}</p>
         {/* Placeholder for future list display */}
      </Card>

    </div>
  );
};

export default OverviewPage; 