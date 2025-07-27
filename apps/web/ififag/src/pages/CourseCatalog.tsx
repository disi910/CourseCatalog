import { useState, useEffect, useMemo } from 'react';
import { api } from '../services/api';
import { CourseCard } from '../components/CourseCard';
import { CourseFilters } from '../components/CourseFilters';
import { SearchBar } from '../components/SearchBar';
import { LoadingSpinner } from '../components/LoadingSpinner';
import { ErrorMessage } from '../components/ErrorMessage';

interface CourseCatalogProps {
  onCourseSelect?: (courseId: string) => void;
}

export const CourseCatalog = ({ onCourseSelect }: CourseCatalogProps) => {
  // State management
  const [courses, setCourses] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [filters, setFilters] = useState({});
  const [searchTerm, setSearchTerm] = useState('');

  // Fetch courses when filters change
  useEffect(() => {
    const fetchCourses = async () => {
      try {
        setLoading(true);
        setError(null);
        const data = await api.getCourses(filters);
        setCourses(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Kunne ikke hente emner');
      } finally {
        setLoading(false);
      }
    };

    fetchCourses();
  }, [filters]); // Dependency array - re-run when filters change

  // Client-side search filtering
  const filteredCourses = useMemo(() => {
    if (!searchTerm) return courses;
    
    const searchLower = searchTerm.toLowerCase();
    return courses.filter(course => 
      course.id.toLowerCase().includes(searchLower) ||
      course.title.toLowerCase().includes(searchLower) ||
      course.title_english?.toLowerCase().includes(searchLower) ||
      course.description?.toLowerCase().includes(searchLower)
    );
  }, [courses, searchTerm]); // Recalculate when courses or searchTerm change

  // Handle course click
  const handleCourseClick = (course: any) => {
    if (onCourseSelect) {
      onCourseSelect(course.id);
    }
    console.log('Course clicked:', course);
    // TODO: Navigate to course detail page or show modal
  };

  // Render states
  if (loading) return <LoadingSpinner />;
  if (error) return <ErrorMessage message={error} />;

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Emnekatalog - Institutt for informatikk
          </h1>
          <p className="text-gray-600">
            Bla gjennom og søk i emner ved Institutt for informatikk, UiO
          </p>
        </div>
        
        {/* Search */}
        <SearchBar 
          value={searchTerm} 
          onChange={setSearchTerm}
          placeholder="Søk etter emnekode, tittel eller beskrivelse..."
        />
        
        {/* Filters */}
        <CourseFilters 
          filters={filters} 
          onFilterChange={setFilters} 
        />
        
        {/* Results count */}
        <div className="mb-4 text-gray-600">
          Viser {filteredCourses.length} av {courses.length} emner
        </div>
        
        {/* Course grid */}
        {filteredCourses.length === 0 ? (
          <div className="text-center py-12">
            <p className="text-gray-500 text-lg">
              Ingen emner funnet. Prøv å justere filtrene eller søket.
            </p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredCourses.map((course) => (
              <CourseCard
                key={course.id}
                course={course}
                onClick={() => handleCourseClick(course)}
              />
            ))}
          </div>
        )}
      </div>
    </div>
  );
};