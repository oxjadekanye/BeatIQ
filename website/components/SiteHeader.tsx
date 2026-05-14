import Image from "next/image";
import Link from "next/link";

const nav = [
  { href: "/#discover", label: "Discover" },
  { href: "/#download", label: "App" },
  { href: "/privacy-policy/", label: "Privacy" },
] as const;

export function SiteHeader() {
  return (
    <header className="sticky top-0 z-50 border-b border-violet-500/15 bg-beatiq-midnight/90 backdrop-blur-md">
      <div className="mx-auto flex max-w-5xl items-center justify-between gap-4 px-4 py-3 sm:px-6 lg:px-8">
        <Link href="/" className="flex items-center gap-2">
          <Image
            src="/brand-logo.png"
            alt="BeatIQ"
            width={40}
            height={40}
            className="h-9 w-9 object-contain"
            priority
          />
          <span className="text-lg font-bold tracking-tight text-white">
            BeatIQ
          </span>
        </Link>
        <nav className="hidden items-center gap-6 sm:flex" aria-label="Main">
          {nav.map((item) => (
            <Link
              key={item.href}
              href={item.href}
              className="text-sm font-medium text-zinc-300 transition hover:text-beatiq-accent"
            >
              {item.label}
            </Link>
          ))}
        </nav>
        <Link
          href="/#download"
          className="rounded-full bg-violet-600 px-4 py-2 text-sm font-semibold text-white shadow-lg shadow-violet-900/40 transition hover:bg-violet-500 sm:hidden"
        >
          Get the app
        </Link>
      </div>
    </header>
  );
}
