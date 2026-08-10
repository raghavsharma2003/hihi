export default function Eyebrow({ children }: { children: React.ReactNode }) {
  return (
    <p className="font-mono text-12 font-medium uppercase tracking-[0.14em] text-current">
      {children}
    </p>
  );
}
