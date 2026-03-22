import { AppLayout } from "@/components/layout/app-layout";

export default function AgentsPage() {
  return (
    <AppLayout>
      <div className="space-y-4">
        <h2 className="text-xl font-semibold">Agentes</h2>
        <p className="text-[hsl(var(--muted-foreground))] text-sm">
          Lista de agentes — em construção
        </p>
      </div>
    </AppLayout>
  );
}
