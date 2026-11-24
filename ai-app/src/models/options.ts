/** Один вариант выбора из константного списка бэкенда. */
export interface OptionItem {
  value: string;
  label: string;
  description: string | null;
  dangerous: boolean | null;
  category: string | null;
}

/** Все константные списки, полученные с GET /options. */
export interface OptionsData {
  agentModels: OptionItem[];
  permissionModes: OptionItem[];
  effortLevels: OptionItem[];
  toolOptions: OptionItem[];
  defaultModel: string;
  defaultPermissionMode: string;
  defaultEffort: string;
}
