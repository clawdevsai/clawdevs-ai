"use client";

type StatCardProps = {
  label: string;
  value: string | number;
  tone?: "default" | "accent" | "success" | "warning";
};

const tones = {
  default: "text-slate-900",
  accent: "text-indigo-600",
  success: "text-emerald-600",
  warning: "text-amber-500"
};

export function StatCard({ label, value, tone = "default" }: StatCardProps) {
  return (
    <div className="bg-white border border-slate-200 shadow-sm rounded-2xl p-5 card-hover">
      <div className="text-[11px] font-semibold uppercase tracking-[0.24em] text-slate-500">{label}</div>
      <div className={`mt-3 text-3xl font-bold ${tones[tone]}`}>{value}</div>
    </div>
  );
}
