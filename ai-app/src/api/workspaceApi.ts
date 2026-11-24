import type {
  ChatMessage,
  ChatSession,
  ProjectItem,
} from '../models/workspace';

/** Мок отправки сообщений. Будет заменён реальным API отдельной задачей. */

function delay(ms: number): Promise<void> {
  return new Promise((resolve) => {
    window.setTimeout(resolve, ms);
  });
}

function formatCurrentTime(): string {
  const now = new Date();
  return now.toLocaleTimeString('ru-RU', { hour: '2-digit', minute: '2-digit' });
}

export const workspaceApi = {
  async sendMessage(
    project: ProjectItem,
    chat: ChatSession,
    content: string,
  ): Promise<{ userMessage: ChatMessage; assistantMessage: ChatMessage }> {
    await delay(260);
    const timestamp = formatCurrentTime();

    const userMessage: ChatMessage = {
      id: `msg-u-${Date.now()}`,
      role: 'user',
      content: content.trim(),
      timestamp,
    };

    const assistantMessage: ChatMessage = {
      id: `msg-a-${Date.now() + 1}`,
      role: 'assistant',
      content: `Запрос принят в контексте проекта «${project.name}» (${chat.model}). Мок-ответ сформирован.`,
      timestamp: formatCurrentTime(),
      activities: [
        { id: `step-1-${Date.now()}`, label: 'Загрузка системного промпта', status: 'done' },
        { id: `step-2-${Date.now()}`, label: 'Формирование ответа агента', status: 'done' },
      ],
    };

    return { userMessage, assistantMessage };
  },
};
