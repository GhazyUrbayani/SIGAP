interface HeaderProps {
  title: string;
  subtitle?: string;
}

export function Header({ title, subtitle }: HeaderProps) {
  return (
    <header className="mb-6">
      <h1 className="font-display text-2xl font-bold text-text-primary">
        {title}
      </h1>
      {subtitle && (
        <p className="text-sm text-text-secondary mt-1">{subtitle}</p>
      )}
    </header>
  );
}
