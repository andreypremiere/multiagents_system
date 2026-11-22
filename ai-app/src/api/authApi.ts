import type { CurrentUser, LoginResponse } from '../models/auth';

const API_BASE = '/api/v1';

async function readErrorDetail(response: Response): Promise<string> {
  try {
    const data: unknown = await response.json();
    if (
      typeof data === 'object' &&
      data !== null &&
      'detail' in data &&
      typeof data.detail === 'string'
    ) {
      return data.detail;
    }
  } catch {
    // Тело ответа не JSON — используем общий текст ниже.
  }
  return 'Ошибка запроса';
}

/** Отправляет никнейм и пароль на бэкенд. JWT сохраняется сервером в httpOnly-cookie. */
export async function loginWithPassword(
  nickname: string,
  password: string,
): Promise<LoginResponse> {
  const response = await fetch(`${API_BASE}/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    credentials: 'include',
    body: JSON.stringify({ nickname: nickname.trim(), password }),
  });

  if (!response.ok) {
    throw new Error(await readErrorDetail(response));
  }

  return (await response.json()) as LoginResponse;
}

/** Возвращает текущего пользователя по cookie. Используется для проверки сессии. */
export async function fetchCurrentUser(): Promise<CurrentUser> {
  const response = await fetch(`${API_BASE}/users/me`, {
    credentials: 'include',
  });

  if (!response.ok) {
    throw new Error('Не авторизован');
  }

  return (await response.json()) as CurrentUser;
}

/** Удаляет cookie с токеном на сервере. */
export async function logoutUser(): Promise<void> {
  await fetch(`${API_BASE}/auth/logout`, {
    method: 'POST',
    credentials: 'include',
  });
}
