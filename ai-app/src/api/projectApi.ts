import type {
  CreateProjectPayload,
  ProjectItem,
  UpdateProjectPayload,
} from '../models/workspace';
import { apiRequest } from './client';

interface ProjectDto {
  id: string;
  name: string;
  description: string | null;
  working_directory: string;
  additional_directories: string[];
  system_prompt: string | null;
  permission_mode: string;
  allowed_tools: string[];
  disallowed_tools: string[];
  is_archived: boolean;
}

function mapProject(dto: ProjectDto): ProjectItem {
  return {
    id: dto.id,
    name: dto.name,
    description: dto.description ?? '',
    workingDirectory: dto.working_directory,
    systemPrompt: dto.system_prompt ?? '',
    permissionMode: dto.permission_mode,
    additionalDirectories: dto.additional_directories,
    allowedTools: dto.allowed_tools,
    disallowedTools: dto.disallowed_tools,
    isArchived: dto.is_archived,
    chats: [],
  };
}

export const projectApi = {
  async list(): Promise<ProjectItem[]> {
    const dtos = await apiRequest<ProjectDto[]>('/projects');
    return dtos.map(mapProject);
  },

  async create(payload: CreateProjectPayload): Promise<ProjectItem> {
    const dto = await apiRequest<ProjectDto>('/projects', {
      method: 'POST',
      body: JSON.stringify({
        name: payload.name.trim(),
        description: payload.description.trim(),
        working_directory: payload.workingDirectory.trim(),
        system_prompt: payload.systemPrompt,
        permission_mode: payload.permissionMode,
      }),
    });
    return mapProject(dto);
  },

  async update(projectId: string, payload: UpdateProjectPayload): Promise<ProjectItem> {
    const dto = await apiRequest<ProjectDto>(`/projects/${projectId}`, {
      method: 'PATCH',
      body: JSON.stringify({
        name: payload.name.trim(),
        description: payload.description.trim(),
        working_directory: payload.workingDirectory.trim(),
        system_prompt: payload.systemPrompt,
        permission_mode: payload.permissionMode,
      }),
    });
    return mapProject(dto);
  },
};
