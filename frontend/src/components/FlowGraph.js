import ReactFlow, { MiniMap, Controls } from 'react-flow-renderer';



const graphStyles = {
    height: "700px" ,
    color: '#333',
    border: '1px solid #222138',

};
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