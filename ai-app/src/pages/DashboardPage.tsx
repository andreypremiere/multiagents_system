import { useAuth } from '../context/AuthContext';

/** Главная защищенная страница приложения. */
export function DashboardPage() {
  const { logout, user } = useAuth();

  return (
    <div className="min-h-full bg-zinc-50 p-6">
      <header className="max-w-4xl mx-auto flex items-center justify-between bg-white border border-zinc-200/80 rounded-2xl px-6 py-4">
        <span className="text-sm font-medium text-zinc-900">
          {user ? `Рабочее пространство — ${user.name}` : 'Рабочее пространство'}
        </span>
        <button
          type="button"
          onClick={() => void logout()}
          className="rounded-xl border border-zinc-200 px-3.5 py-1.5 text-xs font-medium text-zinc-700 transition-all duration-150 hover:border-[#722323] hover:text-[#722323] active:scale-95"
        >
          Выйти
        </button>
      </header>
    </div>
  );
}