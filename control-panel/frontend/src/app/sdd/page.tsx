import { AppLayout } from "@/components/layout/app-layout";

export default function SddPage() {
  return (
    <AppLayout>
      <div className="space-y-4">
        <h2 className="text-xl font-semibold">SDD</h2>
        <p className="text-[hsl(var(--muted-foreground))] text-sm">
          Software Design Documents — em construção
        </p>
      </div>
    </AppLayout>
  );
}
