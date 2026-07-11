import { CATEGORY_META, modelBadge } from "../assets";

export function CategoryPill({ category }: { category: string }) {
  const meta = CATEGORY_META[category] || { icon: "❔", color: "#9AA0AE" };
  return (
    <span
      className="inline-flex items-center gap-1.5 rounded-full px-3 py-1 text-xs font-semibold border"
      style={{
        background: `${meta.color}18`,
        color: meta.color,
        borderColor: `${meta.color}40`,
      }}
    >
      <span>{meta.icon}</span>
      {category}
    </span>
  );
}

export function ModelBadge({ source }: { source: string }) {
  const m = modelBadge(source);
  return (
    <div className="flex items-center gap-2">
      <div
        className="flex h-6 w-6 shrink-0 items-center justify-center overflow-hidden rounded-full ring-2 ring-black/30"
        style={{ background: m.bg }}
      >
        {m.icon}
      </div>
      <span className="text-sm text-neutral-300">{m.name}</span>
    </div>
  );
}

export function Chip({ children }: { children: React.ReactNode }) {
  return (
    <span className="inline-block rounded-full border border-neutral-800 bg-neutral-900 px-2.5 py-1 text-xs font-medium text-neutral-400">
      {children}
    </span>
  );
}
