import { Sidebar } from './Sidebar';

interface PageLayoutProps {
  children: React.ReactNode;
}

export function PageLayout({ children }: PageLayoutProps) {
  return (
    <div className="flex min-h-screen bg-bg">
      <Sidebar />
      <main className="ml-60 flex-1 p-6 lg:p-8 max-w-[1400px]">
        {children}
      </main>
    </div>
  );
}
