export function Stats({ tokens, queries }: { tokens: number; queries: number }) {
  const avg = queries ? Math.round(tokens / queries) : 0;
  const items = [
    { label: "Tokens spent", value: tokens },
    { label: "Queries run", value: queries },
    { label: "Avg tokens / query", value: avg },
  ];
  return (
    <div className="grid grid-cols-3 gap-3">
      {items.map((it) => (
        <div
          key={it.label}
          className="rounded-xl border border-neutral-800 bg-gradient-to-b from-neutral-900 to-neutral-950 px-4 py-3"
        >
          <div className="font-mono text-2xl font-bold text-neutral-100">{it.value}</div>
          <div className="text-[11px] uppercase tracking-wide text-neutral-500">{it.label}</div>
        </div>
      ))}
    </div>
  );
}
