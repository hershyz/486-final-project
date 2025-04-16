// src/stubData.js

export const stubData = {
  overview: {
    totalDocumentsProcessed: 0,
    totalClustersCreated: 0,
    untrustedClustersCount: 0,
    clusterSizeDistribution: "No cluster data available.",
    documentInitialAssessmentRatio: "No documents assessed yet.",
    currentlyUntrustedClusters: "No untrusted clusters identified.",
  },
  realtime: {
    avgProcessingLatency: "--",
    throughput: "--",
    queueLength: "--",
    recentlyProcessedFeed: "No recent documents found.",
    latencyUnit: "ms",
    throughputUnit: "docs/sec",
    // Placeholder for potential future list of documents
    recentDocuments: [], // e.g., [{id: 1, title: "Doc Title 1", status: "Processed"}, ...]
  },
  clusters: {
    // Placeholder for potential future list of clusters
    clusterList: [], // e.g., [{id: 1, size: 10, trustworthiness: 0.8, keywords: ["keyword1", "keyword2"]}, ...]
    statusMessage: "No clusters found.",
  },
  documents: {
    // Placeholder for potential future list of documents
    documentList: [], // e.g., [{id: 1, title: "Doc Title 1", contentSnippet: "...", assessment: "Real (0.9)"}, ...]
    statusMessage: "No documents found.",
  },
  system: {
    offlineModelPerformance: {
      classifierAccuracy: "96.00%",
      trustworthinessMAE: "0.15 (Placeholder)",
    },
    onlineClusteringPerformance: "Online metrics like Silhouette Score are not currently implemented.",
    keyHyperparameters: {
      "Document Title Weight Factor": 1.4,
      "Cosine Similarity Threshold": 0.7,
      "Untrusted Cluster Threshold": 0.2,
      "Cluster Keyword Threshold (Polarity)": 0.3,
    },
  },
}; 