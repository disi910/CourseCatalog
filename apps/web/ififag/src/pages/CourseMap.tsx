import { useState, useEffect } from 'react';
import { api } from '../services/api';
import { DependencyVisualization } from '../components/dependency/DependencyVisualization';
import type { Course } from '../types';

export const CourseMap = () => {
  const [courses, setCourses] = useState<Course[]>([]);
  const [selectedCourseId, setSelectedCourseId] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [prereqCounts, setPrereqCounts] = useState<Record<string, number>>({});

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [coursesData, counts] = await Promise.all([
          api.getCourses(),
          api.getPrerequisiteCounts(),
        ]);

        const coursesWithPrereqs = coursesData.filter(
          (course) => course.prerequisites && course.prerequisites.length > 0
        );
        setCourses(coursesWithPrereqs);
        setPrereqCounts(counts);

        if (coursesWithPrereqs.length > 0) {
          setSelectedCourseId(coursesWithPrereqs[0].id);
        }
      } catch (error) {
        console.error('Error fetching courses:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const filteredCourses = courses.filter((course) => {
    const query = searchQuery.toLowerCase();
    return (
      course.id.toLowerCase().includes(query) ||
      course.title.toLowerCase().includes(query)
    );
  });

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

      {/* Search + Course Selector */}
      <div className="retro-panel" style={{marginBottom: '12px'}}>
        <div className="retro-panel-header">Velg emne å utforske</div>

        {/* Search bar */}
        <div style={{padding: '8px 10px 4px 10px'}}>
          <input
            type="text"
            placeholder="Søk etter emne (kode eller navn)..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            style={{width: '100%', marginBottom: '6px'}}
          />
        </div>

        {/* Scrollable course grid */}
        <div style={{maxHeight: '200px', overflowY: 'auto', padding: '0 10px 10px 10px'}}>
          <div className="retro-grid-4col">
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
                  {prereqCounts[course.id] ?? course.prerequisites.length} totale forkunnskaper
                </div>
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Dependency Visualization */}
      {selectedCourseId && (
        <div className="retro-panel">
          <div className="retro-panel-header">
            Avhengigheter for {selectedCourseId}
          </div>
          <div style={{ height: '500px' }}>
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
