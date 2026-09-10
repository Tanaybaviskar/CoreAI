export function StatusDot({
  state,
  label,
}: {
  state: "ok" | "warn" | "err" | "idle";
  label?: string;
}) {
  const color = {
    ok: "bg-ok",
    warn: "bg-warn",
    err: "bg-err",
    idle: "bg-muted",
  }[state];

  return (
    <span className="inline-flex items-center gap-2 font-mono text-xs text-muted">
      <span className={`h-1.5 w-1.5 rounded-full ${color} ${state === "ok" ? "status-dot-live" : ""}`} />
      {label}
    </span>
  );
}
