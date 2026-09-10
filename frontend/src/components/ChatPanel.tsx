"use client";

import { useEffect, useRef, useState } from "react";
import { api } from "@/lib/api";

type Message = { role: "user" | "assistant"; content: string };

const SUGGESTIONS = ["add task: review the JD", "list tasks", "what's the weather?"];

export function ChatPanel() {
  const [threadId, setThreadId] = useState("");
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [sending, setSending] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    setThreadId(crypto.randomUUID());
  }, []);

  useEffect(() => {
    scrollRef.current?.scrollTo({ top: scrollRef.current.scrollHeight, behavior: "smooth" });
  }, [messages]);

  const send = async () => {
    const text = input.trim();
    if (!text || sending || !threadId) return;

    setMessages((prev) => [...prev, { role: "user", content: text }]);
    setInput("");
    setSending(true);
    setError(null);

    setMessages((prev) => [...prev, { role: "assistant", content: "" }]);

    try {
      await api.streamChat(text, threadId, (chunk) => {
        setMessages((prev) => {
          const next = [...prev];
          next[next.length - 1] = {
            role: "assistant",
            content: next[next.length - 1].content + chunk,
          };
          return next;
        });
      });
    } catch {
      setError("Message failed to send. Check that the proxy (port 3001) and backend (port 5000) are running.");
      setMessages((prev) => prev.slice(0, -1));
    } finally {
      setSending(false);
    }
  };

  return (
    <div className="flex h-full max-w-3xl flex-col">
      <div className="border-b border-border pb-4">
        <h1 className="font-display text-xl font-bold text-text">Chat</h1>
        <p className="mt-1 text-sm text-muted">
          Talk to the supervisor agent directly. Thread{" "}
          <span className="font-mono text-xs">{threadId ? threadId.slice(0, 8) : "…"}</span>
        </p>
      </div>

      <div ref={scrollRef} className="flex-1 space-y-4 overflow-y-auto py-6">
        {messages.length === 0 && (
          <div className="flex flex-wrap gap-2">
            {SUGGESTIONS.map((s) => (
              <button
                key={s}
                onClick={() => setInput(s)}
                className="rounded-sm border border-border px-3 py-1.5 text-xs text-muted hover:border-accent/50 hover:text-text"
              >
                {s}
              </button>
            ))}
          </div>
        )}

        {messages.map((m, i) => (
          <div key={i} className={`flex ${m.role === "user" ? "justify-end" : "justify-start"}`}>
            <div
              className={`max-w-[75%] rounded-md px-4 py-2.5 text-sm leading-relaxed ${
                m.role === "user"
                  ? "bg-accent text-base"
                  : "border border-border bg-surface text-text"
              }`}
            >
              {m.content || (sending && i === messages.length - 1 ? "…" : "")}
            </div>
          </div>
        ))}

        {error && <div className="font-mono text-xs text-err">{error}</div>}
      </div>

      <div className="border-t border-border pt-4">
        <div className="flex gap-2">
          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && send()}
            placeholder="Message the agents…"
            className="flex-1 rounded-md border border-border bg-surface px-3 py-2.5 text-sm text-text placeholder:text-muted focus:border-accent/50"
          />
          <button
            onClick={send}
            disabled={sending || !input.trim()}
            className="rounded-md bg-accent px-4 py-2.5 text-sm font-medium text-base disabled:opacity-40"
          >
            Send
          </button>
        </div>
      </div>
    </div>
  );
}
