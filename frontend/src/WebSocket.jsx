import React, { createContext, useContext, useEffect, useRef, useState } from 'react';

// create a null websocket context
const webSocketContext = createContext(null);

// allows any component to use the WebSocket hook
export const useWebSocket = () => useContext(webSocketContext);

export const WebSocketProvider = ({ children }) => {
    // store a reference to the socket that isn't changed upon re-render
    const socketRef = useRef(null);
    
    
    const [numberDocuments, setNumberDocuments] = useState(0);
    const [documents, setDocuments] = useState([])

    const [numberClusters, setNumberClusters] = useState(0)
    const [clusters, setClusters] = useState({})

    const [numberUntruestedClusters, setNumberUntrustedClusters] = useState(0)
    const [untrusted_clusters, setUntrustedClusters] = useState({})



    useEffect(() => {
      const filtered = Object.entries(clusters).filter(([key, value]) => value['Suspicous']).reduce((obj, [key, value]) => { obj[key] = value; return obj;}, {});

      setUntrustedClusters(filtered)
      setNumberUntrustedClusters(Object.keys(filtered).length)

    }, [clusters]);



    useEffect(() => {
        socketRef.current = new WebSocket('ws://localhost:8080');
        
        socketRef.current.onmessage = (event) => {

         const parsedData = JSON.parse(event.data); 

          const document = parsedData.doc
          const ClusterChanges = parsedData.ClusterData

          const updatedClusters = {};
          let NewClusters = 0;


          for (let cluster in ClusterChanges){
            if (!(cluster in clusters)){  NewClusters += 1; }

            updatedClusters[cluster] = {'Score': ClusterChanges[cluster][0], 'keywords': ClusterChanges[cluster][1], 'Suspicous': ClusterChanges[cluster][2]}

            if(!("cluster_id" in document)){
              document['cluster_id'] = [cluster]
            }else{
              document['cluster_id'].push(cluster)
            }

          }

          console.log(document)

          setClusters(prevClusters => ({...prevClusters,  ...updatedClusters  }));

          setNumberClusters(prev => prev + NewClusters);
          

          setNumberDocuments(prev => prev + 1);
          setDocuments(docs => [...docs, document])



        };
    
        socketRef.current.onerror = (err) => {
          console.error('WebSocket error:', err);
        };

        socketRef.current.onclose = (event) => {
          console.warn('WebSocket closed:', event);
        };
    
        return () => {
          socketRef.current?.close();
        };
      }, []);

      // allows me to provide the values to all the children components
      return (
        <webSocketContext.Provider value={{ numberDocuments, documents, numberClusters, clusters, numberUntruestedClusters, untrusted_clusters}}>
          {children}
        </webSocketContext.Provider>
      );

};