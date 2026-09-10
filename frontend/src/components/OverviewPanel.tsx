"use client";

import { useEffect, useState } from "react";
import { api, AgentStatus } from "@/lib/api";
import { StatusDot } from "./StatusDot";

type DashboardData = {
  totalConversations: number;
  activeAgents: number;
  apiCallsToday: number;
  successRate: number;
  recentActivity: { time: string; action: string; type: string }[];
};

export function OverviewPanel() {
  const [agents, setAgents] = useState<AgentStatus[] | null>(null);
  const [dashboard, setDashboard] = useState<DashboardData | null>(null);
  const [error, setError] = useState<string | null>(null);

  const load = async () => {
    try {
      const [health, dash] = await Promise.all([api.health(), api.dashboard()]);
      setAgents(health.agents);
      setDashboard(dash as DashboardData);
      setError(null);
    } catch {
      setError(
        "Can't reach the backend. Make sure the Flask API (port 5000) and the proxy (port 3001) are running."
      );
    }
  };

  useEffect(() => {
    load();
    const interval = setInterval(load, 8000);
    return () => clearInterval(interval);
  }, []);

  if (error) {
    return (
      <div className="max-w-lg rounded-md border border-err/40 bg-err/10 p-4 font-mono text-sm text-err">
        {error}
      </div>
    );
  }

  const stats = [
    { label: "Active agents", value: dashboard?.activeAgents ?? "—" },
    { label: "Conversations", value: dashboard?.totalConversations ?? "—" },
    { label: "API calls today", value: dashboard?.apiCallsToday ?? "—" },
    { label: "Success rate", value: dashboard ? `${dashboard.successRate}%` : "—" },
  ];

  return (
    <div className="max-w-4xl">
      <h1 className="font-display text-xl font-bold text-text">Overview</h1>
      <p className="mt-1 text-sm text-muted">Live status pulled from the Flask API every few seconds.</p>

      <div className="mt-6 grid grid-cols-2 gap-3 sm:grid-cols-4">
        {stats.map((s) => (
          <div key={s.label} className="rounded-md border border-border bg-surface p-4">
            <div className="font-mono text-2xl font-medium text-text">{s.value}</div>
            <div className="mt-1 text-xs text-muted">{s.label}</div>
          </div>
        ))}
      </div>

      <div className="mt-8">
        <h2 className="mb-3 text-sm font-medium text-muted">Agents</h2>
        <div className="divide-y divide-border rounded-md border border-border bg-surface">
          {agents?.map((agent) => (
            <div key={agent.name} className="flex items-center justify-between px-4 py-3">
              <div>
                <div className="text-sm text-text">{agent.name}</div>
                <div className="mt-0.5 text-xs text-muted">{agent.description}</div>
              </div>
              <StatusDot
                state={agent.status === "idle" ? "idle" : agent.status === "error" ? "err" : "ok"}
                label={agent.status}
              />
            </div>
          ))}
        </div>
      </div>

      <div className="mt-8">
        <h2 className="mb-3 text-sm font-medium text-muted">Recent activity</h2>
        <div className="rounded-md border border-border bg-surface">
          {dashboard?.recentActivity?.length ? (
            <div className="divide-y divide-border">
              {dashboard.recentActivity.map((item, i) => (
                <div key={i} className="flex items-center justify-between px-4 py-2.5 text-sm">
                  <span className="text-text">{item.action}</span>
                  <span className="font-mono text-xs text-muted">{item.time}</span>
                </div>
              ))}
            </div>
          ) : (
            <div className="px-4 py-6 text-center text-sm text-muted">
              Nothing yet — send a message from the Chat tab.
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
