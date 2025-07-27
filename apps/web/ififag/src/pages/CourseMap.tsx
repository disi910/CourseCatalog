import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import { DependencyVisualization } from '../components/dependency/DependencyVisualization';

interface Course {
  id: string;
  title: string;
  title_english: string;
  prerequisites: any[];
}

export const CourseMap: React.FC = () => {
  const [courses, setCourses] = useState<Course[]>([]);
  const [selectedCourseId, setSelectedCourseId] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  // Fetch all courses on component mount
  useEffect(() => {
    const fetchCourses = async () => {
      try {
        const coursesData = await api.getCourses();
        // Filter courses that have prerequisites (more interesting to visualize)
        const coursesWithPrereqs = coursesData.filter(
          (course: Course) => course.prerequisites && course.prerequisites.length > 0
        );
        setCourses(coursesWithPrereqs);
        
        // Auto-select the first course with prerequisites
        if (coursesWithPrereqs.length > 0) {
          setSelectedCourseId(coursesWithPrereqs[0].id);
        }
      } catch (error) {
        console.error('Error fetching courses:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchCourses();
  }, []);

  if (loading) {
    return (
      <div className="text-center py-12">
        <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
        <p className="mt-2 text-gray-600">Laster emnekart...</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="text-center">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Emnekart</h1>
        <p className="text-gray-600">
          Visualiser avhengigheter mellom emner ved Institutt for Informatikk
        </p>
      </div>

      {/* Course Selector */}
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-lg font-semibold mb-4">Velg emne å utforske</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
          {courses.map((course) => (
            <button
              key={course.id}
              onClick={() => setSelectedCourseId(course.id)}
              className={`p-3 text-left rounded-lg border-2 transition-colors ${
                selectedCourseId === course.id
                  ? 'border-blue-500 bg-blue-50'
                  : 'border-gray-200 hover:border-gray-300'
              }`}
            >
              <div className="font-semibold text-gray-900">{course.id}</div>
              <div className="text-sm text-gray-600 line-clamp-2">
                {course.title}
              </div>
              <div className="text-xs text-gray-500 mt-1">
                {course.prerequisites.length} forkunnskaper
              </div>
            </button>
          ))}
        </div>
      </div>

      {/* Visualization */}
      {selectedCourseId && (
        <div className="bg-white rounded-lg shadow">
          <div className="p-4 border-b">
            <h3 className="text-lg font-semibold">
              Avhengigheter for {selectedCourseId}
            </h3>
          </div>
          <div style={{ height: '600px' }}>
            <DependencyVisualization 
              courseId={selectedCourseId}
              onCourseClick={(courseId) => setSelectedCourseId(courseId)}
            />
          </div>
        </div>
      )}

      {courses.length === 0 && (
        <div className="text-center py-12">
          <div className="text-gray-400 text-6xl mb-4">🗺️</div>
          <h3 className="text-lg font-medium text-gray-900 mb-2">
            Ingen emner med forkunnskaper funnet
          </h3>
          <p className="text-gray-500">
            Emnekart viser emner som har andre emner som forkunnskaper.
          </p>
        </div>
      )}
    </div>
  );
};