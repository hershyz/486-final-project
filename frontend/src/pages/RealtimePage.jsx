import React from 'react';
import Card from '../components/Card';
import { stubData } from '../stubData';

const RealtimePage = () => {
  const data = stubData.realtime;

  return (
    <div>
      <h1 className="text-2xl font-semibold text-gray-900 mb-6">Real-time Monitoring</h1>
      
      {/* Top Row */}
      <div className="grid grid-cols-1 gap-5 sm:grid-cols-3 mb-5">
        <Card title="Avg. Processing Latency">
          <p className="text-3xl font-semibold text-gray-900">{data.avgProcessingLatency} <span className="text-xl">{data.latencyUnit}</span></p>
          <p className="text-xs text-gray-500">(Not Implemented)</p>
        </Card>
        <Card title="Throughput">
           <p className="text-3xl font-semibold text-gray-900">{data.throughput} <span className="text-xl">{data.throughputUnit}</span></p>
           <p className="text-xs text-gray-500">(Not Implemented)</p>
        </Card>
        <Card title="Queue Length">
           <p className="text-3xl font-semibold text-gray-900">{data.queueLength}</p>
           <p className="text-xs text-gray-500">(Not Implemented)</p>
        </Card>
      </div>

      {/* Bottom Section */}
      <Card title="Recently Processed Documents Feed">
         <p className="text-sm text-gray-700">{data.recentlyProcessedFeed}</p>
         {/* Placeholder for future list/table display */}
         {data.recentDocuments.length === 0 && (
            <p className="text-sm text-gray-500 mt-2">No recent documents found.</p>
         )}
         {/* TODO: Map data.recentDocuments to a list/table when available */}
      </Card>

    </div>
  );
};

export default RealtimePage; 