import { memo } from 'react';
import { Handle, Position } from 'reactflow';
import type { NodeProps } from 'reactflow';

interface CourseNodeData {
    id: string;
    title: string;
    department: string;
    credits: number;
    level: string;
    isRoot?: boolean;
}

const CourseNode = ({ data, selected }: NodeProps<CourseNodeData>) => {
    return (
        <div className={`course-node ${selected ? 'selected' : ''} ${data.isRoot ? 'root' : ''}`}>
            <Handle
                type='target'
                position={Position.Top}
                className='handle handle-target'
            />

            <div className='course-content'>
                <div className={`course-badge ${data.isRoot ? 'root-badge' : ''}`}>{data.id}</div>
                <div className='course-title'>{data.title}</div>
                <div className='course-meta'>
                    <span className='credits'>{data.credits} stp</span>
                    <span className='level'>{data.level}</span>
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
