import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuthStore } from '../store/authStore';
import api from '../lib/api';

export default function Login() {
  const [email, setEmail] = useState('admin@sigap.id');
  const [password, setPassword] = useState('Admin123!');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const { setTokens, setUser } = useAuthStore();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const res = await api.post('/auth/login', { email, password });
      setTokens(res.data.access_token, res.data.refresh_token);

      // Fetch user profile
      const profile = await api.get('/auth/me', {
        headers: { Authorization: `Bearer ${res.data.access_token}` },
      });
      setUser(profile.data);

      navigate('/');
    } catch {
      setError('Email atau password salah');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-bg flex items-center justify-center px-4">
      <div className="w-full max-w-sm">
        {/* Logo */}
        <div className="text-center mb-8">
          <h1 className="font-display text-3xl font-bold text-text-primary tracking-tight">
            SIGAP
          </h1>
          <p className="text-sm text-text-secondary mt-2 leading-relaxed">
            Smart Integrated Geo-Analytics<br />for Urban Pressure
          </p>
        </div>

        {/* Login Form */}
        <form
          onSubmit={handleSubmit}
          className="bg-surface rounded-lg shadow-md p-6 border border-border"
        >
          <h2 className="font-display text-lg font-semibold text-text-primary mb-5">
            Masuk ke Dashboard
          </h2>

          {error && (
            <div className="mb-4 p-3 rounded-md bg-zone-red-bg text-zone-red text-sm border-l-[3px] border-zone-red">
              {error}
            </div>
          )}

          <div className="space-y-4">
            <div>
              <label
                htmlFor="email-input"
                className="block text-xs font-medium uppercase tracking-wider text-text-tertiary mb-1.5"
              >
                Email
              </label>
              <input
                id="email-input"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full px-3 py-2.5 rounded-md border border-border bg-surface text-sm text-text-primary placeholder-text-tertiary focus:border-accent focus:ring-0 transition-colors duration-100"
                placeholder="admin@sigap.id"
                required
              />
            </div>

            <div>
              <label
                htmlFor="password-input"
                className="block text-xs font-medium uppercase tracking-wider text-text-tertiary mb-1.5"
              >
                Password
              </label>
              <input
                id="password-input"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full px-3 py-2.5 rounded-md border border-border bg-surface text-sm text-text-primary placeholder-text-tertiary focus:border-accent focus:ring-0 transition-colors duration-100"
                placeholder="••••••••"
                required
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full py-2.5 rounded-md bg-accent text-text-inverse text-sm font-semibold hover:bg-accent-hover transition-colors duration-100 disabled:opacity-50"
            >
              {loading ? 'Memproses...' : 'Masuk'}
            </button>
          </div>

          <p className="text-xs text-text-tertiary mt-4 text-center">
            Demo: admin@sigap.id / Admin123!
          </p>
        </form>

        <p className="text-xs text-text-tertiary text-center mt-6">
          © 2026 SIGAP — Kota Bandung
        </p>
      </div>
    </div>
  );
}
