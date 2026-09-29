import { useEffect, useRef, useState } from 'react';

// Win98-style taskbar shared with the rest of didriksi.com (links go to the portfolio's pages).
const icon = (name: string, ext = 'svg') => `${import.meta.env.BASE_URL}icons/${name}.${ext}`;

const USAGE_BAR_FOR_CLAUDE = 'https://chromewebstore.google.com/detail/usage-bar-for-claude-limi/imblbfhdbdecholhjbagcjahdkhidneb';

const formatTime = (d: Date) => d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

export const Taskbar = () => {
  const [open, setOpen] = useState(false);
  const [time, setTime] = useState(() => formatTime(new Date()));
  const menuRef = useRef<HTMLElement>(null);
  const btnRef = useRef<HTMLButtonElement>(null);

  useEffect(() => {
    const id = setInterval(() => setTime(formatTime(new Date())), 15000);
    return () => clearInterval(id);
  }, []);

  useEffect(() => {
    if (!open) return;
    menuRef.current?.querySelector('a')?.focus();
    const onClick = (e: MouseEvent) => {
      if (!menuRef.current?.contains(e.target as Node) && !btnRef.current?.contains(e.target as Node)) {
        setOpen(false);
      }
    };
    const onKey = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        setOpen(false);
        btnRef.current?.focus();
      }
    };
    document.addEventListener('click', onClick);
    document.addEventListener('keydown', onKey);
    return () => {
      document.removeEventListener('click', onClick);
      document.removeEventListener('keydown', onKey);
    };
  }, [open]);

  return (
    <>
      {open && (
        <nav className="start-menu" ref={menuRef} aria-label="Start menu">
          <a href="/"><img src={icon('computer')} alt="" />Home</a>
          <a href="/datanorge/"><img src={icon('map')} alt="" />DataNorge</a>
          <a href="/coursecatalog/"><img src={icon('exe')} alt="" />Course Catalog</a>
          <a href="/housingclassifier/"><img src={icon('chart')} alt="" />Housing Classifier</a>
          <a href={USAGE_BAR_FOR_CLAUDE} target="_blank" rel="noopener noreferrer"><img src={icon('usage-bar', 'png')} alt="" />Usage Bar for Claude</a>
          <hr />
          <a href="https://github.com/disi910" target="_blank" rel="noopener"><img src={icon('github')} alt="" />GitHub</a>
        </nav>
      )}
      <footer className="taskbar">
        <button
          ref={btnRef}
          className="btn start-btn"
          aria-expanded={open}
          onClick={() => setOpen((o) => !o)}
        >
          <img src={icon('start')} alt="" />Start
        </button>
        <div className="taskbar-items">
          <a className="btn taskbar-item" href="/"><img src={icon('computer')} alt="" /><span>didriksi.com</span></a>
          <a className="btn taskbar-item current" href="/coursecatalog/"><img src={icon('exe')} alt="" /><span>Course Catalog</span></a>
          <a className="btn taskbar-item" href="/housingclassifier/"><img src={icon('chart')} alt="" /><span>Housing Classifier</span></a>
        </div>
        <div className="tray">
          <span className="tray-copy">&copy; 2026 Didrik S.</span>
          <time>{time}</time>
        </div>
      </footer>
    </>
  );
};
