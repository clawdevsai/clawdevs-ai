"use client";

import type { ActivityItem } from "@/lib/server/types";

type ActivityFeedProps = {
  items: ActivityItem[];
};

export function ActivityFeed({ items }: ActivityFeedProps) {
  return (
    <div className="bg-white shadow-sm border border-slate-200 rounded-3xl p-6 relative overflow-hidden">
      <div className="mb-6 relative z-10">
        <h2 className="text-xl font-bold text-slate-900 tracking-tight">Feed de atividade</h2>
        <p className="mt-1 text-sm text-slate-500 font-medium">Eventos combinados dos streams principais e orquestracao.</p>
      </div>
      <div className="space-y-4 relative z-10">
        {items.length === 0 ? (
          <p className="text-sm font-medium text-slate-500">Nenhum evento recente encontrado.</p>
        ) : (
          items.map((item) => (
            <div key={`${item.stream}-${item.id}`} className="rounded-2xl border border-slate-100 bg-slate-50 px-5 py-4 transition duration-200 hover:bg-slate-100/60 hover:shadow-sm">
              <div className="flex flex-wrap items-center justify-between gap-3 text-xs font-semibold text-slate-500 uppercase tracking-wider">
                <span>{item.timestamp}</span>
                <span className="rounded-full border border-slate-200 bg-white px-3 py-1 shadow-sm text-slate-700">{item.agent}</span>
              </div>
              <div className="mt-3 text-sm font-bold text-slate-800">{item.eventName}</div>
              <div className="mt-2 flex flex-wrap items-center gap-2 text-[11px] font-semibold uppercase tracking-wider text-slate-500">
                <span className="bg-slate-200/50 text-slate-600 px-2 py-1 rounded-md">Stream: {item.stream}</span>
                {item.issueId ? <span className="bg-indigo-50 text-indigo-600 px-2 py-1 rounded-md border border-indigo-100 flex items-center gap-1">Issue: {item.issueId}</span> : null}
              </div>
              {item.summary ? <div className="mt-3 text-sm text-slate-600 leading-relaxed border-l-2 border-indigo-300 pl-3 bg-white/50 py-1">{item.summary}</div> : null}
            </div>
          ))
        )}
      </div>
    </div>
  );
}
