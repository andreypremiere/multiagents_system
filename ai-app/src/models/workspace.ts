export type AgentActivityStatus = 'running' | 'done';

export interface AgentActivityStep {
  id: string;
  label: string;
  status: AgentActivityStatus;
}

export interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: string;
  activities?: AgentActivityStep[];
}

/** Чат. Сообщения пока локальные (мок), бэкенд их не хранит. */
export interface ChatSession {
  id: string;
  projectId: string;
  title: string;
  model: string;
  effort: string | null;
  status: string;
  messages: ChatMessage[];
}

export interface ProjectItem {
  id: string;
  name: string;
  description: string;
  workingDirectory: string;
  systemPrompt: string;
  permissionMode: string;
  additionalDirectories: string[];
  allowedTools: string[];
  disallowedTools: string[];
  isArchived: boolean;
  chats: ChatSession[];
}

export interface CreateProjectPayload {
  name: string;
  description: string;
  workingDirectory: string;
  systemPrompt: string;
  permissionMode: string;
}

export interface UpdateProjectPayload {
  name: string;
  description: string;
  workingDirectory: string;
  systemPrompt: string;
  permissionMode: string;
}

export interface CreateChatPayload {
  model: string;
  effort: string;
}
