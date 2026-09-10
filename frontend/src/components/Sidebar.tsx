"use client";

export type Tab = "overview" | "chat" | "tasks" | "memory" | "connections";

const TABS: { id: Tab; label: string; hint: string }[] = [
  { id: "overview", label: "Overview", hint: "01" },
  { id: "chat", label: "Chat", hint: "02" },
  { id: "tasks", label: "Tasks", hint: "03" },
  { id: "memory", label: "Memory", hint: "04" },
  { id: "connections", label: "Connections", hint: "05" },
];

export function Sidebar({
  active,
  onSelect,
}: {
  active: Tab;
  onSelect: (tab: Tab) => void;
}) {
  return (
    <aside className="flex h-full w-[220px] shrink-0 flex-col border-r border-border bg-surface">
      <div className="border-b border-border px-5 py-5">
        <div className="font-display text-lg font-bold tracking-tight text-text">CoreAI</div>
        <div className="mt-0.5 font-mono text-[11px] text-muted">agent console</div>
      </div>

      <nav className="flex-1 px-3 py-4">
        {TABS.map((tab) => {
          const isActive = tab.id === active;
          return (
            <button
              key={tab.id}
              onClick={() => onSelect(tab.id)}
              className={`mb-1 flex w-full items-center justify-between rounded-sm px-3 py-2 text-left text-sm transition-colors ${
                isActive
                  ? "bg-surface2 text-text"
                  : "text-muted hover:bg-surface2/60 hover:text-text"
              }`}
            >
              <span>{tab.label}</span>
              <span className="font-mono text-[10px] text-muted">{tab.hint}</span>
            </button>
          );
        })}
      </nav>

      <div className="border-t border-border px-5 py-4 font-mono text-[10px] text-muted">
        Flask :5000 · Proxy :3001
      </div>
    </aside>
  );
}
