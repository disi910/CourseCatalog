import type { FilterOptions } from '../types';

interface CourseFiltersProps {
  filters: FilterOptions;
  onFilterChange: (filters: FilterOptions) => void;
}

export const CourseFilters = ({ filters, onFilterChange }: CourseFiltersProps) => {
  const handleChange = (filterName: string, value: string) => {
    onFilterChange({
      ...filters,
      [filterName]: value || undefined
    });
  };

  return (
    <div className="retro-filters">
      <div className="retro-filters-title">Filtrer emner</div>

      <div className="retro-grid-4col">
        <div className="retro-filter-group">
          <label>Institutt</label>
          <select
            value={filters.department || ''}
            onChange={(e) => handleChange('department', e.target.value)}
          >
            <option value="">Alle institutter</option>
            <option value="Informatics">Informatikk</option>
            <option value="Mathematics">Matematikk</option>
            <option value="Economics">Økonomi</option>
          </select>
        </div>

        <div className="retro-filter-group">
          <label>Nivå</label>
          <select
            value={filters.level || ''}
            onChange={(e) => handleChange('level', e.target.value)}
          >
            <option value="">Alle nivåer</option>
            <option value="bachelor">Bachelor</option>
            <option value="master">Master</option>
            <option value="phd">PhD</option>
          </select>
        </div>

        <div className="retro-filter-group">
          <label>Språk</label>
          <select
            value={filters.language || ''}
            onChange={(e) => handleChange('language', e.target.value)}
          >
            <option value="">Alle språk</option>
            <option value="Norwegian">Norsk</option>
            <option value="English">Engelsk</option>
          </select>
        </div>

        <div className="retro-filter-group">
          <label>Semester</label>
          <select
            value={filters.semester || ''}
            onChange={(e) => handleChange('semester', e.target.value)}
          >
            <option value="">Alle semestre</option>
            <option value="fall">Høst</option>
            <option value="spring">Vår</option>
          </select>
        </div>
      </div>

      <hr />

      <button
        onClick={() => onFilterChange({})}
        className="btn-back"
        style={{marginTop: '4px'}}
      >
        Nullstill filtre
      </button>
    </div>
  );
};
