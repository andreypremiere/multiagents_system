import { useEffect, useMemo, useState, type FormEvent } from 'react';

import { chatApi } from '../api/chatApi';
import { optionsApi } from '../api/optionsApi';
import { projectApi } from '../api/projectApi';
import { workspaceApi } from '../api/workspaceApi';
import { useAuth } from '../context/AuthContext';
import type { OptionsData } from '../models/options';
import type {
  AgentActivityStep,
  ChatSession,
  ProjectItem,
} from '../models/workspace';

type WorkspaceMode =
  | { kind: 'chat'; projectId: string; chatId: string }
  | { kind: 'project'; projectId: string }
  | { kind: 'create-project' };

/** Основная защищенная страница рабочего пространства. */
export function DashboardPage() {
  const { logout, user } = useAuth();

  const [options, setOptions] = useState<OptionsData | null>(null);
  const [projects, setProjects] = useState<ProjectItem[]>([]);
  const [expandedIds, setExpandedIds] = useState<Record<string, boolean>>({});
  const [mode, setMode] = useState<WorkspaceMode>({ kind: 'create-project' });
  const [isLoading, setIsLoading] = useState(true);

  const [newProjectName, setNewProjectName] = useState('');
  const [newProjectDesc, setNewProjectDesc] = useState('');
  const [newProjectWorkDir, setNewProjectWorkDir] = useState('');
  const [newProjectPrompt, setNewProjectPrompt] = useState(
    'Ты полезный технический ассистент.',
  );
  const [newProjectPermissionMode, setNewProjectPermissionMode] = useState('default');
  const [isCreatingProject, setIsCreatingProject] = useState(false);

  const [editName, setEditName] = useState('');
  const [editDesc, setEditDesc] = useState('');
  const [editWorkDir, setEditWorkDir] = useState('');
  const [editPrompt, setEditPrompt] = useState('');
  const [editPermissionMode, setEditPermissionMode] = useState('default');
  const [isSavingSettings, setIsSavingSettings] = useState(false);
  const [settingsSavedNotice, setSettingsSavedNotice] = useState(false);

  const [promptInput, setPromptInput] = useState('');
  const [isSending, setIsSending] = useState(false);
  const [liveActivities, setLiveActivities] = useState<AgentActivityStep[]>([]);

  useEffect(() => {
    let active = true;
    void (async () => {
      try {
        const [loadedOptions, loadedProjects] = await Promise.all([
          optionsApi.get(),
          projectApi.list(),
        ]);
        const chatsByProject = await Promise.all(
          loadedProjects.map((project) => chatApi.listByProject(project.id)),
        );
        if (!active) {
          return;
        }

        const data = loadedProjects.map((project, index) => ({
          ...project,
          chats: chatsByProject[index],
        }));

        setOptions(loadedOptions);
        setNewProjectPermissionMode(loadedOptions.defaultPermissionMode);
        setProjects(data);

        const initialExpanded: Record<string, boolean> = {};
        for (const item of data) {
          initialExpanded[item.id] = true;
        }
        setExpandedIds(initialExpanded);

        const firstProject = data[0];
        const firstChat = firstProject?.chats[0];
        if (firstProject && firstChat) {
          setMode({ kind: 'chat', projectId: firstProject.id, chatId: firstChat.id });
        } else if (firstProject) {
          setMode({ kind: 'project', projectId: firstProject.id });
        }
      } finally {
        if (active) {
          setIsLoading(false);
        }
      }
    })();
    return () => {
      active = false;
    };
  }, []);

  const activeProject = useMemo<ProjectItem | undefined>(() => {
    if (mode.kind === 'create-project') {
      return undefined;
    }
    return projects.find((item) => item.id === mode.projectId);
  }, [mode, projects]);

  const activeChat = useMemo<ChatSession | undefined>(() => {
    if (mode.kind !== 'chat' || !activeProject) {
      return undefined;
    }
    return activeProject.chats.find((chat) => chat.id === mode.chatId);
  }, [activeProject, mode]);

  useEffect(() => {
    if (mode.kind === 'project' && activeProject) {
      setEditName(activeProject.name);
      setEditDesc(activeProject.description);
      setEditWorkDir(activeProject.workingDirectory);
      setEditPrompt(activeProject.systemPrompt);
      setEditPermissionMode(activeProject.permissionMode);
      setSettingsSavedNotice(false);
    }
  }, [activeProject, mode.kind]);

  function toggleProjectExpand(projectId: string) {
    setExpandedIds((prev) => ({
      ...prev,
      [projectId]: !prev[projectId],
    }));
  }

  function handleSelectProject(projectId: string) {
    setExpandedIds((prev) => ({ ...prev, [projectId]: true }));
    setMode({ kind: 'project', projectId });
  }

  function handleSelectChat(projectId: string, chatId: string) {
    setExpandedIds((prev) => ({ ...prev, [projectId]: true }));
    setLiveActivities([]);
    setMode({ kind: 'chat', projectId, chatId });
  }

  async function handleCreateChat(projectId: string) {
    if (!options) {
      return;
    }
    const createdChat = await chatApi.create(projectId, {
      model: options.defaultModel,
      effort: options.defaultEffort,
    });
    setProjects((prev) =>
      prev.map((proj) =>
        proj.id === projectId
          ? { ...proj, chats: [...proj.chats, createdChat] }
          : proj,
      ),
    );
    setExpandedIds((prev) => ({ ...prev, [projectId]: true }));
    setLiveActivities([]);
    setMode({ kind: 'chat', projectId, chatId: createdChat.id });
  }

  async function handleCreateProjectSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!newProjectName.trim() || !newProjectWorkDir.trim() || isCreatingProject) {
      return;
    }
    setIsCreatingProject(true);
    try {
      const created = await projectApi.create({
        name: newProjectName,
        description: newProjectDesc,
        workingDirectory: newProjectWorkDir,
        systemPrompt: newProjectPrompt,
        permissionMode: newProjectPermissionMode,
      });
      setProjects((prev) => [...prev, { ...created, chats: [] }]);
      setExpandedIds((prev) => ({ ...prev, [created.id]: true }));
      setNewProjectName('');
      setNewProjectDesc('');
      setNewProjectWorkDir('');

      // Сразу создаём первый чат, как и раньше.
      if (options) {
        const initialChat = await chatApi.create(created.id, {
          model: options.defaultModel,
          effort: options.defaultEffort,
        });
        setProjects((prev) =>
          prev.map((proj) =>
            proj.id === created.id ? { ...proj, chats: [initialChat] } : proj,
          ),
        );
        setMode({ kind: 'chat', projectId: created.id, chatId: initialChat.id });
      } else {
        setMode({ kind: 'project', projectId: created.id });
      }
    } finally {
      setIsCreatingProject(false);
    }
  }

  async function handleSaveProjectSettings(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!activeProject || !editName.trim() || !editWorkDir.trim() || isSavingSettings) {
      return;
    }
    setIsSavingSettings(true);
    setSettingsSavedNotice(false);
    try {
      const updated = await projectApi.update(activeProject.id, {
        name: editName,
        description: editDesc,
        workingDirectory: editWorkDir,
        systemPrompt: editPrompt,
        permissionMode: editPermissionMode,
      });
      setProjects((prev) =>
        prev.map((proj) =>
          proj.id === activeProject.id
            ? {
                ...proj,
                name: updated.name,
                description: updated.description,
                workingDirectory: updated.workingDirectory,
                systemPrompt: updated.systemPrompt,
                permissionMode: updated.permissionMode,
              }
            : proj,
        ),
      );
      setSettingsSavedNotice(true);
    } finally {
      setIsSavingSettings(false);
    }
  }

  async function handleSendMessage(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!activeProject || !activeChat || !promptInput.trim() || isSending) {
      return;
    }

    const text = promptInput.trim();
    setPromptInput('');
    setIsSending(true);
    setLiveActivities([
      { id: 'live-1', label: 'Анализ запроса пользователя', status: 'running' },
      { id: 'live-2', label: 'Выполнение шага агента', status: 'running' },
    ]);

    try {
      const { userMessage, assistantMessage } = await workspaceApi.sendMessage(
        activeProject,
        activeChat,
        text,
      );

      setProjects((prev) =>
        prev.map((proj) => {
          if (proj.id !== activeProject.id) {
            return proj;
          }
          const nextChats = proj.chats.map((chat) => {
            if (chat.id !== activeChat.id) {
              return chat;
            }
            const nextTitle =
              chat.messages.length === 0 && chat.title === 'Новый чат'
                ? text.slice(0, 36)
                : chat.title;
            return {
              ...chat,
              title: nextTitle,
              messages: [...chat.messages, userMessage, assistantMessage],
            };
          });
          return { ...proj, chats: nextChats };
        }),
      );
    } finally {
      setIsSending(false);
      setLiveActivities([]);
    }
  }

  const displayedActivities = isSending
    ? liveActivities
    : activeChat?.messages
        .slice()
        .reverse()
        .find((m) => m.role === 'assistant' && m.activities?.length)?.activities ?? [];

  const permissionModes = options?.permissionModes ?? [];

  return (
    <div className="min-h-screen bg-zinc-50 text-zinc-900 flex flex-col">
      <header className="bg-white border-b border-zinc-200/80 px-6 py-3.5 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <span className="h-2.5 w-2.5 rounded-full bg-[#722323]" />
          <span className="text-sm font-medium text-zinc-900">
            {user ? `Рабочее пространство — ${user.name}` : 'Рабочее пространство'}
          </span>
        </div>

        <button
          type="button"
          onClick={() => void logout()}
          className="rounded-xl border border-zinc-200 px-3.5 py-1.5 text-xs font-medium text-zinc-700 transition-all duration-150 hover:border-[#722323] hover:text-[#722323] active:scale-95"
        >
          Выйти
        </button>
      </header>

      <div className="flex-1 max-w-7xl w-full mx-auto p-4 md:p-6 grid grid-cols-1 md:grid-cols-[300px_minmax(0,1fr)] gap-5 items-start">
        <aside className="bg-white border border-zinc-200/80 rounded-2xl p-4 flex flex-col gap-3">
          <div className="flex items-center justify-between gap-2">
            <h1 className="text-xs font-semibold uppercase tracking-wider text-zinc-500">
              Проекты
            </h1>
            <button
              type="button"
              onClick={() => setMode({ kind: 'create-project' })}
              className={`rounded-xl px-3 py-1.5 text-xs font-medium transition-all duration-150 active:scale-95 ${
                mode.kind === 'create-project'
                  ? 'bg-[#722323] text-white'
                  : 'border border-zinc-200 text-zinc-700 hover:border-[#722323] hover:text-[#722323]'
              }`}
            >
              + Новый проект
            </button>
          </div>

          {isLoading ? (
            <div className="py-8 text-center text-xs text-zinc-400">
              Загрузка проектов...
            </div>
          ) : (
            <nav aria-label="Список проектов" className="flex flex-col gap-1.5">
              {projects.map((project) => {
                const isExpanded = Boolean(expandedIds[project.id]);
                const isProjectSelected =
                  mode.kind === 'project' && mode.projectId === project.id;

                return (
                  <div
                    key={project.id}
                    className="rounded-xl border border-zinc-200/70 bg-zinc-50/50 overflow-hidden"
                  >
                    <div
                      className={`flex items-center justify-between gap-1 px-2.5 py-2 transition-colors ${
                        isProjectSelected ? 'bg-[#722323]/10' : 'hover:bg-zinc-100/80'
                      }`}
                    >
                      <button
                        type="button"
                        onClick={() => toggleProjectExpand(project.id)}
                        aria-label={isExpanded ? 'Свернуть чаты' : 'Развернуть чаты'}
                        className="w-6 h-6 rounded-lg flex items-center justify-center text-zinc-500 hover:text-zinc-900 hover:bg-zinc-200/60 transition-colors text-xs"
                      >
                        {isExpanded ? '▾' : '▸'}
                      </button>

                      <button
                        type="button"
                        onClick={() => handleSelectProject(project.id)}
                        className={`flex-1 text-left truncate text-xs font-medium px-1 py-0.5 transition-colors ${
                          isProjectSelected
                            ? 'text-[#722323]'
                            : 'text-zinc-800 hover:text-[#722323]'
                        }`}
                      >
                        {project.name}
                      </button>

                      <button
                        type="button"
                        onClick={() => void handleCreateChat(project.id)}
                        title="Создать новый чат"
                        aria-label={`Создать новый чат в проекте ${project.name}`}
                        className="w-7 h-7 rounded-lg border border-zinc-200 bg-white flex items-center justify-center text-zinc-700 hover:border-[#722323] hover:text-[#722323] transition-all duration-150 active:scale-95 text-sm leading-none"
                      >
                        +
                      </button>
                    </div>

                    {isExpanded && (
                      <ul className="px-2 pb-2 pt-1 flex flex-col gap-1 border-t border-zinc-200/60 bg-white">
                        {project.chats.length === 0 ? (
                          <li className="px-2.5 py-1.5 text-[11px] text-zinc-400">
                            Чатов пока нет
                          </li>
                        ) : (
                          project.chats.map((chat) => {
                            const isChatSelected =
                              mode.kind === 'chat' &&
                              mode.projectId === project.id &&
                              mode.chatId === chat.id;

                            return (
                              <li key={chat.id}>
                                <button
                                  type="button"
                                  onClick={() => handleSelectChat(project.id, chat.id)}
                                  className={`w-full text-left px-2.5 py-1.5 rounded-lg text-xs truncate transition-colors ${
                                    isChatSelected
                                      ? 'bg-[#722323] text-white font-medium'
                                      : 'text-zinc-600 hover:bg-zinc-100 hover:text-zinc-900'
                                  }`}
                                >
                                  {chat.title}
                                </button>
                              </li>
                            );
                          })
                        )}
                      </ul>
                    )}
                  </div>
                );
              })}
            </nav>
          )}
        </aside>

        <main className="bg-white border border-zinc-200/80 rounded-2xl p-5 md:p-6 min-h-[540px] flex flex-col">
          {mode.kind === 'create-project' && (
            <section className="max-w-2xl w-full flex flex-col gap-5">
              <div>
                <h2 className="text-base font-semibold text-zinc-900">
                  Новый проект
                </h2>
                <p className="text-xs text-zinc-500 mt-1">
                  Задайте название, рабочую директорию и режим разрешений.
                </p>
              </div>

              <form onSubmit={(e) => void handleCreateProjectSubmit(e)} className="flex flex-col gap-4">
                <label className="flex flex-col gap-1.5 text-xs font-medium text-zinc-700">
                  Название проекта
                  <input
                    type="text"
                    required
                    value={newProjectName}
                    onChange={(e) => setNewProjectName(e.target.value)}
                    placeholder="Например, Агент аналитики логов"
                    className="rounded-xl border border-zinc-200 bg-zinc-50/60 px-3.5 py-2 text-sm text-zinc-900 outline-none transition-colors focus:border-[#722323] focus:bg-white"
                  />
                </label>

                <label className="flex flex-col gap-1.5 text-xs font-medium text-zinc-700">
                  Описание
                  <textarea
                    rows={2}
                    value={newProjectDesc}
                    onChange={(e) => setNewProjectDesc(e.target.value)}
                    placeholder="Краткое назначение проекта"
                    className="rounded-xl border border-zinc-200 bg-zinc-50/60 px-3.5 py-2 text-sm text-zinc-900 outline-none transition-colors focus:border-[#722323] focus:bg-white resize-none"
                  />
                </label>

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <label className="flex flex-col gap-1.5 text-xs font-medium text-zinc-700">
                    Рабочая директория
                    <input
                      type="text"
                      required
                      value={newProjectWorkDir}
                      onChange={(e) => setNewProjectWorkDir(e.target.value)}
                      placeholder="/workspace/my-project"
                      className="rounded-xl border border-zinc-200 bg-zinc-50/60 px-3.5 py-2 text-sm text-zinc-900 outline-none transition-colors focus:border-[#722323] focus:bg-white"
                    />
                  </label>

                  <label className="flex flex-col gap-1.5 text-xs font-medium text-zinc-700">
                    Режим разрешений
                    <select
                      value={newProjectPermissionMode}
                      onChange={(e) => setNewProjectPermissionMode(e.target.value)}
                      className="rounded-xl border border-zinc-200 bg-zinc-50/60 px-3.5 py-2 text-sm text-zinc-900 outline-none transition-colors focus:border-[#722323] focus:bg-white"
                    >
                      {permissionModes.map((option) => (
                        <option key={option.value} value={option.value}>
                          {option.label}
                        </option>
                      ))}
                    </select>
                  </label>
                </div>

                <label className="flex flex-col gap-1.5 text-xs font-medium text-zinc-700">
                  Системный промпт по умолчанию
                  <textarea
                    rows={4}
                    value={newProjectPrompt}
                    onChange={(e) => setNewProjectPrompt(e.target.value)}
                    className="rounded-xl border border-zinc-200 bg-zinc-50/60 px-3.5 py-2 text-sm text-zinc-900 outline-none transition-colors focus:border-[#722323] focus:bg-white resize-none"
                  />
                </label>

                <div className="pt-1 flex items-center gap-3">
                  <button
                    type="submit"
                    disabled={isCreatingProject}
                    className="rounded-xl bg-[#722323] px-4 py-2 text-xs font-medium text-white transition-all duration-150 hover:bg-[#5c1c1c] active:scale-95 disabled:opacity-60"
                  >
                    {isCreatingProject ? 'Создание...' : 'Создать проект'}
                  </button>
                </div>
              </form>
            </section>
          )}

          {mode.kind === 'project' && activeProject && (
            <section className="max-w-2xl w-full flex flex-col gap-5">
              <div className="flex items-start justify-between gap-4 border-b border-zinc-100 pb-4">
                <div>
                  <h2 className="text-base font-semibold text-zinc-900">
                    Настройки проекта — {activeProject.name}
                  </h2>
                  <p className="text-xs text-zinc-500 mt-1">
                    Параметры применяются к новым запускам и чатам внутри проекта.
                  </p>
                </div>
                <button
                  type="button"
                  onClick={() => void handleCreateChat(activeProject.id)}
                  className="rounded-xl border border-zinc-200 px-3 py-1.5 text-xs font-medium text-zinc-700 transition-all duration-150 hover:border-[#722323] hover:text-[#722323] active:scale-95"
                >
                  + Новый чат
                </button>
              </div>

              <form onSubmit={(e) => void handleSaveProjectSettings(e)} className="flex flex-col gap-4">
                <label className="flex flex-col gap-1.5 text-xs font-medium text-zinc-700">
                  Название проекта
                  <input
                    type="text"
                    required
                    value={editName}
                    onChange={(e) => setEditName(e.target.value)}
                    className="rounded-xl border border-zinc-200 bg-zinc-50/60 px-3.5 py-2 text-sm text-zinc-900 outline-none transition-colors focus:border-[#722323] focus:bg-white"
                  />
                </label>

                <label className="flex flex-col gap-1.5 text-xs font-medium text-zinc-700">
                  Описание
                  <textarea
                    rows={2}
                    value={editDesc}
                    onChange={(e) => setEditDesc(e.target.value)}
                    className="rounded-xl border border-zinc-200 bg-zinc-50/60 px-3.5 py-2 text-sm text-zinc-900 outline-none transition-colors focus:border-[#722323] focus:bg-white resize-none"
                  />
                </label>

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <label className="flex flex-col gap-1.5 text-xs font-medium text-zinc-700">
                    Рабочая директория
                    <input
                      type="text"
                      required
                      value={editWorkDir}
                      onChange={(e) => setEditWorkDir(e.target.value)}
                      className="rounded-xl border border-zinc-200 bg-zinc-50/60 px-3.5 py-2 text-sm text-zinc-900 outline-none transition-colors focus:border-[#722323] focus:bg-white"
                    />
                  </label>

                  <label className="flex flex-col gap-1.5 text-xs font-medium text-zinc-700">
                    Режим разрешений
                    <select
                      value={editPermissionMode}
                      onChange={(e) => setEditPermissionMode(e.target.value)}
                      className="rounded-xl border border-zinc-200 bg-zinc-50/60 px-3.5 py-2 text-sm text-zinc-900 outline-none transition-colors focus:border-[#722323] focus:bg-white"
                    >
                      {permissionModes.map((option) => (
                        <option key={option.value} value={option.value}>
                          {option.label}
                        </option>
                      ))}
                    </select>
                  </label>
                </div>

                <label className="flex flex-col gap-1.5 text-xs font-medium text-zinc-700">
                  Системный промпт
                  <textarea
                    rows={4}
                    value={editPrompt}
                    onChange={(e) => setEditPrompt(e.target.value)}
                    className="rounded-xl border border-zinc-200 bg-zinc-50/60 px-3.5 py-2 text-sm text-zinc-900 outline-none transition-colors focus:border-[#722323] focus:bg-white resize-none"
                  />
                </label>

                <div className="pt-1 flex items-center gap-3">
                  <button
                    type="submit"
                    disabled={isSavingSettings}
                    className="rounded-xl bg-[#722323] px-4 py-2 text-xs font-medium text-white transition-all duration-150 hover:bg-[#5c1c1c] active:scale-95 disabled:opacity-60"
                  >
                    {isSavingSettings ? 'Сохранение...' : 'Сохранить настройки'}
                  </button>
                  {settingsSavedNotice && (
                    <span className="text-xs text-zinc-600">Сохранено</span>
                  )}
                </div>
              </form>
            </section>
          )}

          {mode.kind === 'chat' && activeProject && activeChat && (
            <section className="flex-1 flex flex-col justify-between gap-4">
              <div className="flex flex-wrap items-center justify-between gap-2 border-b border-zinc-100 pb-3.5">
                <div>
                  <div className="flex items-center gap-2 text-xs text-zinc-500">
                    <button
                      type="button"
                      onClick={() => handleSelectProject(activeProject.id)}
                      className="hover:text-[#722323] transition-colors font-medium"
                    >
                      {activeProject.name}
                    </button>
                    <span>/</span>
                    <span>{activeChat.model}</span>
                  </div>
                  <h2 className="text-base font-semibold text-zinc-900 mt-0.5">
                    {activeChat.title}
                  </h2>
                </div>
              </div>

              {displayedActivities.length > 0 && (
                <div className="rounded-xl border border-zinc-200/80 bg-zinc-50 px-3.5 py-2.5 flex flex-col gap-1.5">
                  <span className="text-[11px] font-semibold uppercase tracking-wider text-zinc-500">
                    Активность агента
                  </span>
                  <ul className="flex flex-col gap-1">
                    {displayedActivities.map((step) => (
                      <li
                        key={step.id}
                        className="flex items-center justify-between text-xs text-zinc-700"
                      >
                        <span>{step.label}</span>
                        <span
                          className={`text-[11px] font-medium ${
                            step.status === 'running'
                              ? 'text-[#722323]'
                              : 'text-zinc-500'
                          }`}
                        >
                          {step.status === 'running' ? 'выполняется...' : 'готово'}
                        </span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              <div className="flex-1 flex flex-col gap-3 overflow-y-auto max-h-[360px] pr-1">
                {activeChat.messages.length === 0 ? (
                  <div className="my-auto py-12 text-center text-xs text-zinc-400">
                    Сообщений пока нет. Напишите запрос, чтобы начать диалог.
                  </div>
                ) : (
                  activeChat.messages.map((msg) => (
                    <div
                      key={msg.id}
                      className={`max-w-2xl rounded-2xl px-4 py-3 text-sm leading-relaxed ${
                        msg.role === 'user'
                          ? 'self-end bg-[#722323] text-white'
                          : 'self-start bg-zinc-100 text-zinc-900 border border-zinc-200/70'
                      }`}
                    >
                      <div>{msg.content}</div>
                      <div
                        className={`text-[10px] mt-1.5 ${
                          msg.role === 'user' ? 'text-white/75 text-right' : 'text-zinc-400'
                        }`}
                      >
                        {msg.timestamp}
                      </div>
                    </div>
                  ))
                )}
              </div>

              <form
                onSubmit={(e) => void handleSendMessage(e)}
                className="border-t border-zinc-100 pt-3.5 flex items-end gap-2.5"
              >
                <textarea
                  rows={2}
                  value={promptInput}
                  onChange={(e) => setPromptInput(e.target.value)}
                  placeholder="Введите сообщение для агента..."
                  className="flex-1 rounded-xl border border-zinc-200 bg-zinc-50/60 px-3.5 py-2 text-sm text-zinc-900 outline-none transition-colors focus:border-[#722323] focus:bg-white resize-none"
                />
                <button
                  type="submit"
                  disabled={isSending || !promptInput.trim()}
                  className="rounded-xl bg-[#722323] px-4 py-2.5 text-xs font-medium text-white transition-all duration-150 hover:bg-[#5c1c1c] active:scale-95 disabled:opacity-50"
                >
                  {isSending ? 'Отправка...' : 'Отправить'}
                </button>
              </form>
            </section>
          )}
        </main>
      </div>
    </div>
  );
}
