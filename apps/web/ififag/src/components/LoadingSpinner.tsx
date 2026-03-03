export const LoadingSpinner = () => {
  return (
    <div className="retro-loading" style={{minHeight: '200px', display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
      <div className="retro-loading-indicator">
        <span className="retro-blink">*** Loading ***</span>
      </div>
    </div>
  );
};
