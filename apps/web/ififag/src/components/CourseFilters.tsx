interface FilterOptions {
  department?: string;
  level?: string;
  language?: string;
  semester?: string;
}

interface CourseFiltersProps {
  filters: FilterOptions;
  onFilterChange: (filters: FilterOptions) => void;
}

export const CourseFilters = ({ filters, onFilterChange }: CourseFiltersProps) => {
  // Handle individual filter changes
  const handleChange = (filterName: string, value: string) => {
    onFilterChange({
      ...filters, // Keep existing filters
      [filterName]: value || undefined // Update specific filter
    });
  };

  return (
    <div className="bg-white rounded-lg shadow p-6 mb-6">
      <h2 className="text-lg font-semibold mb-4">Filtrer emner</h2>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Department filter */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Institutt
          </label>
          <select
            value={filters.department || ''}
            onChange={(e) => handleChange('department', e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="">Alle institutter</option>
            <option value="Informatics">Informatikk</option>
            <option value="Mathematics">Matematikk</option>
          </select>
        </div>
        
        {/* Level filter */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Nivå
          </label>
          <select
            value={filters.level || ''}
            onChange={(e) => handleChange('level', e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="">Alle nivåer</option>
            <option value="bachelor">Bachelor</option>
            <option value="master">Master</option>
            <option value="phd">PhD</option>
          </select>
        </div>
        
        {/* Language filter */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Språk
          </label>
          <select
            value={filters.language || ''}
            onChange={(e) => handleChange('language', e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="">Alle språk</option>
            <option value="Norwegian">Norsk</option>
            <option value="English">Engelsk</option>
          </select>
        </div>
        
        {/* Semester filter */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Semester
          </label>
          <select
            value={filters.semester || ''}
            onChange={(e) => handleChange('semester', e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="">Alle semestre</option>
            <option value="fall">Høst</option>
            <option value="spring">Vår</option>
          </select>
        </div>
      </div>
      
      {/* Reset button */}
      <button
        onClick={() => onFilterChange({})}
        className="mt-4 px-4 py-2 bg-gray-200 text-gray-700 rounded-md hover:bg-gray-300 transition-colors"
      >
        Nullstill filtre
      </button>
    </div>
  );
};