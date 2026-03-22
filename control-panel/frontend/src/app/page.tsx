import { AppLayout } from "@/components/layout/app-layout";

export default function DashboardPage() {
  return (
    <AppLayout>
      <div className="space-y-4">
        <h2 className="text-xl font-semibold">Dashboard</h2>
        <p className="text-[hsl(var(--muted-foreground))] text-sm">
          ClawDevs AI Control Panel — carregando...
        </p>
      </div>
    </AppLayout>
  );
}
