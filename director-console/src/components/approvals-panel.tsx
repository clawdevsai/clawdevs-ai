"use client";

import { useEffect, useMemo, useState, useTransition } from "react";

import type { ApprovalItem } from "@/lib/server/types";

type ApprovalsPanelProps = {
  pendingItems: ApprovalItem[];
  onChanged?: () => void;
};

type ActionState = {
  message: string | null;
  isPending: boolean;
};

export function ApprovalsPanel({ pendingItems, onChanged }: ApprovalsPanelProps) {
  const [pending, setPending] = useState(pendingItems);
  const [actionState, setActionState] = useState<ActionState>({ message: null, isPending: false });
  const [isTransitionPending, startTransition] = useTransition();

  const isBusy = actionState.isPending || isTransitionPending;

  const grouped = useMemo(() => pending, [pending]);

  useEffect(() => {
    setPending(pendingItems);
  }, [pendingItems]);

  const refresh = async () => {
    const response = await fetch("/api/approvals");
    const payload = (await response.json()) as { pending?: ApprovalItem[]; error?: string };
    if (!response.ok) {
      setActionState({ message: payload.error ?? "approvals_error", isPending: false });
      return;
    }
    setPending(payload.pending ?? []);
    setActionState({ message: null, isPending: false });
    onChanged?.();
  };

  const runAction = (action: "approve" | "deny", key: string) => {
    setActionState({ message: null, isPending: true });
    startTransition(async () => {
      const response = await fetch("/api/approvals", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ action, key })
      });
      const payload = (await response.json()) as { error?: string };
      if (!response.ok) {
        setActionState({ message: payload.error ?? "approvals_action_error", isPending: false });
        return;
      }
      await refresh();
    });
  };

  return (
    <div className="bg-white shadow-sm border border-slate-200 rounded-3xl p-6">
      <div className="mb-6">
        <h2 className="text-xl font-bold text-slate-900 tracking-tight">Aprovacoes pendentes</h2>
        <p className="mt-1 text-sm text-slate-500 font-medium">
          Itens aguardando autorizacao humana (UI e Telegram).
        </p>
      </div>
      {grouped.length === 0 ? (
        <div className="rounded-2xl border border-dashed border-slate-300 bg-slate-50 flex items-center justify-center p-8">
          <p className="text-sm font-semibold text-slate-400">Sem aprovacoes pendentes no momento.</p>
        </div>
      ) : (
        <div className="space-y-4">
          {grouped.map((item) => (
            <div key={item.key} className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
              <div className="flex flex-wrap items-center justify-between gap-3 text-xs font-semibold text-slate-500 uppercase tracking-wider">
                <span>{item.requestedAt}</span>
                <span className="rounded-full border border-slate-200 bg-slate-50 px-3 py-1 shadow-sm text-slate-700">{item.source}</span>
              </div>
              <div className="mt-3 text-sm font-bold text-slate-900">{item.issueId}</div>
              <div className="mt-3 text-sm text-slate-600 font-medium whitespace-pre-wrap leading-relaxed bg-slate-50 border border-slate-100 rounded-xl p-3">{item.directive}</div>
              <div className="mt-5 flex flex-wrap gap-3">
                <button
                  type="button"
                  disabled={isBusy}
                  onClick={() => runAction("approve", item.key)}
                  className="rounded-full bg-indigo-600 px-6 py-2 text-sm font-semibold text-white transition hover:bg-indigo-700 shadow-sm shadow-indigo-200 disabled:cursor-not-allowed disabled:opacity-50"
                >
                  Aprovar
                </button>
                <button
                  type="button"
                  disabled={isBusy}
                  onClick={() => runAction("deny", item.key)}
                  className="rounded-full border border-slate-300 bg-white px-6 py-2 text-sm font-semibold text-slate-700 transition hover:bg-slate-50 hover:text-slate-900 disabled:cursor-not-allowed disabled:opacity-50 shadow-sm"
                >
                  Recusar
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
      <div className="mt-5 text-sm font-medium text-slate-500">
        {isBusy ? "Processando..." : actionState.message ?? "Aprovacoes disparam cmd:strategy."}
      </div>
    </div>
  );
}
