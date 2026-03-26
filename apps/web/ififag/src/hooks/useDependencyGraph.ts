import { useState, useEffect, useCallback } from 'react';
import type { Node, Edge } from 'reactflow';
import dagre from 'dagre';
import { api } from '../services/api';
import type { DependencyNode, DependencyEdge } from '../types';

export interface CourseNodeData {
    id: string;
    title: string;
    department: string;
    credits: number;
    level: string;
    isRoot?: boolean;
    prerequisiteType?: 'mandatory' | 'recommended';
}

const NODE_WIDTH = 250;
const NODE_HEIGHT = 100;

const getLayoutedElements = (nodes: Node[], edges: Edge[]) => {
    const g = new dagre.graphlib.Graph();
    g.setDefaultEdgeLabel(() => ({}));
    g.setGraph({ rankdir: 'TB', ranksep: 80, nodesep: 50 });

    nodes.forEach((node) => {
        g.setNode(node.id, { width: NODE_WIDTH, height: NODE_HEIGHT });
    });

    edges.forEach((edge) => {
        g.setEdge(edge.source, edge.target);
    });

    dagre.layout(g);

    const layoutedNodes = nodes.map((node) => {
        const nodeWithPosition = g.node(node.id);
        return {
            ...node,
            position: {
                x: nodeWithPosition.x - NODE_WIDTH / 2,
                y: nodeWithPosition.y - NODE_HEIGHT / 2,
            },
        };
    });

    return { nodes: layoutedNodes, edges };
};

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

            // Build a map of node id -> prerequisite type from edges
            // An edge { source: prereqId, target: courseId, type } means
            // the prereq node's type relative to the target
            const nodeTypeMap: Record<string, string> = {};
            for (const edge of response.edges) {
                // source is the prerequisite, target is the dependent course
                // The prereq type is determined by the edge
                if (!nodeTypeMap[edge.source]) {
                    nodeTypeMap[edge.source] = edge.type || 'mandatory';
                }
            }

            const transformedNodes: Node<CourseNodeData>[] = response.nodes.map((node: DependencyNode) => ({
                id: node.id,
                type: 'courseNode',
                position: { x: 0, y: 0 }, // will be set by dagre
                data: {
                    id: node.id,
                    title: node.label,
                    department: node.department,
                    credits: node.credits,
                    level: node.level,
                    isRoot: node.id === id,
                    prerequisiteType: node.id === id ? undefined : (nodeTypeMap[node.id] as 'mandatory' | 'recommended') || 'mandatory',
                },
            }));

            // Reverse edge direction: selected course at top, prerequisites below
            // API gives: prereq -> course (source=prereq, target=course)
            // We want: course -> prereq (source=course, target=prereq) for dagre TB layout
            const transformedEdges: Edge[] = response.edges.map((edge: DependencyEdge) => {
                const isMandatory = (edge.type || 'mandatory') === 'mandatory';
                return {
                    id: `${edge.target}-${edge.source}`,
                    source: edge.target,
                    target: edge.source,
                    type: 'step',
                    animated: false,
                    style: {
                        stroke: isMandatory ? '#003366' : '#996600',
                        strokeWidth: 2,
                        strokeDasharray: isMandatory ? undefined : '5 5',
                    },
                };
            });

            const { nodes: layoutedNodes, edges: layoutedEdges } = getLayoutedElements(
                transformedNodes,
                transformedEdges
            );

            setNodes(layoutedNodes);
            setEdges(layoutedEdges);
        } catch (err) {
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
