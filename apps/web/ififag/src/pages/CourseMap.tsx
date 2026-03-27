import { useState, useEffect, useMemo } from 'react';
import { api } from '../services/api';
import { DependencyVisualization } from '../components/dependency/DependencyVisualization';
import { SearchBar } from '../components/SearchBar';
import type { Course } from '../types';

export const CourseMap = () => {
  const [courses, setCourses] = useState<Course[]>([]);
  const [selectedCourseId, setSelectedCourseId] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');

  useEffect(() => {
    const fetchCourses = async () => {
      try {
        const coursesData = await api.getCourses();
        const coursesWithPrereqs = coursesData.filter(
          (course) => course.prerequisites && course.prerequisites.length > 0
        );
        setCourses(coursesWithPrereqs);

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

  const filteredCourses = useMemo(() => {
    if (!searchQuery.trim()) return courses;
    const q = searchQuery.toLowerCase();
    return courses.filter(
      (c) => c.id.toLowerCase().includes(q) || c.title.toLowerCase().includes(q)
    );
  }, [courses, searchQuery]);

  if (loading) {
    return (
      <div className="retro-loading">
        <div className="retro-loading-indicator">
          <span className="retro-blink">*** Loading ***</span>
        </div>
        <p className="mt-2">Laster emnekart...</p>
      </div>
    );
  }

  return (
    <div>
      {/* Header */}
      <div className="text-center mb-4">
        <h1>Emnekart</h1>
        <p style={{color: '#666', fontSize: '12px'}}>
          Visualiser avhengigheter mellom emner ved Institutt for Informatikk
        </p>
      </div>

      {/* Course Selector */}
      <div className="retro-panel">
        <div className="retro-panel-header">Velg emne å utforske</div>
        <div style={{ padding: '8px 8px 0' }}>
          <SearchBar
            value={searchQuery}
            onChange={setSearchQuery}
            placeholder="Søk etter emne..."
          />
        </div>
        <div style={{ maxHeight: '250px', overflowY: 'auto', border: '2px inset #c0c0c0', padding: '4px' }}>
          <div className="retro-grid-3col">
            {filteredCourses.map((course) => (
              <button
                key={course.id}
                onClick={() => setSelectedCourseId(course.id)}
                className={`retro-course-selector-btn ${
                  selectedCourseId === course.id ? 'selected' : ''
                }`}
              >
                <div className="retro-course-selector-code">{course.id}</div>
                <div className="retro-course-selector-title">{course.title}</div>
                <div className="retro-course-selector-prereqs">
                  {course.prerequisites.length} forkunnskaper
                </div>
              </button>
            ))}
          </div>
        </div>
      </div>

      {selectedCourseId && (
        <div className="retro-panel">
          <div className="retro-panel-header">
            Avhengigheter for {selectedCourseId}
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
        <div className="retro-empty">
          <p><strong>Ingen emner med forkunnskaper funnet</strong></p>
          <p>Emnekart viser emner som har andre emner som forkunnskaper.</p>
        </div>
      )}
    </div>
  );
};
