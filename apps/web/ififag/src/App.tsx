import { useState } from 'react';
import { CourseCatalog } from './pages/CourseCatalog';
import { CourseDetailModal } from './components/CourseDetailModal';

function App() {
  const [selectedCourseId, setSelectedCourseId] = useState<string | null>(null);

  return (
    <div className="App">
      <CourseCatalog 
        onCourseSelect={(courseId) => setSelectedCourseId(courseId)} 
      />
      
      <CourseDetailModal
        courseId={selectedCourseId}
        isOpen={!!selectedCourseId}
        onClose={() => setSelectedCourseId(null)}
      />
    </div>
  );
}

export default App;