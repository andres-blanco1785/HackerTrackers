import ReactFlow, { MiniMap, Controls } from 'react-flow-renderer';



const graphStyles = { width: "100%", height: "500px" ,      background: '#D6D5E6',
      color: '#333',
      border: '1px solid #222138', };
function Flow({ nodes, edges, onNodesChange, onEdgesChange, onConnect }) {
  return (
    <ReactFlow
      nodes={nodes}
      edges={edges}
      onNodesChange={onNodesChange}
      onEdgesChange={onEdgesChange}
      onConnect={onConnect}
      style = {graphStyles}
    >
      <MiniMap />
      <Controls />
    </ReactFlow>
  );
}

export default Flow;