"use client";

import { useEffect, useState } from "react";
import { api, MemoryItem } from "@/lib/api";

export function MemoryPanel() {
  const [items, setItems] = useState<MemoryItem[]>([]);
  const [key, setKey] = useState("");
  const [value, setValue] = useState("");
  const [error, setError] = useState<string | null>(null);

  const load = async () => {
    try {
      const { memory_items } = await api.listMemory();
      setItems(memory_items);
      setError(null);
    } catch {
      setError("Couldn't load memory. Is the backend running?");
    }
  };

  useEffect(() => {
    load();
  }, []);

  const add = async () => {
    if (!key.trim() || !value.trim()) return;
    try {
      await api.addMemory(key.trim(), value.trim());
      setKey("");
      setValue("");
      load();
    } catch {
      setError("Couldn't save that item.");
    }
  };

  return (
    <div className="max-w-2xl">
      <h1 className="font-display text-xl font-bold text-text">Memory</h1>
      <p className="mt-1 text-sm text-muted">Persisted key/value context the agents can draw on.</p>

      <div className="mt-6 flex gap-2">
        <input
          value={key}
          onChange={(e) => setKey(e.target.value)}
          placeholder="Key"
          className="w-1/3 rounded-md border border-border bg-surface px-3 py-2.5 text-sm text-text placeholder:text-muted focus:border-accent/50"
        />
        <input
          value={value}
          onChange={(e) => setValue(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && add()}
          placeholder="Value"
          className="flex-1 rounded-md border border-border bg-surface px-3 py-2.5 text-sm text-text placeholder:text-muted focus:border-accent/50"
        />
        <button onClick={add} className="rounded-md bg-accent px-4 py-2.5 text-sm font-medium text-base">
          Save
        </button>
      </div>

      {error && <div className="mt-3 font-mono text-xs text-err">{error}</div>}

      <div className="mt-6 rounded-md border border-border bg-surface">
        {items.length === 0 ? (
          <div className="px-4 py-6 text-center text-sm text-muted">No memory items yet.</div>
        ) : (
          <div className="divide-y divide-border">
            {items.map((item) => (
              <div key={item.id} className="flex items-center justify-between px-4 py-3">
                <span className="font-mono text-xs text-muted">{item.key}</span>
                <span className="text-sm text-text">{item.value}</span>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
