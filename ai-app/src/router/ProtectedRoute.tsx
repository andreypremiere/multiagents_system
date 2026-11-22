import { Navigate, Outlet } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

/** Ограничивает доступ к дочерним маршрутам для неавторизованных пользователей. */
export function ProtectedRoute() {
  const { isAuthenticated, isInitializing } = useAuth();

  // Пока не завершена проверка cookie, не редиректим — иначе пользователь
  // увидит форму входа каждый раз при перезагрузке страницы.
  if (isInitializing) {
    return null;
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  return <Outlet />;
}
