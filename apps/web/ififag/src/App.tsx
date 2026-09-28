import { useState } from 'react';
import { CourseCatalog } from './pages/CourseCatalog';
import { CourseDetailModal } from './components/CourseDetailModal';
import { CourseMap } from './pages/CourseMap';
import { Taskbar } from './components/Taskbar';

const VIEW_TITLES = {
  home: 'IFI Emnesøk',
  catalog: 'Emnesøk',
  map: 'Emnekart',
} as const;

function App() {
  const [selectedCourseId, setSelectedCourseId] = useState<string | null>(null);
  const [currentView, setCurrentView] = useState<'home' | 'catalog' | 'map'>('home');

  const handleBackToHome = () => {
    setCurrentView('home');
    setSelectedCourseId(null);
  };

  return (
    <div className="retro-page">
      <main className="win-desktop">
        <div className="window app-window">
          <div className="title-bar">
            <div className="title-bar-text">
              <img src={`${import.meta.env.BASE_URL}icons/exe.svg`} alt="" />
              {VIEW_TITLES[currentView]} &mdash; Institutt for Informatikk
            </div>
            <div className="title-bar-controls">
              <span aria-hidden="true">_</span>
              <span aria-hidden="true">□</span>
              <a href="/" title="Lukk (tilbake til didriksi.com)" aria-label="Lukk og gå tilbake til didriksi.com">×</a>
            </div>
          </div>

          <nav className="toolbar" aria-label="Visninger">
            <button className="btn" aria-pressed={currentView === 'home'} onClick={handleBackToHome}>
              <img src={`${import.meta.env.BASE_URL}icons/computer.svg`} alt="" />Hjem
            </button>
            <button className="btn" aria-pressed={currentView === 'catalog'} onClick={() => setCurrentView('catalog')}>
              <img src={`${import.meta.env.BASE_URL}icons/folder.svg`} alt="" />Emnesøk
            </button>
            <button className="btn" aria-pressed={currentView === 'map'} onClick={() => setCurrentView('map')}>
              <img src={`${import.meta.env.BASE_URL}icons/chart.svg`} alt="" />Emnekart
            </button>
            <span className="toolbar-sep" aria-hidden="true"></span>
            <a href="/" className="btn">&laquo; didriksi.com</a>
          </nav>

          <div className="window-body-sunken">
            {currentView === 'home' && (
              <div className="retro-container">
                <div className="retro-center">
                  {/* Logo */}
                  <div className="mb-4">
                    <img
                      src={`${import.meta.env.BASE_URL}ifi.png`}
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
                    <button onClick={() => setCurrentView('catalog')} className="btn-primary">
                      Emnesøk
                    </button>
                    <button onClick={() => setCurrentView('map')} className="btn-secondary">
                      Emnekart
                    </button>
                  </div>

                </div>
              </div>
            )}

            {currentView === 'catalog' && (
              <div className="retro-container-wide">
                <CourseCatalog
                  onCourseSelect={(courseId) => setSelectedCourseId(courseId)}
                />
              </div>
            )}

            {currentView === 'map' && (
              <div className="retro-container-wide">
                <CourseMap />
              </div>
            )}

            <CourseDetailModal
              courseId={selectedCourseId}
              isOpen={!!selectedCourseId}
              onClose={() => setSelectedCourseId(null)}
            />
          </div>

          <div className="status-bar">
            <p className="status-bar-field">Sist oppdatert: Mars 2026</p>
            <p className="status-bar-field grow-0">Institutt for Informatikk, UiO</p>
          </div>
        </div>
      </main>

      <Taskbar />
    </div>
  );
}

export default App;
