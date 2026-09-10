"use client";

import { useState } from "react";
import { Sidebar, Tab } from "@/components/Sidebar";
import { TopBar } from "@/components/TopBar";
import { OverviewPanel } from "@/components/OverviewPanel";
import { ChatPanel } from "@/components/ChatPanel";
import { TasksPanel } from "@/components/TasksPanel";
import { MemoryPanel } from "@/components/MemoryPanel";
import { ConnectionsPanel } from "@/components/ConnectionsPanel";

export default function Home() {
  const [tab, setTab] = useState<Tab>("overview");

  return (
    <div className="flex h-screen bg-base">
      <Sidebar active={tab} onSelect={setTab} />
      <div className="flex flex-1 flex-col overflow-hidden">
        <TopBar />
        <main className="flex-1 overflow-y-auto px-8 py-8">
          {tab === "overview" && <OverviewPanel />}
          {tab === "chat" && <ChatPanel />}
          {tab === "tasks" && <TasksPanel />}
          {tab === "memory" && <MemoryPanel />}
          {tab === "connections" && <ConnectionsPanel />}
        </main>
      </div>
    </div>
  );
}
