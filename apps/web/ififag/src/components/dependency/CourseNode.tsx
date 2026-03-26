import { memo } from 'react';
import { Handle, Position } from 'reactflow';
import type { NodeProps } from 'reactflow';
import './CourseNode.css';

interface CourseNodeData {
    id: string;
    title: string;
    department: string;
    credits: number;
    level: string;
    isRoot?: boolean;
    isSelected?: boolean;
    prerequisiteType?: 'mandatory' | 'recommended';
}

const CourseNode = ({ data, selected }: NodeProps<CourseNodeData>) => {
    const nodeClass = data.isRoot
        ? 'root'
        : data.prerequisiteType === 'recommended'
        ? 'recommended'
        : 'mandatory';

    return (
        <div className={`course-node ${nodeClass} ${selected ? 'selected' : ''}`}>
            <Handle
                type='target'
                position={Position.Top}
                className='handle handle-target'
            />

            <div className='course-content'>
                <div className={`course-badge ${nodeClass}`}>{data.id}</div>
                <div className='course-title'>{data.title}</div>
                <div className='course-meta'>
                    <span className='credits'>{data.credits} studiepoeng</span>
                </div>
            </div>

            <Handle
                type='source'
                position={Position.Bottom}
                className='handle handle-source'
            />
        </div>
    );
};

export default memo(CourseNode);
