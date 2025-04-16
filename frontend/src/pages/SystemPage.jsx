import React from 'react';
import Card from '../components/Card';
import { stubData } from '../stubData';

const SystemPage = () => {
  const data = stubData.system;

  return (
    <div>
      <h1 className="text-2xl font-semibold text-gray-900 mb-6">System & Model Metrics</h1>
      
      {/* Top Row */}
      <div className="grid grid-cols-1 gap-5 md:grid-cols-2 mb-5">
        <Card title="Offline Model Performance">
          <dl className="space-y-2">
            <div className="flex justify-between text-sm">
              <dt className="text-gray-600">Untrusted Cluster Classifier Accuracy:</dt>
              <dd className="font-medium text-gray-900">{data.offlineModelPerformance.classifierAccuracy}</dd>
            </div>
            <div className="flex justify-between text-sm">
              <dt className="text-gray-600">Cluster Trustworthiness MAE:</dt>
              <dd className="font-medium text-gray-900">{data.offlineModelPerformance.trustworthinessMAE}</dd>
            </div>
          </dl>
        </Card>
        <Card title="Online Clustering Performance">
          <p className="text-sm text-gray-700">{data.onlineClusteringPerformance}</p>
        </Card>
      </div>

      {/* Bottom Section */}
      <Card title="Key Hyperparameters">
         <dl className="space-y-2">
            {Object.entries(data.keyHyperparameters).map(([key, value]) => (
              <div key={key} className="flex justify-between text-sm">
                <dt className="text-gray-600">{key}:</dt>
                <dd className="font-medium text-gray-900">{value}</dd>
              </div>
            ))}
          </dl>
      </Card>

    </div>
  );
};

export default SystemPage; 