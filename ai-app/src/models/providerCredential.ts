/** Ключ провайдера в замаскированном виде. Секрет на фронт не приходит. */
export interface ProviderCredential {
  id: string;
  provider: string;
  authType: string;
  maskedSecret: string;
  isActive: boolean;
  createdAt: string;
  updatedAt: string;
}

export interface UpsertProviderCredentialPayload {
  authType: string;
  secret: string;
}
