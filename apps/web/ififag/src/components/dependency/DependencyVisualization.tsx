// apps/web/src/components/dependency/DependencyVisualization.tsx
import React, { useCallback, useState, useEffect } from 'react';
import ReactFlow, {
  ReactFlowProvider,
  Controls,
  Background,
  useNodesState,
  useEdgesState,
  ConnectionMode,
  Panel,
} from 'reactflow';
import type { Node, Edge } from 'reactflow';
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

export const DependencyVisualization: React.FC<DependencyVisualizationProps> = ({
  courseId,
  onCourseClick,
}) => {
  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);
  const [selectedNode, setSelectedNode] = useState<string | null>(null);

  const { nodes: graphNodes, edges: graphEdges, loading, error } = useDependencyGraph(courseId);

  // Update nodes and edges when graph data changes
  useEffect(() => {
    if (graphNodes && graphEdges) {
      setNodes(graphNodes);
      setEdges(graphEdges);
    }
  }, [graphNodes, graphEdges, setNodes, setEdges]);

  const onNodeClick = useCallback(
    (event: React.MouseEvent, node: Node) => {
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
      <div className="flex items-center justify-center h-full">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
          <p className="mt-2 text-gray-600">Laster avhengigheter...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="text-center text-red-600">
          <p>Feil ved lasting av avhengigheter</p>
          <p className="text-sm">{error}</p>
        </div>
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
        attributionPosition="bottom-left"
      >
        <Background color="#f1f5f9" gap={16} />
        <Controls />
        
        <Panel position="top-right">
          <div className="bg-white p-3 rounded-lg shadow-lg">
            <h4 className="font-semibold text-sm mb-2">Emnekart</h4>
            <p className="text-xs text-gray-600 mb-2">
              Klikk på emner for å utforske
            </p>
            {selectedNode && (
              <div className="text-xs">
                <span className="font-medium">Valgt: </span>
                <span className="text-blue-600">{selectedNode}</span>
              </div>
            )}
          </div>
        </Panel>
      </ReactFlow>
    </ReactFlowProvider>
  );
};