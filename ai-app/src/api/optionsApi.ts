import type { OptionsData, OptionItem } from '../models/options';
import { apiRequest } from './client';

interface OptionsDto {
  agent_models: OptionItem[];
  permission_modes: OptionItem[];
  effort_levels: OptionItem[];
  tool_options: OptionItem[];
  default_model: string;
  default_permission_mode: string;
  default_effort: string;
}

export const optionsApi = {
  async get(): Promise<OptionsData> {
    const dto = await apiRequest<OptionsDto>('/options');
    return {
      agentModels: dto.agent_models,
      permissionModes: dto.permission_modes,
      effortLevels: dto.effort_levels,
      toolOptions: dto.tool_options,
      defaultModel: dto.default_model,
      defaultPermissionMode: dto.default_permission_mode,
      defaultEffort: dto.default_effort,
    };
  },
};
