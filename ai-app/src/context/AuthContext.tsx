import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useState,
  ReactNode,
} from 'react';
import { AuthState, LoginCredentials } from '../models/auth';
import { fetchCurrentUser, loginWithPassword, logoutUser } from '../api/authApi';

interface AuthContextValue extends AuthState {
  isInitializing: boolean;
  login: (credentials: LoginCredentials) => Promise<void>;
  logout: () => Promise<void>;
}

const AuthContext = createContext<AuthContextValue | null>(null);

interface AuthProviderProps {
  children: ReactNode;
}

/** Провайдер состояния авторизации. Сессия хранится в httpOnly-cookie. */
export function AuthProvider({ children }: AuthProviderProps) {
  const [authState, setAuthState] = useState<AuthState>({
    isAuthenticated: false,
    user: null,
  });
  const [isInitializing, setIsInitializing] = useState(true);

  // При старте проверяем cookie через защищённый эндпоинт.
  useEffect(() => {
    let cancelled = false;

    fetchCurrentUser()
      .then((user) => {
        if (!cancelled) {
          setAuthState({ isAuthenticated: true, user });
        }
      })
      .catch(() => {
        if (!cancelled) {
          setAuthState({ isAuthenticated: false, user: null });
        }
      })
      .finally(() => {
        if (!cancelled) {
          setIsInitializing(false);
        }
      });

    return () => {
      cancelled = true;
    };
  }, []);

  const login = useCallback(async (credentials: LoginCredentials) => {
    const response = await loginWithPassword(
      credentials.nickname,
      credentials.password,
    );
    setAuthState({ isAuthenticated: true, user: response.user });
  }, []);

  const logout = useCallback(async () => {
    try {
      await logoutUser();
    } finally {
      setAuthState({ isAuthenticated: false, user: null });
    }
  }, []);

  return (
    <AuthContext.Provider
      value={{ ...authState, isInitializing, login, logout }}
    >
      {children}
    </AuthContext.Provider>
  );
}

/** Хук доступа к контексту авторизации. */
export function useAuth(): AuthContextValue {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth должен использоваться внутри AuthProvider');
  }
  return context;
}
