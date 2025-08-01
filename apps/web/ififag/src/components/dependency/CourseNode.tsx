import React, { memo } from 'react';
import { Handle } from 'reactflow';
import type { NodeProps } from 'reactflow';
import { Position } from 'reactflow';

interface CourseNodeData {
    id: string;
    title: string;
    department: string;
    credits: number;
    level: string;
    isSelected?: boolean;
}

const CourseNode: React.FC<NodeProps<CourseNodeData>> = ({ data, selected }) => {
    return (
        <div className={`course-node ${selected  ? 'selected' : ''}`}>
            {/* Handle is a node's connection point, here it gets connected if its a target. On top of the node*/}
            <Handle 
                type='target'
                position={Position.Top}
                className='handle handle-target'
            />

            <div className='course-content'>
                <div className='course-badge'>{data.id}</div>
                <div className='course-title'>{data.title}</div>
                <div className='course-meta'>
                    <span className='credits'>{data.credits} studiepoeng</span>
                </div>
            </div>
            
            {/* Here it gets connected if its a source. On bottom of the node*/}
            <Handle
                type='source'
                position={Position.Bottom}
                className='handle handle-source'
            />
        </div>
    );
};
{/* memo() prevents unnecessary re-renders */}
export default memo(CourseNode);
