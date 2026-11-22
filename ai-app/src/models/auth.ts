export interface LoginCredentials {
  nickname: string;
  password: string;
}

export interface CurrentUser {
  id: string;
  nickname: string;
  name: string;
}

/** Ответ бэкенда на успешный вход. Сам JWT приходит в httpOnly-cookie. */
export interface LoginResponse {
  authenticated: boolean;
  token_type: string;
  expires_in: number;
  user: CurrentUser;
}

export interface AuthState {
  isAuthenticated: boolean;
  user: CurrentUser | null;
}
