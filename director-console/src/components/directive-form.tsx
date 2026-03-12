"use client";

import { useState, useTransition } from "react";

type DirectiveFormProps = {
  onCompleted?: () => void;
};

export function DirectiveForm({ onCompleted }: DirectiveFormProps) {
  const [directive, setDirective] = useState("");
  const [requiresApproval, setRequiresApproval] = useState(true);
  const [message, setMessage] = useState<string | null>(null);
  const [isPending, startTransition] = useTransition();

  return (
    <form
      className="bg-white shadow-sm border border-slate-200 rounded-3xl p-6"
      onSubmit={(event) => {
        event.preventDefault();
        setMessage(null);
        startTransition(async () => {
          const endpoint = requiresApproval ? "/api/approvals" : "/api/directives";
          const payload = requiresApproval
            ? { action: "create", directive }
            : { directive };
          const response = await fetch(endpoint, {
            method: "POST",
            headers: {
              "Content-Type": "application/json"
            },
            body: JSON.stringify(payload)
          });
          const result = (await response.json()) as { issueId?: string; error?: string };
          if (!response.ok) {
            setMessage(`Erro: ${result.error ?? "directive_error"}`);
            return;
          }
          setMessage(
            requiresApproval
              ? `Diretiva aguardando aprovação. Ref ${result.issueId}`
              : `Diretiva enviada com sucesso. Ref ${result.issueId}`
          );
          setDirective("");
          onCompleted?.();
        });
      }}
    >
      <div className="mb-4 flex items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-semibold text-slate-900">Console do diretor</h2>
          <p className="mt-1 text-sm text-slate-500">
            Envie uma demanda unica para o stream `cmd:strategy`.
          </p>
        </div>
      </div>
      <textarea
        value={directive}
        onChange={(event) => setDirective(event.target.value)}
        placeholder="Exemplo: criar backlog inicial para um CRUD de usuarios em Go, com auth JWT e persistencia Postgres..."
        className="min-h-40 w-full rounded-2xl border border-slate-300 bg-slate-50 px-4 py-3 text-sm text-slate-900 outline-none transition focus:bg-white focus:border-indigo-500 focus:ring-4 focus:ring-indigo-500/10 placeholder-slate-400"
      />
      <label className="mt-4 flex items-center gap-3 text-sm text-slate-600 font-medium">
        <input
          type="checkbox"
          checked={requiresApproval}
          onChange={(event) => setRequiresApproval(event.target.checked)}
          className="h-4 w-4 rounded border-slate-300 text-indigo-600 focus:ring-indigo-600"
        />
        Requer aprovacao humana antes de iniciar o pipeline.
      </label>
      <div className="mt-5 flex items-center justify-between gap-4">
        <p className="text-sm font-medium text-slate-500">{message ?? "O envio gera um item para o PO consumir."}</p>
        <button
          type="submit"
          disabled={isPending || !directive.trim()}
          className="rounded-full bg-indigo-600 px-6 py-2.5 text-sm font-semibold text-white shadow-sm shadow-indigo-200 transition hover:bg-indigo-700 disabled:cursor-not-allowed disabled:opacity-50"
        >
          {isPending ? "Enviando..." : "Enviar diretiva"}
        </button>
      </div>
    </form>
  );
}
