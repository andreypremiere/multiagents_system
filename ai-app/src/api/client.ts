/** Базовый URL API. Совпадает с authApi. */
export const API_BASE = '/api/v1';

/** Достаёт текст ошибки из тела ответа FastAPI (поле detail). */
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

/**
 * Запрос к защищённому API. Сессия передаётся через httpOnly-cookie.
 * Возвращает распарсенный JSON либо undefined для ответов 204.
 */
export async function apiRequest<T>(path: string, init: RequestInit = {}): Promise<T> {
  const headers = new Headers(init.headers);
  if (init.body !== undefined && !headers.has('Content-Type')) {
    headers.set('Content-Type', 'application/json');
  }

  const response = await fetch(`${API_BASE}${path}`, {
    ...init,
    headers,
    credentials: 'include',
  });

  if (!response.ok) {
    throw new Error(await readErrorDetail(response));
  }

  if (response.status === 204) {
    return undefined as T;
  }

  return (await response.json()) as T;
}
