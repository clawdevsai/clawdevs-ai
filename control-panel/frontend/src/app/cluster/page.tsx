import { AppLayout } from "@/components/layout/app-layout";

export default function ClusterPage() {
  return (
    <AppLayout>
      <div className="space-y-4">
        <h2 className="text-xl font-semibold">Cluster</h2>
        <p className="text-[hsl(var(--muted-foreground))] text-sm">
          Status do cluster — em construção
        </p>
      </div>
    </AppLayout>
  );
}
