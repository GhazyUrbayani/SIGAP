import { NavLink, useNavigate } from 'react-router-dom';
import { useAuthStore } from '../../store/authStore';
import { useUSSLatest } from '../../hooks/useUSS';

const navItems = [
  { path: '/', label: 'Dashboard', icon: '◉' },
  { path: '/alerts', label: 'Alert Log', icon: '⚡' },
  { path: '/simulator', label: 'Simulator', icon: '◎' },
];

export function Sidebar() {
  const navigate = useNavigate();
  const logout = useAuthStore((s) => s.logout);
  const user = useAuthStore((s) => s.user);
  const { data: ussData } = useUSSLatest();

  // Count zones
  const redCount = ussData.filter((d) => d.uss >= 70).length;
  const yellowCount = ussData.filter((d) => d.uss >= 40 && d.uss < 70).length;
  const greenCount = ussData.filter((d) => d.uss < 40).length;

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <aside className="w-60 h-screen fixed left-0 top-0 flex flex-col bg-bg-subtle border-r-2 border-border-strong z-40">
      {/* Logo */}
      <div className="px-5 py-6 border-b border-border">
        <h1 className="font-display text-lg font-bold tracking-tight text-text-primary">
          SIGAP
        </h1>
        <p className="text-sm text-text-secondary mt-0.5">Kota Bandung ▾</p>
      </div>

      {/* Navigation */}
      <nav className="flex-1 py-4 px-3 space-y-1">
        {navItems.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            end={item.path === '/'}
            className={({ isActive }) =>
              `flex items-center gap-3 px-3 py-2.5 rounded-md text-sm font-medium transition-colors duration-150 ${
                isActive
                  ? 'bg-accent-subtle border-l-[3px] border-accent text-accent font-semibold'
                  : 'text-text-secondary hover:bg-border hover:text-text-primary'
              }`
            }
          >
            <span className="text-base">{item.icon}</span>
            {item.label}
          </NavLink>
        ))}
      </nav>

      {/* USS Zone Summary */}
      <div className="px-4 py-3 border-t border-border">
        <p className="text-xs font-medium uppercase tracking-widest text-text-tertiary mb-2">
          Ringkasan Zona
        </p>
        <div className="flex items-center gap-3 font-data text-xs">
          <span className="flex items-center gap-1">
            <span className="w-2 h-2 rounded-full bg-zone-red" />
            <span className="text-zone-red font-semibold">{redCount}</span>
          </span>
          <span className="flex items-center gap-1">
            <span className="w-2 h-2 rounded-full bg-zone-yellow" />
            <span className="text-zone-yellow font-semibold">{yellowCount}</span>
          </span>
          <span className="flex items-center gap-1">
            <span className="w-2 h-2 rounded-full bg-zone-green" />
            <span className="text-zone-green font-semibold">{greenCount}</span>
          </span>
        </div>
      </div>

      {/* User */}
      <div className="px-4 py-3 border-t border-border">
        <p className="text-sm font-medium text-text-primary truncate">
          {user?.full_name || 'User'}
        </p>
        <p className="text-xs text-text-tertiary">{user?.role || '-'}</p>
        <button
          onClick={handleLogout}
          className="mt-2 text-xs text-text-secondary hover:text-zone-red transition-colors duration-100"
        >
          Keluar
        </button>
      </div>
    </aside>
  );
}
