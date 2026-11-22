import type {
  ChatMessage,
  ChatSession,
  CreateProjectPayload,
  ProjectItem,
  ProjectSettings,
} from '../models/workspace';

const INITIAL_PROJECTS: ProjectItem[] = [
  {
    id: 'proj-core',
    name: 'Платформа оркестрации',
    description: 'Основной контур работы агентов, маршрутизации задач и инструментов.',
    settings: {
      systemPrompt: 'Ты технический ассистент. Отвечай лаконично и по существу.',
      model: 'claude-sonnet',
      environment: 'development',
    },
    chats: [
      {
        id: 'chat-1',
        projectId: 'proj-core',
        title: 'Разбор архитектуры воркфлоу',
        messages: [
          {
            id: 'msg-1',
            role: 'user',
            content: 'Проверь текущий поток выполнения шагов агента.',
            timestamp: '14:12',
          },
          {
            id: 'msg-2',
            role: 'assistant',
            content: 'Граф шагов проверен: узлы инициализации, планирования и проверки результата связаны последовательно.',
            timestamp: '14:13',
            activities: [
              { id: 'act-1', label: 'Чтение конфигурации проекта', status: 'done' },
              { id: 'act-2', label: 'Проверка графа выполнения', status: 'done' },
            ],
          },
        ],
      },
      {
        id: 'chat-2',
        projectId: 'proj-core',
        title: 'Проверка контрактов API',
        messages: [
          {
            id: 'msg-3',
            role: 'user',
            content: 'Подготовь список эндпоинтов для проектов и чатов.',
            timestamp: '15:04',
          },
        ],
      },
    ],
  },
  {
    id: 'proj-ui',
    name: 'Веб-клиент и UI',
    description: 'Интерфейс оператора, панели управления и отображение статусов.',
    settings: {
      systemPrompt: 'Помогай проектировать строгие и минималистичные интерфейсы.',
      model: 'claude-opus',
      environment: 'staging',
    },
    chats: [
      {
        id: 'chat-3',
        projectId: 'proj-ui',
        title: 'Компоновка рабочего стола',
        messages: [
          {
            id: 'msg-4',
            role: 'user',
            content: 'Собери базовый макет панели проектов и рабочей зоны.',
            timestamp: '16:20',
          },
        ],
      },
    ],
  },
];

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
  async listProjects(): Promise<ProjectItem[]> {
    await delay(120);
    return structuredClone(INITIAL_PROJECTS);
  },

  async createProject(payload: CreateProjectPayload): Promise<ProjectItem> {
    await delay(160);
    const projectId = `proj-${Date.now()}`;
    return {
      id: projectId,
      name: payload.name.trim(),
      description: payload.description.trim(),
      settings: { ...payload.settings },
      chats: [
        {
          id: `chat-${Date.now()}`,
          projectId,
          title: 'Новый чат',
          messages: [],
        },
      ],
    };
  },

  async updateProjectSettings(
    projectId: string,
    payload: { name: string; description: string; settings: ProjectSettings },
  ): Promise<{ name: string; description: string; settings: ProjectSettings }> {
    await delay(140);
    void projectId;
    return {
      name: payload.name.trim(),
      description: payload.description.trim(),
      settings: { ...payload.settings },
    };
  },

  async createChat(projectId: string, title = 'Новый чат'): Promise<ChatSession> {
    await delay(120);
    return {
      id: `chat-${Date.now()}`,
      projectId,
      title,
      messages: [],
    };
  },

  async sendMessage(
    project: ProjectItem,
    chatId: string,
    content: string,
  ): Promise<{ userMessage: ChatMessage; assistantMessage: ChatMessage }> {
    void chatId;
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
      content: `Запрос принят в контексте проекта «${project.name}» (${project.settings.model}). Мок-ответ сформирован.`,
      timestamp: formatCurrentTime(),
      activities: [
        { id: `step-1-${Date.now()}`, label: 'Загрузка системного промпта', status: 'done' },
        { id: `step-2-${Date.now()}`, label: 'Формирование ответа агента', status: 'done' },
      ],
    };

    return { userMessage, assistantMessage };
  },
};