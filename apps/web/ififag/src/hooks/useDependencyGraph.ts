import { useState, useEffect, useCallback } from 'react';
import type { Node, Edge } from 'reactflow';
import { api } from '../services/api';
import type { DependencyNode, DependencyEdge } from '../types';

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

            setNodes(transformToNodes(response.nodes));
            setEdges(transformToEdges(response.edges));
        } catch(err) {
            setError('Failed to load dependencies');
            console.error(err);
        } finally {
            setLoading(false);
        }
    }, []);

    useEffect(() => {
        if (courseId) {
            fetchDependencyData(courseId);
        }
    }, [courseId, fetchDependencyData]);

    return { nodes, edges, loading, error };
};

const transformToNodes = (apiNodes: DependencyNode[]): Node[] => {
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
};

const transformToEdges = (apiEdges: DependencyEdge[]): Edge[] => {
    return apiEdges.map((edge) => ({
        id: `${edge.source}-${edge.target}`,
        source: edge.source,
        target: edge.target,
        type: 'step',
        animated: false,
        style: { stroke: '#003366', strokeWidth: 2 },
    }));
};

const calculatePosition = (index: number, total: number) => {
    const radius = 300;
    const angle = (index / total) * 2 * Math.PI;
    return {
        x: Math.cos(angle) * radius,
        y: Math.sin(angle) * radius,
    };
};
