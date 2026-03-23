import { useEffect, useState } from 'react';
import { api } from '../services/api';
import type { Course, DependencyGraph, DependencyNode } from '../types';

interface CourseDetailModalProps {
  courseId: string | null;
  isOpen: boolean;
  onClose: () => void;
}

export const CourseDetailModal = ({ courseId, isOpen, onClose }: CourseDetailModalProps) => {
  const [course, setCourse] = useState<Course | null>(null);
  const [dependencies, setDependencies] = useState<DependencyGraph | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!courseId || !isOpen) return;

    const fetchCourseDetails = async () => {
      try {
        setLoading(true);
        const [courseData, depsData] = await Promise.all([
          api.getCourse(courseId),
          api.getCourseDependencies(courseId)
        ]);
        setCourse(courseData);
        setDependencies(depsData);
      } catch (error) {
        console.error('Error fetching course details:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchCourseDetails();
  }, [courseId, isOpen]);

  if (!isOpen) return null;

  return (
    <>
      {/* Backdrop */}
      <div className="retro-modal-backdrop" onClick={onClose} />

      {/* Modal */}
      <div className="retro-modal-container">
        <div className="retro-modal">
          {/* Windows-style title bar */}
          <div className="retro-modal-titlebar">
            <span>{course?.id} - {course?.title}</span>
            <button onClick={onClose} className="retro-modal-close">X</button>
          </div>

          {/* Content */}
          <div className="retro-modal-body" style={{minHeight: '300px'}}>
            {loading ? (
              <div className="retro-loading" style={{minHeight: '280px', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center'}}>
                <span className="retro-blink">Laster...</span>
              </div>
            ) : (
              <>
                <h3>Beskrivelse</h3>
                <p className="whitespace-pre-line" style={{fontSize: '12px'}}>
                  {course?.description}
                </p>

                <hr />

                <div className="retro-grid-2col">
                  <div>
                    <h4>Studiepoeng</h4>
                    <p>{course?.credits}</p>
                  </div>
                  <div>
                    <h4>Undervisningsspråk</h4>
                    <p>{course?.language}</p>
                  </div>
                  <div>
                    <h4>Nivå</h4>
                    <p className="capitalize">{course?.level}</p>
                  </div>
                  <div>
                    <h4>Semester</h4>
                    <p>{course?.semester?.map((s: string) =>
                      s === 'fall' ? 'Høst' : 'Vår'
                    ).join(', ')}</p>
                  </div>
                </div>

                {course?.exam_form && (
                  <>
                    <hr />
                    <h4>Eksamen</h4>
                    <p>{course.exam_form}</p>
                  </>
                )}

                {course?.teaching_form && (
                  <>
                    <h4>Undervisningsform</h4>
                    <p>{course.teaching_form}</p>
                  </>
                )}

                {dependencies?.nodes && dependencies.nodes.length > 1 && (
                  <>
                    <hr />
                    <h4>Emneavhengigheter</h4>
                    <div className="retro-panel-sunken">
                      <p style={{fontSize: '11px', color: '#666'}}>
                        Dette emnet krever:
                      </p>
                      {dependencies.nodes
                        .filter((n: DependencyNode) => n.id !== courseId)
                        .map((node: DependencyNode) => (
                          <div key={node.id} style={{marginLeft: '12px', fontSize: '12px', fontFamily: 'Courier New, monospace'}}>
                            &rarr; {node.id}: {node.label}
                          </div>
                        ))}
                    </div>
                  </>
                )}
              </>
            )}
          </div>
        </div>
      </div>
    </>
  );
};
