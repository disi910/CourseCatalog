import { useEffect, useState } from 'react';
import { api } from '../services/api';

interface CourseDetailModalProps {
  courseId: string | null;
  isOpen: boolean;
  onClose: () => void;
}

export const CourseDetailModal = ({ courseId, isOpen, onClose }: CourseDetailModalProps) => {
  const [course, setCourse] = useState<any>(null);
  const [dependencies, setDependencies] = useState<any>(null);
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
      <div 
        className="fixed inset-0 bg-black bg-opacity-50 z-40"
        onClick={onClose}
      />
      
      {/* Modal */}
      <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
        <div className="bg-white rounded-lg max-w-4xl w-full max-h-[90vh] overflow-auto">
          {/* Header */}
          <div className="sticky top-0 bg-white border-b px-6 py-4 flex justify-between items-center">
            <h2 className="text-2xl font-bold">
              {course?.id} - {course?.title}
            </h2>
            <button
              onClick={onClose}
              className="text-gray-400 hover:text-gray-600 text-2xl"
            >
              ×
            </button>
          </div>
          
          {/* Content */}
          <div className="p-6">
            {loading ? (
              <div className="text-center py-8">Laster...</div>
            ) : (
              <>
                {/* Course details */}
                <div className="space-y-4">
                  <div>
                    <h3 className="font-semibold mb-2">Beskrivelse</h3>
                    <p className="text-gray-700 whitespace-pre-line">
                      {course?.description}
                    </p>
                  </div>
                  
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <h4 className="font-semibold">Studiepoeng</h4>
                      <p>{course?.credits}</p>
                    </div>
                    <div>
                      <h4 className="font-semibold">Undervisningsspråk</h4>
                      <p>{course?.language}</p>
                    </div>
                    <div>
                      <h4 className="font-semibold">Nivå</h4>
                      <p className="capitalize">{course?.level}</p>
                    </div>
                    <div>
                      <h4 className="font-semibold">Semester</h4>
                      <p>{course?.semester?.map((s: string) => 
                        s === 'fall' ? 'Høst' : 'Vår'
                      ).join(', ')}</p>
                    </div>
                  </div>
                  
                  {course?.exam_form && (
                    <div>
                      <h4 className="font-semibold">Eksamen</h4>
                      <p>{course.exam_form}</p>
                    </div>
                  )}
                  
                  {course?.teaching_form && (
                    <div>
                      <h4 className="font-semibold">Undervisningsform</h4>
                      <p>{course.teaching_form}</p>
                    </div>
                  )}
                  
                  {/* Prerequisites visualization */}
                  {dependencies?.nodes?.length > 1 && (
                    <div>
                      <h4 className="font-semibold mb-2">Emneavhengigheter</h4>
                      <div className="bg-gray-50 p-4 rounded-lg">
                        <p className="text-sm text-gray-600 mb-2">
                          Dette emnet krever:
                        </p>
                        {dependencies.nodes
                          .filter((n: any) => n.id !== courseId)
                          .map((node: any) => (
                            <div key={node.id} className="ml-4">
                              → {node.id}: {node.label}
                            </div>
                          ))}
                      </div>
                    </div>
                  )}
                </div>
              </>
            )}
          </div>
        </div>
      </div>
    </>
  );
};