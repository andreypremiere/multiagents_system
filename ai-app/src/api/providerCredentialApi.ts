import type {
  ProviderCredential,
  UpsertProviderCredentialPayload,
} from '../models/providerCredential';
import { apiRequest } from './client';

interface ProviderCredentialDto {
  id: string;
  provider: string;
  auth_type: string;
  masked_secret: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

function mapCredential(dto: ProviderCredentialDto): ProviderCredential {
  return {
    id: dto.id,
    provider: dto.provider,
    authType: dto.auth_type,
    maskedSecret: dto.masked_secret,
    isActive: dto.is_active,
    createdAt: dto.created_at,
    updatedAt: dto.updated_at,
  };
}

export const providerCredentialApi = {
  async list(): Promise<ProviderCredential[]> {
    const dtos = await apiRequest<ProviderCredentialDto[]>('/provider-credentials');
    return dtos.map(mapCredential);
  },

  async upsert(
    provider: string,
    payload: UpsertProviderCredentialPayload,
  ): Promise<ProviderCredential> {
    const dto = await apiRequest<ProviderCredentialDto>(
      `/provider-credentials/${encodeURIComponent(provider)}`,
      {
        method: 'PUT',
        body: JSON.stringify({ auth_type: payload.authType, secret: payload.secret }),
      },
    );
    return mapCredential(dto);
  },

  async remove(credentialId: string): Promise<void> {
    await apiRequest<void>(`/provider-credentials/${credentialId}`, { method: 'DELETE' });
  },
};
