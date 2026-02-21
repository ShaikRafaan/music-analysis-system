import { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import '../App.css';
import { api } from '../utils/api';

// ── Animated waveform bars (pure CSS) ───────────────────────────────────────
function Waveform({ count = 28 }) {
  return (
    <div style={{ display: 'flex', alignItems: 'center', gap: 3, height: 48 }}>
      {Array.from({ length: count }).map((_, i) => (
        <div
          key={i}
          style={{
            width: 3,
            borderRadius: 2,
            background: 'var(--green)',
            opacity: 0.35 + Math.random() * 0.45,
            animation: `wave ${0.8 + (i % 5) * 0.18}s ease-in-out ${(i % 7) * 0.09}s infinite alternate`,
            height: `${20 + Math.round(Math.sin(i * 0.7) * 16 + Math.cos(i * 0.4) * 12)}px`,
          }}
        />
      ))}
    </div>
  );
}

// ── Floating music notes ─────────────────────────────────────────────────────
function FloatingNotes() {
  const notes = ['♩', '♪', '♫', '♬', '𝄞'];
  return (
    <div style={{ position: 'absolute', inset: 0, pointerEvents: 'none', overflow: 'hidden' }}>
      {Array.from({ length: 12 }).map((_, i) => (
        <span
          key={i}
          style={{
            position: 'absolute',
            left: `${8 + (i * 7.5) % 88}%`,
            top: `${10 + (i * 13) % 75}%`,
            fontSize: `${0.7 + (i % 4) * 0.25}rem`,
            color: 'var(--green)',
            opacity: 0.04 + (i % 3) * 0.03,
            animation: `floatNote ${6 + (i % 5) * 2}s ease-in-out ${i * 0.6}s infinite alternate`,
            fontFamily: 'serif',
          }}
        >
          {notes[i % notes.length]}
        </span>
      ))}
    </div>
  );
}

// ── Avatar ───────────────────────────────────────────────────────────────────
function Avatar({ profile }) {
  const img = profile?.images?.[0]?.url;
  const initials = profile?.name
    ? profile.name.split(' ').map(w => w[0]).join('').slice(0, 2).toUpperCase()
    : '?';

  return (
    <div style={{
      width: 56, height: 56, borderRadius: '50%',
      border: '2px solid var(--green)',
      overflow: 'hidden', flexShrink: 0,
      boxShadow: '0 0 0 4px rgba(29,185,84,0.12)',
    }}>
      {img ? (
        <img src={img} alt={profile.name} style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
      ) : (
        <div style={{
          width: '100%', height: '100%',
          background: '#0f1f14',
          display: 'flex', alignItems: 'center', justifyContent: 'center',
          fontFamily: 'var(--font-display)', fontSize: '1.1rem', color: 'var(--green)',
        }}>
          {initials}
        </div>
      )}
    </div>
  );
}

// ── NavLink ──────────────────────────────────────────────────────────────────
function NavLink({ to, label, icon, navigate }) {
  return (
    <button
      onClick={() => navigate(to)}
      style={{
        background: 'none', border: '1px solid var(--border)',
        color: 'var(--muted)', padding: '0.55rem 1.1rem',
        fontFamily: 'var(--font-mono)', fontSize: '0.68rem',
        letterSpacing: '0.1em', textTransform: 'uppercase',
        cursor: 'pointer', borderRadius: 4,
        display: 'flex', alignItems: 'center', gap: '0.5rem',
        transition: 'all 0.18s',
      }}
      onMouseEnter={e => {
        e.currentTarget.style.borderColor = 'var(--green)';
        e.currentTarget.style.color = 'var(--green)';
        e.currentTarget.style.background = 'rgba(29,185,84,0.06)';
      }}
      onMouseLeave={e => {
        e.currentTarget.style.borderColor = 'var(--border)';
        e.currentTarget.style.color = 'var(--muted)';
        e.currentTarget.style.background = 'none';
      }}
    >
      <span>{icon}</span> {label}
    </button>
  );
}

// ── Main ─────────────────────────────────────────────────────────────────────
export const Landing = () => {
  const [authStatus, setAuthStatus]     = useState(false);
  const [authLoading, setAuthLoading]   = useState(true);
  const [loadingLogin, setLoadingLogin] = useState(false);
  const [userProfile, setUserProfile]   = useState(null);
  const navigate = useNavigate();

  // Check auth on mount
  useEffect(() => {
    (async () => {
      try {
        const res = await api.get('/auth/status');
        setAuthStatus(!!res.authenticated);
      } catch {
        setAuthStatus(false);
      } finally {
        setAuthLoading(false);
      }
    })();
  }, []);

  // Fetch profile once authed
  useEffect(() => {
    if (!authStatus) return;
    (async () => {
      try {
        const res = await api.get('/spotify/profile');
        if (res) setUserProfile(res);
      } catch {
        /* silent – profile is decorative here */
      }
    })();
  }, [authStatus]);

  const handleLogin = () => {
    setLoadingLogin(true);
    window.location.href = `${import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000'}/auth/login`;
  };

  return (
    <>
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=Inconsolata:wght@300;400;500&display=swap');

        :root {
          --green:   #1DB954;
          --green-dim: rgba(29,185,84,0.15);
          --bg:      #060609;
          --surface: #0d0d14;
          --border:  #181824;
          --text:    #ddd8cc;
          --muted:   #444458;
          --font-display: 'Syne', sans-serif;
          --font-mono:    'Inconsolata', monospace;
        }

        body { background: var(--bg); }

        @keyframes wave {
          from { transform: scaleY(0.5); }
          to   { transform: scaleY(1.4); }
        }
        @keyframes floatNote {
          from { transform: translateY(0px) rotate(-5deg); }
          to   { transform: translateY(-18px) rotate(8deg); }
        }
        @keyframes fadeUp {
          from { opacity: 0; transform: translateY(18px); }
          to   { opacity: 1; transform: translateY(0); }
        }
        @keyframes scanline {
          from { transform: translateY(-100%); }
          to   { transform: translateY(100vh); }
        }
        @keyframes pulse-ring {
          0%   { box-shadow: 0 0 0 0 rgba(29,185,84,0.3); }
          70%  { box-shadow: 0 0 0 14px rgba(29,185,84,0); }
          100% { box-shadow: 0 0 0 0 rgba(29,185,84,0); }
        }

        .fade-1 { animation: fadeUp 0.55s ease both 0.05s; }
        .fade-2 { animation: fadeUp 0.55s ease both 0.18s; }
        .fade-3 { animation: fadeUp 0.55s ease both 0.3s; }
        .fade-4 { animation: fadeUp 0.55s ease both 0.42s; }

        .login-btn {
          display: inline-flex; align-items: center; gap: 0.65rem;
          background: var(--green); color: #000;
          border: none; padding: 0.85rem 2rem;
          font-family: var(--font-mono); font-size: 0.78rem;
          font-weight: 500; letter-spacing: 0.12em; text-transform: uppercase;
          cursor: pointer; border-radius: 4px;
          transition: all 0.2s; animation: pulse-ring 2.5s infinite;
        }
        .login-btn:hover:not(:disabled) {
          background: #23d45e; transform: translateY(-2px);
          box-shadow: 0 8px 32px rgba(29,185,84,0.35);
        }
        .login-btn:disabled { opacity: 0.6; cursor: not-allowed; animation: none; }

        .feature-card {
          background: var(--surface); border: 1px solid var(--border);
          border-radius: 8px; padding: 1.25rem 1.4rem;
          transition: border-color 0.2s, transform 0.2s;
        }
        .feature-card:hover {
          border-color: rgba(29,185,84,0.3);
          transform: translateY(-2px);
        }

        .tag {
          display: inline-block;
          background: var(--green-dim); color: var(--green);
          border: 1px solid rgba(29,185,84,0.25);
          padding: 0.15rem 0.55rem; border-radius: 100px;
          font-size: 0.6rem; letter-spacing: 0.12em; text-transform: uppercase;
        }
      `}</style>

      <div style={{
        height: '100vh', background: 'var(--bg)',
        color: 'var(--text)', fontFamily: 'var(--font-mono)',
        position: 'relative', overflow: 'hidden',
        display: 'flex', flexDirection: 'column',
      }}>

        {/* Background grid */}
        <div style={{
          position: 'fixed', inset: 0, pointerEvents: 'none', zIndex: 0,
          backgroundImage: `
            linear-gradient(rgba(29,185,84,0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(29,185,84,0.03) 1px, transparent 1px)
          `,
          backgroundSize: '48px 48px',
        }} />

        {/* Scanline sweep */}
        <div style={{
          position: 'fixed', left: 0, right: 0, height: 2, zIndex: 1, pointerEvents: 'none',
          background: 'linear-gradient(transparent, rgba(29,185,84,0.07), transparent)',
          animation: 'scanline 8s linear infinite',
        }} />

        <FloatingNotes />

        {/* ── Nav ── */}
        <nav style={{
          position: 'relative', zIndex: 10,
          borderBottom: '1px solid var(--border)',
          padding: '1rem 2.5rem',
          display: 'flex', alignItems: 'center', justifyContent: 'space-between',
          flexShrink: 0,
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
            <span style={{ color: 'var(--green)', fontSize: '1.3rem' }}>◈</span>
            <span style={{ fontFamily: 'var(--font-display)', fontWeight: 800, fontSize: '1rem', letterSpacing: '-0.01em' }}>
              Soundscape
            </span>
          </div>

          {authStatus && (
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <NavLink to="/listening-history" label="History" icon="◷" navigate={navigate} />
            </div>
          )}
        </nav>

        {/* ── Hero ── */}
        <main style={{
          position: 'relative', zIndex: 5,
          flex: 1,
          padding: '0 4rem',
          display: 'grid',
          gridTemplateColumns: '1fr 1fr',
          gap: '0',
        }}>

          {/* LEFT — Headline + CTA */}
          <div style={{
            display: 'flex', flexDirection: 'column', justifyContent: 'center',
            gap: '1.75rem', padding: '4rem 4rem 4rem 0',
            borderRight: '1px solid var(--border)',
          }}>
            <div className="fade-1">
              <span className="tag">Your Spotify · Reimagined</span>
            </div>

            <h1 className="fade-2" style={{
              fontFamily: 'var(--font-display)', fontSize: 'clamp(2.8rem, 4.5vw, 5rem)',
              fontWeight: 800, lineHeight: 1.0, letterSpacing: '-0.03em',
              color: '#f0ece0',
            }}>
              Every track.<br />
              <span style={{ color: 'var(--green)' }}>Every moment.</span><br />
              Remembered.
            </h1>

            <p className="fade-3" style={{
              fontSize: '0.9rem', color: 'var(--muted)', lineHeight: 1.8, maxWidth: 420,
            }}>
              Connect your Spotify account to explore your listening history, uncover patterns in your taste, and rediscover the music that defined your days.
            </p>

            {/* CTA area */}
            <div className="fade-4" style={{ display: 'flex', alignItems: 'center', gap: '1.25rem', flexWrap: 'wrap' }}>
              {authLoading ? (
                <div style={{ fontSize: '0.7rem', color: 'var(--muted)', letterSpacing: '0.1em' }}>
                  Checking session…
                </div>
              ) : authStatus ? (
                /* ── Logged in ── */
                <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', flexWrap: 'wrap' }}>
                  {userProfile && <Avatar profile={userProfile} />}
                  <div>
                    <div style={{ fontSize: '0.65rem', color: 'var(--muted)', letterSpacing: '0.14em', textTransform: 'uppercase', marginBottom: 4 }}>
                      Logged in as
                    </div>
                    <div style={{ fontFamily: 'var(--font-display)', fontSize: '1.1rem', fontWeight: 700, color: 'var(--text)' }}>
                      {userProfile?.name || 'Spotify User'}
                    </div>
                  </div>
                  <button
                    onClick={() => navigate('/listening-history')}
                    className="login-btn"
                    style={{ marginLeft: '0.5rem' }}
                  >
                    <span>◷</span> View History
                  </button>
                </div>
              ) : (
                /* ── Logged out ── */
                <>
                  <button onClick={handleLogin} disabled={loadingLogin} className="login-btn">
                    {loadingLogin ? (
                      <>
                        <span style={{ display: 'inline-block', animation: 'wave 0.6s ease-in-out infinite alternate' }}>♫</span>
                        Redirecting…
                      </>
                    ) : (
                      <>
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                          <path d="M12 0C5.4 0 0 5.4 0 12s5.4 12 12 12 12-5.4 12-12S18.66 0 12 0zm5.521 17.34c-.24.359-.66.48-1.021.24-2.82-1.74-6.36-2.101-10.561-1.141-.418.122-.779-.179-.899-.539-.12-.421.18-.78.54-.9 4.56-1.021 8.52-.6 11.64 1.32.42.18.479.659.301 1.02zm1.44-3.3c-.301.42-.841.6-1.262.3-3.239-1.98-8.159-2.58-11.939-1.38-.479.12-1.02-.12-1.14-.6-.12-.48.12-1.021.6-1.141C9.6 9.9 15 10.561 18.72 12.84c.361.181.54.78.241 1.2zm.12-3.36C15.24 8.4 8.82 8.16 5.16 9.301c-.6.179-1.2-.181-1.38-.721-.18-.601.18-1.2.72-1.381 4.26-1.26 11.28-1.02 15.721 1.621.539.3.719 1.02.419 1.56-.299.421-1.02.599-1.559.3z"/>
                        </svg>
                        Login with Spotify
                      </>
                    )}
                  </button>
                  <span style={{ fontSize: '0.65rem', color: '#222230' }}>Free · No data stored</span>
                </>
              )}
            </div>
          </div>

          {/* RIGHT — Waveform + Feature cards */}
          <div style={{
            display: 'flex', flexDirection: 'column', justifyContent: 'center',
            gap: '2.5rem', padding: '4rem 0 4rem 4rem',
          }}>

            {/* Big waveform visual */}
            <div className="fade-2" style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
              <div style={{ fontSize: '0.6rem', letterSpacing: '0.18em', textTransform: 'uppercase', color: 'var(--muted)' }}>
                Now Listening
              </div>
              <Waveform count={48} />
              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.6rem', color: '#1e1e2c', letterSpacing: '0.08em' }}>
                <span>0:00</span><span>3:42</span>
              </div>
            </div>

            {/* Feature cards */}
            {!authLoading && (
              <div className="fade-4" style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.75rem' }}>
                {[
                  { icon: '◷', title: 'Listening Timeline', desc: 'Every track you played, with precise timestamps.' },
                  { icon: '◈', title: 'Taste Breakdown', desc: 'Patterns by release type and artist frequency.' },
                  { icon: '♫', title: 'Weekly Rhythm', desc: 'Which days you listen the most, visualised.' },
                  { icon: '↗', title: 'Top Artists', desc: 'Your most-reached-for artists at a glance.' },
                ].map((f) => (
                  <div key={f.title} className="feature-card">
                    <div style={{ fontSize: '1rem', color: 'var(--green)', marginBottom: '0.5rem' }}>{f.icon}</div>
                    <div style={{ fontFamily: 'var(--font-display)', fontWeight: 700, fontSize: '0.82rem', color: 'var(--text)', marginBottom: '0.3rem' }}>
                      {f.title}
                    </div>
                    <div style={{ fontSize: '0.67rem', color: 'var(--muted)', lineHeight: 1.6 }}>
                      {f.desc}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </main>

        {/* ── Footer ── */}
        <footer style={{
          position: 'relative', zIndex: 5,
          borderTop: '1px solid var(--border)',
          padding: '1rem 2.5rem',
          display: 'flex', justifyContent: 'space-between', alignItems: 'center',
          fontSize: '0.6rem', color: '#1e1e2c', letterSpacing: '0.1em',
          flexShrink: 0,
        }}>
          <span>◈ SOUNDSCAPE</span>
          <span>NOT AFFILIATED WITH SPOTIFY AB</span>
        </footer>
      </div>
    </>
  );
};