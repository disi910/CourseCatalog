import { useState, useEffect, useCallback } from 'react';
import type { Node } from 'reactflow';
import type { Edge } from 'reactflow';
import { api } from '../services/api';

// Data transformation logic
// Creating a Custom Hook for Data Processing
// Custom hook pattern for reusable logic?
export const useDependencyGraph = (courseId: string | null) => {
    const [nodes, setNodes] = useState<Node[]>([]);
    const [edges, setEdges] = useState<Edge[]>([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const fetchDependencyData = useCallback(async (id: string) => {
        try {
            setLoading(true);
            setError(null);

            const response = await api.getCourseDependencies(id);

            // Transform API data to react flow format

            const transformedNodes = transformToNodes(response.nodes);
            const transformedEdges = transformToEdges(response.edges);

            setNodes(transformedNodes);
            setEdges(transformedEdges);
        } catch(err) {
            setError('Failed to load dependencies');
            console.error(err);
        } finally {
            setLoading(false);
        }
    }, []); // Empty dependency array means this function never changes

    useEffect(() => {
        if (courseId) {
            fetchDependencyData(courseId);
        }
    }, [courseId, fetchDependencyData]);

    return { nodes, edges, loading, error};
};

const transformToNodes = (apiNodes: any[]): Node[] => {
    return apiNodes.map((node, index) => ({
        id: node.id,
        type: 'courseNode',
        position: calculatePosition(index, apiNodes.length),
        data: {
            id: node.id,
            title: node.label,
            department: node.department,
            credits: node.credits,
            level: node.level,
        },
    }));
}

const transformToEdges = (apiEdges: any[]): Edge[] => {
  return apiEdges.map((edge) => ({
    id: `${edge.source}-${edge.target}`,
    source: edge.source,
    target: edge.target,
    type: 'smoothstep', // Built-in edge type
    animated: true,
    style: { stroke: '#3b82f6', strokeWidth: 2 },
  }));
};

// Algorithm for automatic layout
const calculatePosition = (index: number, total: number) => {
    const radius = 300;
    const angle = (index / total) * 2 * Math.PI;

    return {
        x: Math.cos(angle) * radius,
        y: Math.sin(angle) * radius,
    };
};