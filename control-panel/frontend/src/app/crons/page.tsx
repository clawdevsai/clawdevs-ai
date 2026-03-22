import { AppLayout } from "@/components/layout/app-layout";

export default function CronsPage() {
  return (
    <AppLayout>
      <div className="space-y-4">
        <h2 className="text-xl font-semibold">Crons</h2>
        <p className="text-[hsl(var(--muted-foreground))] text-sm">
          Jobs agendados — em construção
        </p>
      </div>
    </AppLayout>
  );
}
