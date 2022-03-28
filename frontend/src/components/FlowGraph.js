import ReactFlow, { MiniMap, Controls } from 'react-flow-renderer';



const graphStyles = { width: "100%", height: "500px" };
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