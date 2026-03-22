import { AppLayout } from "@/components/layout/app-layout";

export default function TasksPage() {
  return (
    <AppLayout>
      <div className="space-y-4">
        <h2 className="text-xl font-semibold">Tarefas</h2>
        <p className="text-[hsl(var(--muted-foreground))] text-sm">
          Gerenciamento de tarefas — em construção
        </p>
      </div>
    </AppLayout>
  );
}
