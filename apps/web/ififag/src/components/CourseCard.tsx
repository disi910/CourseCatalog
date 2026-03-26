import type { Course, CoursePrerequisite } from '../types';

interface CourseCardProps {
    course: Course;
    onClick?: () => void;
}

export const CourseCard = ({ course, onClick }: CourseCardProps) => {
    return (
        <div className="retro-card" onClick={onClick}>
            {/* Course Header */}
            <div className="retro-card-header">
                <span className="retro-card-code">{course.id}</span>
                <span className="retro-badge retro-badge-credits">
                    {course.credits} stp
                </span>
            </div>

            {/* Course title */}
            <div className="retro-card-title">{course.title}</div>
            {course.title_english && (
                <div className="retro-card-title-en">{course.title_english}</div>
            )}

            {/* Course description */}
            <div className="retro-card-desc">
                {course.description || "Ingen beskrivelse tilgjengelig"}
            </div>

            <hr />

            {/* Course metadata */}
            <div className="retro-card-meta">
                <p><span className="meta-label">Språk:</span> {course.language}</p>
                <p><span className="meta-label">Nivå:</span> {course.level}</p>
                {course.teaching_form && (
                    <p><span className="meta-label">Undervisning:</span> {course.teaching_form}</p>
                )}
                {course.exam_form && (
                    <p><span className="meta-label">Eksamen:</span> {course.exam_form}</p>
                )}
            </div>

            {/* Prerequisites */}
            {course.prerequisites && course.prerequisites.length > 0 && (
                <div style={{marginTop: '4px'}}>
                    <span className="meta-label" style={{fontSize: '11px'}}>Forkunnskaper: </span>
                    {course.prerequisites.map((prereq: CoursePrerequisite) => (
                        <span key={prereq.id} className="retro-badge retro-badge-prereq">
                            {prereq.id}
                        </span>
                    ))}
                </div>
            )}

            {/* Semester badges */}
            <div style={{marginTop: '4px', display: 'flex', gap: '4px'}}>
                {course.semester?.map((sem: string) => (
                    <span key={sem} className="retro-badge retro-badge-semester">
                        {sem === 'fall' ? 'Høst' : 'Vår'}
                    </span>
                ))}
            </div>
        </div>
    );
};
