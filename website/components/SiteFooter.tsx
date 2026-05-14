import Link from "next/link";
import { company } from "@/lib/site";

const legal = [
  { href: "/privacy-policy", label: "Privacy Policy" },
  { href: "/terms-and-conditions", label: "Terms and Conditions" },
  { href: "/cookie-policy", label: "Cookie Policy" },
] as const;

export function SiteFooter() {
  return (
    <footer className="border-t border-violet-500/20 bg-beatiq-violet/80">
      <div className="mx-auto max-w-5xl px-4 py-12 sm:px-6 lg:px-8">
        <div className="grid gap-10 sm:grid-cols-2">
          <div>
            <p className="text-sm font-semibold uppercase tracking-wider text-beatiq-accent">
              BeatIQ
            </p>
            <p className="mt-2 text-sm text-zinc-400">
              BeatIQ is a product of{" "}
              <span className="text-zinc-200">{company.name}</span>
            </p>
            <address className="mt-3 not-italic text-sm leading-relaxed text-zinc-400">
              {company.lines.map((line) => (
                <span key={line} className="block">
                  {line}
                </span>
              ))}
            </address>
          </div>
          <div>
            <p className="text-sm font-semibold text-zinc-200">Legal</p>
            <ul className="mt-3 space-y-2">
              {legal.map((item) => (
                <li key={item.href}>
                  <Link
                    href={item.href}
                    className="text-sm text-beatiq-accent hover:text-violet-200"
                  >
                    {item.label}
                  </Link>
                </li>
              ))}
            </ul>
            <p className="mt-6 text-sm text-zinc-400">
              Contact:{" "}
              <a
                href={`mailto:${company.email}`}
                className="text-beatiq-accent hover:text-violet-200"
              >
                {company.email}
              </a>
            </p>
          </div>
        </div>
        <p className="mt-10 text-center text-xs text-zinc-500">
          © {new Date().getFullYear()} {company.name}. All rights reserved.
        </p>
      </div>
    </footer>
  );
}
