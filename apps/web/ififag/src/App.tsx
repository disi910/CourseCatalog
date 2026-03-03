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
  };

  const handleBackToHome = () => {
    setCurrentView('home');
    setSelectedCourseId(null);
  };

  return (
    <div className="retro-page">
      {/* Retro marquee banner */}
      <div className="retro-marquee">
        <marquee scrollamount={3}>
          *** Velkommen til Institutt for Informatikk - Universitetet i Oslo *** Oppdatert med de nyeste emnene for 2025/2026 ***
        </marquee>
      </div>

      {currentView === 'home' && (
        <div className="retro-container">
          <div className="retro-center">
            {/* Logo */}
            <div className="mb-4">
              <img
                src="/ifi.png"
                alt="Institutt for Informatikk Logo"
                className="retro-home-logo"
                onError={(e) => {
                  e.currentTarget.style.display = 'none';
                  e.currentTarget.nextElementSibling!.classList.remove('hidden');
                }}
              />
              <div className="hidden" style={{height: '80px', width: '160px', backgroundColor: '#e8e8e8', border: '2px inset #c0c0c0', alignItems: 'center', justifyContent: 'center', color: '#666', fontSize: '11px'}}>
                <span>IFI Logo</span>
              </div>
            </div>

            {/* Title */}
            <p className="retro-home-subtitle">
              Utforsk emner ved Institutt for Informatikk
            </p>

            {/* Buttons */}
            <div className="retro-home-buttons">
              <button onClick={handleEmnesokClick} className="btn-primary">
                Emnesøk
              </button>
              <button onClick={handleEmnekartClick} className="btn-secondary">
                Emnekart
              </button>
            </div>

            {/* Visitor counter */}
            <div className="retro-counter">
              Du er besøkende nr.{' '}
              <span style={{fontFamily: 'Courier New, monospace', fontWeight: 'bold'}}>
                004,831
              </span>{' '}
              siden 01.01.2002
            </div>
          </div>
        </div>
      )}

      {currentView === 'catalog' && (
        <div className="retro-container-wide">
          <button onClick={handleBackToHome} className="btn-back">
            &laquo; Tilbake til hovedside
          </button>
          <CourseCatalog
            onCourseSelect={(courseId) => setSelectedCourseId(courseId)}
          />
        </div>
      )}

      {currentView === 'map' && (
        <div className="retro-container-wide">
          <button onClick={handleBackToHome} className="btn-back">
            &laquo; Tilbake til hovedside
          </button>
          <CourseMap />
        </div>
      )}

      <CourseDetailModal
        courseId={selectedCourseId}
        isOpen={!!selectedCourseId}
        onClose={() => setSelectedCourseId(null)}
      />

      {/* Retro status bar */}
      <div className="retro-status-bar">
        Sist oppdatert: Mars 2026 | Institutt for Informatikk, UiO | Best viewed in Internet Explorer 6.0 at 1024x768
      </div>
    </div>
  );
}

export default App;
