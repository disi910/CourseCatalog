import { useCallback, useState, useEffect } from 'react';
import ReactFlow, {
  ReactFlowProvider,
  Controls,
  Background,
  useNodesState,
  useEdgesState,
  ConnectionMode,
  Panel,
} from 'reactflow';
import type { Node } from 'reactflow';
import 'reactflow/dist/style.css';

import CourseNode from './CourseNode';
import { useDependencyGraph } from '../../hooks/useDependencyGraph';

const nodeTypes = {
  courseNode: CourseNode,
};

interface DependencyVisualizationProps {
  courseId: string;
  onCourseClick?: (courseId: string) => void;
}

export const DependencyVisualization = ({
  courseId,
  onCourseClick,
}: DependencyVisualizationProps) => {
  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);
  const [selectedNode, setSelectedNode] = useState<string | null>(null);

  const { nodes: graphNodes, edges: graphEdges, loading, error } = useDependencyGraph(courseId);

  useEffect(() => {
    setNodes(graphNodes);
    setEdges(graphEdges);
  }, [graphNodes, graphEdges, setNodes, setEdges]);

  const onNodeClick = useCallback(
    (_event: React.MouseEvent, node: Node) => {
      setSelectedNode(node.id);
      onCourseClick?.(node.id);
    },
    [onCourseClick]
  );

  const onPaneClick = useCallback(() => {
    setSelectedNode(null);
  }, []);

  if (loading) {
    return (
      <div style={{height: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
        <div className="text-center">
          <div className="retro-loading-indicator">
            <span className="retro-blink">*** Loading ***</span>
          </div>
          <p className="mt-2" style={{color: '#666'}}>Laster avhengigheter...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div style={{height: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
        <div className="retro-error" style={{textAlign: 'center'}}>
          <p className="retro-error-title">Feil ved lasting av avhengigheter</p>
          <p>{error}</p>
        </div>
      </div>
    );
  }

  if (nodes.length === 0) {
    return (
      <div style={{height: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
        <p style={{color: '#666', fontSize: '12px'}}>Ingen avhengigheter funnet for dette emnet.</p>
      </div>
    );
  }

  return (
    <ReactFlowProvider>
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onNodeClick={onNodeClick}
        onPaneClick={onPaneClick}
        nodeTypes={nodeTypes}
        connectionMode={ConnectionMode.Loose}
        fitView
        fitViewOptions={{ padding: 0.3 }}
        attributionPosition="bottom-left"
      >
        <Background color="#cccccc" gap={16} />
        <Controls />

        <Panel position="top-right">
          <div className="retro-flow-panel">
            <h4>Emnekart</h4>
            <p>Klikk på emner for å utforske</p>
            <p style={{fontSize: '10px', color: '#999'}}>
              {nodes.length} emner, {edges.length} avhengigheter
            </p>
            {selectedNode && (
              <div style={{fontSize: '10px', marginTop: '4px'}}>
                <span style={{fontWeight: 'bold'}}>Valgt: </span>
                <span style={{fontFamily: 'Courier New, monospace', color: '#003366'}}>{selectedNode}</span>
              </div>
            )}
          </div>
        </Panel>
      </ReactFlow>
    </ReactFlowProvider>
  );
};
