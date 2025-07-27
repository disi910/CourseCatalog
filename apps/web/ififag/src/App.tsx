import { useState } from 'react';
import { CourseCatalog } from './pages/CourseCatalog';
import { CourseDetailModal } from './components/CourseDetailModal';
import { CourseMap } from './pages/CourseMap';



function App() {
  const [selectedCourseId, setSelectedCourseId] = useState<string | null>(null);
  const [currentView, setCurrentView] = useState<'home' | 'catalog' | 'map'>('home');

  const handleEmnesokClick = () => {
    setCurrentView('catalog');
  };

  const handleEmnekartClick = () => {
    setCurrentView('map');
    // TODO: Implement course map view
    console.log('Emnekart clicked - not implemented yet');
  };

  const handleBackToHome = () => {
    setCurrentView('home');
    setSelectedCourseId(null);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {currentView === 'home' && (
        <div className="container mx-auto px-4 py-8">
          {/* Centered content container */}
          <div className="flex flex-col items-center justify-center min-h-[80vh] max-w-4xl mx-auto">
            {/* Logo */}
            <div className="mb-8">
              <img
                src="/ifi.png" // You'll need to add this to your public folder
                alt="Institutt for Informatikk Logo"
                className="h-24 w-auto object-contain"
                onError={(e) => {
                  // Fallback if image doesn't exist
                  e.currentTarget.style.display = 'none';
                  e.currentTarget.nextElementSibling!.classList.remove('hidden');
                }}
              />
              {/* Fallback placeholder if image doesn't load */}
              <div className="hidden h-24 w-48 bg-gray-200 rounded-lg flex items-center justify-center">
                <span className="text-gray-500 text-sm">IFI Logo</span>
              </div>
            </div>

            {/* Title */}
            <p className="text-2xl md:text-2xl text-gray-900 text-center mb-12">
              Utforsk emner ved Institutt for Informatikk
            </p>

            {/* Buttons */}
            <div className="flex gap-8 justify-center">
              <button
                onClick={handleEmnesokClick}
                className="px-8 py-4 bg-blue-600 text-gray-900 text-lg font-semibold rounded-lg hover:bg-blue-700 transition-colors shadow-md hover:shadow-lg"
              >
                Emnesøk
              </button>
              <button
                onClick={handleEmnekartClick}
                className="px-8 py-4 bg-green-600 text-gray-900 text-lg font-semibold rounded-lg hover:bg-green-700 transition-colors shadow-md hover:shadow-lg"
              >
                Emnekart
              </button>
            </div>
          </div>
        </div>
      )}

      {currentView === 'catalog' && (
        <div className="min-h-screen flex justify-center bg-gray-50">
          <div className="w-full max-w-7xl px-4 py-8">
            {/* Back button */}
            <button
              onClick={handleBackToHome}
              className="mb-6 flex items-center text-blue-600 hover:text-blue-800 transition-colors"
            >
              <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
              </svg>
              Tilbake til hovedside
            </button>

            <CourseCatalog 
              onCourseSelect={(courseId) => setSelectedCourseId(courseId)} 
            />
          </div>
        </div>
      )}
      {currentView === 'map' && (
        <div className="min-h-screen flex justify-center bg-gray-50">
          <div className="w-full max-w-7xl px-4 py-8">
            {/* Back button */}
            <button
              onClick={handleBackToHome}
              className="mb-6 flex items-center text-blue-600 hover:text-blue-800 transition-colors"
            >
              <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
              </svg>
              Tilbake til hovedside
            </button>

            <CourseMap />
          </div>
        </div>
      )}
      
      <CourseDetailModal
        courseId={selectedCourseId}
        isOpen={!!selectedCourseId}
        onClose={() => setSelectedCourseId(null)}
      />
    </div>
  );
}

export default App;