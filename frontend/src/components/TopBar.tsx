"use client";

import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { StatusDot } from "./StatusDot";

export function TopBar() {
  const [online, setOnline] = useState<boolean | null>(null);

  useEffect(() => {
    const check = () => api.health().then(() => setOnline(true)).catch(() => setOnline(false));
    check();
    const interval = setInterval(check, 6000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="flex h-12 items-center justify-end border-b border-border bg-base px-6">
      <StatusDot
        state={online === null ? "idle" : online ? "ok" : "err"}
        label={online === null ? "checking…" : online ? "backend online" : "backend unreachable"}
      />
    </div>
  );
}
