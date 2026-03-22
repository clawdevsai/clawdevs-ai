import { AppLayout } from "@/components/layout/app-layout";

export default function ApprovalsPage() {
  return (
    <AppLayout>
      <div className="space-y-4">
        <h2 className="text-xl font-semibold">Aprovações</h2>
        <p className="text-[hsl(var(--muted-foreground))] text-sm">
          Fila de aprovações — em construção
        </p>
      </div>
    </AppLayout>
  );
}
