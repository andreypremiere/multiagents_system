import { useState, FormEvent } from 'react';
import { Navigate, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

/** Страница входа по никнейму и паролю. */
export function LoginPage() {
  const { isAuthenticated, isInitializing, login } = useAuth();
  const navigate = useNavigate();

  const [nickname, setNickname] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  if (isInitializing) {
    return null;
  }

  if (isAuthenticated) {
    return <Navigate to="/" replace />;
  }

  const isFormFilled = nickname.trim().length > 0 && password.length > 0;

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setErrorMessage(null);
    setIsSubmitting(true);

    try {
      await login({ nickname, password });
      navigate('/', { replace: true });
    } catch (error) {
      const message =
        error instanceof Error ? error.message : 'Ошибка входа';
      setErrorMessage(message);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="min-h-full flex items-center justify-center px-4 py-12 bg-zinc-50">
      <div className="w-full max-w-sm bg-white border border-zinc-200/80 rounded-2xl shadow-sm p-8">
        <div className="mb-8">
          <div className="w-9 h-9 rounded-xl bg-[#722323] flex items-center justify-center mb-5">
            <svg
              className="w-4 h-4 text-white"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            >
              <path d="M21 2l-2 2m-7.61 7.61a5.5 5.5 0 1 1-7.778 7.778 5.5 5.5 0 0 1 7.777-7.777zm0 0L15.5 7.5m0 0l3 3L22 7l-3-3m-3.5 3.5L19 4" />
            </svg>
          </div>
          <h1 className="text-xl font-semibold tracking-tight text-zinc-900">
            Вход в систему
          </h1>
          <p className="mt-1.5 text-sm text-zinc-500">
            Введите никнейм и пароль для продолжения работы
          </p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-5">
          <div>
            <label
              htmlFor="nickname"
              className="block text-xs font-medium uppercase tracking-wider text-zinc-500 mb-2"
            >
              Никнейм
            </label>
            <input
              id="nickname"
              type="text"
              value={nickname}
              onChange={(e) => setNickname(e.target.value)}
              placeholder="your_nickname"
              autoComplete="username"
              autoFocus
              disabled={isSubmitting}
              maxLength={50}
              className="w-full rounded-xl border border-zinc-200 bg-zinc-50/50 px-3.5 py-2.5 text-sm text-zinc-900 placeholder:text-zinc-400 transition-all duration-150 hover:border-zinc-300 focus:border-[#722323] focus:bg-white focus:outline-none focus:ring-2 focus:ring-[#722323]/15 disabled:opacity-60"
            />
          </div>

          <div>
            <label
              htmlFor="password"
              className="block text-xs font-medium uppercase tracking-wider text-zinc-500 mb-2"
            >
              Пароль
            </label>
            <div className="relative">
              <input
                id="password"
                type={showPassword ? 'text' : 'password'}
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
                autoComplete="current-password"
                disabled={isSubmitting}
                className="w-full rounded-xl border border-zinc-200 bg-zinc-50/50 px-3.5 py-2.5 pr-16 text-sm text-zinc-900 placeholder:text-zinc-400 transition-all duration-150 hover:border-zinc-300 focus:border-[#722323] focus:bg-white focus:outline-none focus:ring-2 focus:ring-[#722323]/15 disabled:opacity-60"
              />
              <button
                type="button"
                onClick={() => setShowPassword((prev) => !prev)}
                className="absolute right-2 top-1/2 -translate-y-1/2 rounded-lg px-2 py-1 text-xs font-medium text-zinc-500 transition-colors hover:bg-zinc-100 hover:text-zinc-800 active:scale-95"
              >
                {showPassword ? 'Скрыть' : 'Показать'}
              </button>
            </div>
          </div>

          {errorMessage && (
            <div className="rounded-xl border border-red-200 bg-red-50/80 px-3.5 py-2.5 text-xs text-red-700">
              {errorMessage}
            </div>
          )}

          <button
            type="submit"
            disabled={isSubmitting || !isFormFilled}
            className="w-full rounded-xl bg-[#722323] px-4 py-2.5 text-sm font-medium text-white shadow-xs transition-all duration-150 hover:bg-[#5c1c1c] hover:shadow active:scale-[0.98] disabled:cursor-not-allowed disabled:opacity-45 disabled:hover:bg-[#722323] disabled:active:scale-100"
          >
            {isSubmitting ? 'Проверка...' : 'Войти'}
          </button>
        </form>
      </div>
    </div>
  );
}
