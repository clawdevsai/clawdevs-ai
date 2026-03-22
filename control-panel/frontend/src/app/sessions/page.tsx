import { AppLayout } from "@/components/layout/app-layout";

export default function SessionsPage() {
  return (
    <AppLayout>
      <div className="space-y-4">
        <h2 className="text-xl font-semibold">Sessões</h2>
        <p className="text-[hsl(var(--muted-foreground))] text-sm">
          Sessões ativas — em construção
        </p>
      </div>
    </AppLayout>
  );
}
