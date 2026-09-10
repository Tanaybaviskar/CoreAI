"use client";

import { useEffect, useState } from "react";
import { api, AuthStatus } from "@/lib/api";
import { StatusDot } from "./StatusDot";

export function ConnectionsPanel() {
  const [status, setStatus] = useState<AuthStatus | null>(null);
  const [error, setError] = useState<string | null>(null);

  const load = async () => {
    try {
      setStatus(await api.authStatus());
      setError(null);
    } catch {
      setError("Couldn't reach the backend's auth endpoint.");
    }
  };

  useEffect(() => {
    load();
  }, []);

  return (
    <div className="max-w-xl">
      <h1 className="font-display text-xl font-bold text-text">Connections</h1>
      <p className="mt-1 text-sm text-muted">Google Calendar and Gmail, via OAuth.</p>

      <div className="mt-6 rounded-md border border-border bg-surface p-5">
        <div className="flex items-center justify-between">
          <div>
            <div className="text-sm text-text">Google Workspace</div>
            <div className="mt-1 text-xs text-muted">
              {status?.authenticated ? status.user?.email || "Connected" : "Calendar and Gmail access"}
            </div>
          </div>
          <StatusDot
            state={status?.authenticated ? "ok" : "idle"}
            label={status?.authenticated ? "connected" : "not connected"}
          />
        </div>

        {!status?.authenticated && (
          <a
            href={api.loginUrl()}
            target="_blank"
            rel="noreferrer"
            className="mt-4 inline-block rounded-md bg-accent px-4 py-2 text-sm font-medium text-base"
          >
            Connect Google account
          </a>
        )}

        {error && <div className="mt-3 font-mono text-xs text-err">{error}</div>}
      </div>

      <p className="mt-4 text-xs text-muted">
        The connect link opens the Flask backend&apos;s OAuth flow directly (not through the proxy),
        since the redirect needs to land back on port 5000.
      </p>
    </div>
  );
}
