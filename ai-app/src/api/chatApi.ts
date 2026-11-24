import type { ChatSession, CreateChatPayload } from '../models/workspace';
import { apiRequest } from './client';

interface ChatDto {
  id: string;
  project_id: string;
  title: string;
  model: string;
  effort: string | null;
  status: string;
}

function mapChat(dto: ChatDto): ChatSession {
  return {
    id: dto.id,
    projectId: dto.project_id,
    title: dto.title,
    model: dto.model,
    effort: dto.effort,
    status: dto.status,
    messages: [],
  };
}

export const chatApi = {
  async listByProject(projectId: string): Promise<ChatSession[]> {
    const dtos = await apiRequest<ChatDto[]>(`/projects/${projectId}/chats`);
    return dtos.map(mapChat);
  },

  async create(projectId: string, payload: CreateChatPayload): Promise<ChatSession> {
    const dto = await apiRequest<ChatDto>(`/projects/${projectId}/chats`, {
      method: 'POST',
      body: JSON.stringify(payload),
    });
    return mapChat(dto);
  },
};
