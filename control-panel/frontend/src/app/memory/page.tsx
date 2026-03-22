import { AppLayout } from "@/components/layout/app-layout";

export default function MemoryPage() {
  return (
    <AppLayout>
      <div className="space-y-4">
        <h2 className="text-xl font-semibold">Memória</h2>
        <p className="text-[hsl(var(--muted-foreground))] text-sm">
          Gerenciamento de memória dos agentes — em construção
        </p>
      </div>
    </AppLayout>
  );
}
