"use client";

import { useEffect, useState } from "react";
import { api, Task } from "@/lib/api";

const THREAD_ID = "frontend-tasks";

export function TasksPanel() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [title, setTitle] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const load = async () => {
    try {
      const { tasks } = await api.listTasks(THREAD_ID);
      setTasks(tasks);
      setError(null);
    } catch {
      setError("Couldn't load tasks. Is the backend running?");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    load();
  }, []);

  const addTask = async () => {
    const t = title.trim();
    if (!t) return;
    setTitle("");
    try {
      await api.addTask(THREAD_ID, t);
      load();
    } catch {
      setError("Couldn't add the task.");
    }
  };

  const complete = async (id: number) => {
    setTasks((prev) => prev.filter((t) => t.id !== id)); // optimistic
    try {
      await api.completeTask(id);
    } catch {
      load(); // revert on failure
    }
  };

  const remove = async (id: number) => {
    setTasks((prev) => prev.filter((t) => t.id !== id));
    try {
      await api.deleteTask(id);
    } catch {
      load();
    }
  };

  return (
    <div className="max-w-2xl">
      <h1 className="font-display text-xl font-bold text-text">Tasks</h1>
      <p className="mt-1 text-sm text-muted">
        Backed by Postgres via the Task Agent — persists across restarts.
      </p>

      <div className="mt-6 flex gap-2">
        <input
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && addTask()}
          placeholder="Add a task…"
          className="flex-1 rounded-md border border-border bg-surface px-3 py-2.5 text-sm text-text placeholder:text-muted focus:border-accent/50"
        />
        <button
          onClick={addTask}
          className="rounded-md bg-accent px-4 py-2.5 text-sm font-medium text-base"
        >
          Add
        </button>
      </div>

      {error && <div className="mt-3 font-mono text-xs text-err">{error}</div>}

      <div className="mt-6 rounded-md border border-border bg-surface">
        {loading ? (
          <div className="px-4 py-6 text-center text-sm text-muted">Loading…</div>
        ) : tasks.length === 0 ? (
          <div className="px-4 py-6 text-center text-sm text-muted">No open tasks.</div>
        ) : (
          <div className="divide-y divide-border">
            {tasks.map((task) => (
              <div key={task.id} className="flex items-center justify-between px-4 py-3">
                <div className="flex items-center gap-3">
                  <button
                    onClick={() => complete(task.id)}
                    aria-label="Mark complete"
                    className="h-4 w-4 rounded-sm border border-border hover:border-accent"
                  />
                  <span className="text-sm text-text">{task.title}</span>
                </div>
                <button
                  onClick={() => remove(task.id)}
                  className="font-mono text-xs text-muted hover:text-err"
                >
                  delete
                </button>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
