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

export interface ChatSession {
  id: string;
  projectId: string;
  title: string;
  messages: ChatMessage[];
}

export type ProjectEnvironment = 'development' | 'staging' | 'production';

export interface ProjectSettings {
  systemPrompt: string;
  model: string;
  environment: ProjectEnvironment;
}

export interface ProjectItem {
  id: string;
  name: string;
  description: string;
  settings: ProjectSettings;
  chats: ChatSession[];
}

export interface CreateProjectPayload {
  name: string;
  description: string;
  settings: ProjectSettings;
}