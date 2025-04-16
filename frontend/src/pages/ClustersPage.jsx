import React from 'react';
import Card from '../components/Card';
import { stubData } from '../stubData';

const ClustersPage = () => {
  const data = stubData.clusters;

  return (
    <div>
      <h1 className="text-2xl font-semibold text-gray-900 mb-6">Cluster Explorer</h1>
      
      <Card>
        {/* Check if there are clusters to display, otherwise show status message */}
        {data.clusterList.length === 0 ? (
          <p className="text-sm text-gray-700">{data.statusMessage}</p>
        ) : (
          <div>
            {/* TODO: Implement cluster list rendering here when data is available */}
            <p>Cluster list would go here.</p> 
          </div>
        )}
      </Card>

    </div>
  );
};

export default ClustersPage; 