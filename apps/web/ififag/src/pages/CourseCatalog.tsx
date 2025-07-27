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

  // Fetch courses whenever filters or search query changes
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

  // Handle filter changes
  const handleFilterChange = (newFilters: FilterOptions) => {
    setFilters(newFilters);
  };

  // Handle search
  const handleSearchChange = (query: string) => {
    setSearchQuery(query);
  };

  return (
    <>
      {/* Header */}
      <div className="text-center mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Emnesøk</h1>
        <p className="text-gray-600">
          Søk og filtrer blant alle emner ved Institutt for Informatikk
        </p>
      </div>

      {/* Search Bar */}
      <SearchBar
        value={searchQuery}
        onChange={handleSearchChange}
        placeholder="Søk etter emner (emnekode, tittel, beskrivelse)..."
      />

      {/* Filters */}
      <CourseFilters
        filters={filters}
        onFilterChange={handleFilterChange}
      />

      {/* Results */}
      {loading && (
        <div className="text-center py-12">
          <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
          <p className="mt-2 text-gray-600">Laster emner...</p>
        </div>
      )}

      {error && (
        <div className="bg-red-50 border border-red-200 rounded-md p-4 mb-6">
          <div className="flex">
            <div className="ml-3">
              <h3 className="text-sm font-medium text-red-800">Feil</h3>
              <div className="mt-2 text-sm text-red-700">
                <p>{error}</p>
              </div>
            </div>
          </div>
        </div>
      )}

      {!loading && !error && (
        <>
          {/* Results count */}
          <div className="mb-6">
            <p className="text-gray-600">
              Fant <span className="font-semibold">{courses.length}</span> emner
            </p>
          </div>

          {/* Course grid */}
          {courses.length > 0 ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {courses.map((course) => (
                <CourseCard
                  key={course.id}
                  course={course}
                  onClick={() => onCourseSelect(course.id)}
                />
              ))}
            </div>
          ) : (
            <div className="text-center py-12">
              <div className="text-gray-400 text-6xl mb-4">📚</div>
              <h3 className="text-lg font-medium text-gray-900 mb-2">
                Ingen emner funnet
              </h3>
              <p className="text-gray-500">
                Prøv å justere søkekriteriene eller filtrene dine.
              </p>
            </div>
          )}
        </>
      )}
    </>
  );
};