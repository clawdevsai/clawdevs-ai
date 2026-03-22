import { AppLayout } from "@/components/layout/app-layout";

export default function SettingsPage() {
  return (
    <AppLayout>
      <div className="space-y-4">
        <h2 className="text-xl font-semibold">Settings</h2>
        <p className="text-[hsl(var(--muted-foreground))] text-sm">
          Configurações do sistema — em construção
        </p>
      </div>
    </AppLayout>
  );
}
