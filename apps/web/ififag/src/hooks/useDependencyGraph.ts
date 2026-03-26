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

            if (!response || !response.nodes || response.nodes.length === 0) {
                setNodes([]);
                setEdges([]);
                return;
            }

            const transformedNodes = transformToNodes(response.nodes, response.edges, id);
            const transformedEdges = transformToEdges(response.edges);

            setNodes(transformedNodes);
            setEdges(transformedEdges);
        } catch(err) {
            setError('Kunne ikke laste avhengigheter');
            console.error(err);
        } finally {
            setLoading(false);
        }
    }, []);

    useEffect(() => {
        if (courseId) {
            fetchDependencyData(courseId);
        } else {
            setNodes([]);
            setEdges([]);
        }
    }, [courseId, fetchDependencyData]);

    return { nodes, edges, loading, error };
};

const transformToNodes = (apiNodes: DependencyNode[], apiEdges: DependencyEdge[], rootId: string): Node[] => {
    // Build a hierarchical layout: root at bottom, prerequisites above
    const levels = assignLevels(apiNodes, apiEdges, rootId);
    const maxLevel = Math.max(...Object.values(levels), 0);

    // Group nodes by level for horizontal spacing
    const nodesByLevel: Record<number, DependencyNode[]> = {};
    for (const node of apiNodes) {
        const level = levels[node.id] ?? 0;
        if (!nodesByLevel[level]) nodesByLevel[level] = [];
        nodesByLevel[level].push(node);
    }

    const NODE_WIDTH = 220;
    const HORIZONTAL_GAP = 40;
    const VERTICAL_GAP = 140;

    return apiNodes.map((node) => {
        const level = levels[node.id] ?? 0;
        const nodesAtLevel = nodesByLevel[level];
        const indexInLevel = nodesAtLevel.indexOf(node);
        const totalWidth = nodesAtLevel.length * NODE_WIDTH + (nodesAtLevel.length - 1) * HORIZONTAL_GAP;

        // Center nodes horizontally, root at bottom
        const x = indexInLevel * (NODE_WIDTH + HORIZONTAL_GAP) - totalWidth / 2 + NODE_WIDTH / 2;
        const y = (maxLevel - level) * VERTICAL_GAP;

        return {
            id: node.id,
            type: 'courseNode',
            position: { x, y },
            data: {
                id: node.id,
                title: node.label,
                department: node.department,
                credits: node.credits,
                level: node.level,
                isRoot: node.id === rootId,
            },
        };
    });
};

// Assign depth levels: root = 0, direct prerequisites = 1, etc.
const assignLevels = (
    nodes: DependencyNode[],
    edges: DependencyEdge[],
    rootId: string
): Record<string, number> => {
    const levels: Record<string, number> = {};
    const visited = new Set<string>();

    const traverse = (nodeId: string, level: number) => {
        if (visited.has(nodeId)) {
            // Update level if we found a deeper path
            levels[nodeId] = Math.max(levels[nodeId] ?? 0, level);
            return;
        }
        visited.add(nodeId);
        levels[nodeId] = Math.max(levels[nodeId] ?? 0, level);

        // Find prerequisites of this node (edges where target = nodeId)
        const prereqEdges = edges.filter(e => e.target === nodeId);
        for (const edge of prereqEdges) {
            traverse(edge.source, level + 1);
        }
    };

    traverse(rootId, 0);

    // Assign level 0 to any orphan nodes not reachable from root
    for (const node of nodes) {
        if (levels[node.id] === undefined) {
            levels[node.id] = 0;
        }
    }

    return levels;
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
