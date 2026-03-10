import { useState, useEffect } from 'react';
import { CourseCard } from '../components/CourseCard';
import { CourseFilters } from '../components/CourseFilters';
import { SearchBar } from '../components/SearchBar';
import { api } from '../services/api';

interface Course {
  id: string;
  title: string;
  title_english: string;
  description: string;
  credits: number;
  level: string;
  semester: string[];
  language: string;
  prerequisites: any[];
  instructor?: string;
  exam_form: string;
  teaching_form: string;
}

interface FilterOptions {
  department?: string;
  level?: string;
  language?: string;
  semester?: string;
}

interface CourseCatalogProps {
  onCourseSelect: (courseId: string) => void;
}

export const CourseCatalog = ({ onCourseSelect }: CourseCatalogProps) => {
  const [courses, setCourses] = useState<Course[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [filters, setFilters] = useState<FilterOptions>({});

  useEffect(() => {
    const fetchCourses = async () => {
      try {
        setLoading(true);
        setError(null);

        const searchFilters = {
          ...filters,
          search: searchQuery || undefined
        };

        const coursesData = await api.getCourses(searchFilters);
        setCourses(coursesData);
      } catch (err) {
        setError('Kunne ikke laste emner. Prøv igjen senere.');
        console.error('Error fetching courses:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchCourses();
  }, [filters, searchQuery]);

  const handleFilterChange = (newFilters: FilterOptions) => {
    setFilters(newFilters);
  };

  const handleSearchChange = (query: string) => {
    setSearchQuery(query);
  };

  return (
    <>
      {/* Header */}
      <div className="text-center mb-4">
        <h1>Emnesøk</h1>
        <p style={{color: '#666', fontSize: '12px'}}>
          Søk og filtrer blant alle emner ved Institutt for Informatikk
        </p>
      </div>

      <SearchBar
        value={searchQuery}
        onChange={handleSearchChange}
        placeholder="Søk etter emner (emnekode, tittel, beskrivelse)..."
      />

      <CourseFilters
        filters={filters}
        onFilterChange={handleFilterChange}
      />

      {/* Results area — always rendered to prevent layout shift */}
      <div style={{minHeight: '200px'}}>
        {/* Error */}
        {error && (
          <div className="retro-error">
            <div className="retro-error-title">!! Feil !!</div>
            <p>{error}</p>
          </div>
        )}

        <div className="retro-results-count">
          Fant <strong>{loading ? '...' : courses.length}</strong> emner
        </div>

        {loading ? (
          <div className="retro-loading">
            <div className="retro-loading-indicator">
              <span className="retro-blink">*** Loading ***</span>
            </div>
            <p className="mt-2">Laster emner...</p>
          </div>
        ) : courses.length > 0 ? (
          <div className="retro-grid">
            {courses.map((course) => (
              <CourseCard
                key={course.id}
                course={course}
                onClick={() => onCourseSelect(course.id)}
              />
            ))}
          </div>
        ) : !error ? (
          <div className="retro-empty">
            <p><strong>Ingen emner funnet</strong></p>
            <p>Prøv å justere søkekriteriene eller filtrene dine.</p>
          </div>
        ) : null}
      </div>
    </>
  );
};
