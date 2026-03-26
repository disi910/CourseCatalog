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
}

const CourseNode = ({ data, selected }: NodeProps<CourseNodeData>) => {
    return (
        <div className={`course-node ${selected ? 'selected' : ''} ${data.isRoot ? 'root' : ''}`}>
            <Handle
                type='target'
                position={Position.Top}
                className='handle handle-target'
            />

            {/* Windows 98 title bar */}
            <div className='course-node-titlebar'>
                <span>{data.id}</span>
                <span className='node-credits'>{data.credits} stp</span>
            </div>

            {/* Node body */}
            <div className='course-node-body'>
                <div className='course-title'>{data.title}</div>
                <div className='course-meta-row'>
                    <span className='meta-tag tag-level'>{data.level}</span>
                    {data.isRoot && <span className='meta-tag tag-root'>Valgt</span>}
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
