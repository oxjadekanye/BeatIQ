import Image from "next/image";
import Link from "next/link";
import { SiteFooter } from "@/components/SiteFooter";
import { SiteHeader } from "@/components/SiteHeader";
import { company } from "@/lib/site";

export default function HomePage() {
  return (
    <>
      <SiteHeader />
      <main>
        <section className="relative overflow-hidden border-b border-violet-500/20">
          <div
            className="pointer-events-none absolute inset-0 opacity-40"
            aria-hidden
            style={{
              background:
                "radial-gradient(ellipse 80% 60% at 50% -20%, rgba(184,85,255,0.35), transparent), radial-gradient(ellipse 60% 50% at 100% 50%, rgba(0,212,255,0.12), transparent)",
            }}
          />
          <div className="relative mx-auto max-w-3xl px-4 pb-16 pt-12 text-center sm:px-6 sm:pb-24 sm:pt-16 lg:px-8">
            <div className="mx-auto mb-6 flex justify-center sm:mb-8">
              <Image
                src="/brand-logo.png"
                alt="BeatIQ logo"
                width={112}
                height={112}
                className="h-24 w-24 object-contain sm:h-28 sm:w-28"
                priority
              />
            </div>
            <h1 className="hero-gradient text-4xl font-extrabold tracking-tight sm:text-5xl md:text-6xl">
              BeatIQ
            </h1>
            <p className="mx-auto mt-3 max-w-xl text-lg font-medium text-beatiq-accent sm:text-2xl">
              Find Every Beat
            </p>
            <p className="mx-auto mt-5 max-w-lg text-sm leading-relaxed text-zinc-400 sm:text-base">
              Search, discover, and organise your music — a dark, focused experience with
              purple accents, built for phones and desktops alike.
            </p>
            <div
              id="discover"
              className="mx-auto mt-8 max-w-md rounded-2xl border border-violet-500/25 bg-beatiq-violet/40 px-4 py-4 text-left sm:px-5"
            >
              <p className="text-xs font-semibold uppercase tracking-wide text-beatiq-accent">
                Discover
              </p>
              <p className="mt-1 text-sm text-zinc-300">
                Explore artists, genres, and playlists — keep every track you care about one
                search away.
              </p>
            </div>
            <div className="mt-8 flex flex-col items-stretch gap-3 sm:flex-row sm:justify-center">
              <Link
                href="/#download"
                className="rounded-full bg-violet-600 px-8 py-3 text-center text-sm font-semibold text-white shadow-lg shadow-violet-900/40 transition hover:bg-violet-500"
              >
                Download the app
              </Link>
              <Link
                href="/privacy-policy/"
                className="rounded-full border border-violet-500/40 px-6 py-3 text-center text-sm font-medium text-zinc-200 transition hover:border-beatiq-accent hover:text-white"
              >
                Privacy Policy
              </Link>
            </div>
          </div>
        </section>

        <section
          id="download"
          className="border-t border-violet-500/20 bg-beatiq-violet/35 py-14 sm:py-20"
        >
          <div className="mx-auto max-w-2xl px-4 text-center sm:px-6">
            <h2 className="text-xl font-bold text-white sm:text-2xl">Get BeatIQ</h2>
            <p className="mt-2 text-sm text-zinc-400 sm:text-base">
              The mobile app is coming to Google Play. This page will link to the store when
              available.
            </p>
            <div className="mt-6 rounded-2xl border border-dashed border-violet-500/35 bg-beatiq-midnight/50 px-5 py-8">
              <p className="text-sm font-medium text-zinc-300">Play Store — coming soon</p>
            </div>
          </div>
        </section>

        <section className="mx-auto max-w-2xl px-4 py-14 text-center sm:px-6">
          <h2 className="text-lg font-semibold text-white sm:text-xl">Contact</h2>
          <p className="mt-3 text-sm text-zinc-400">
            BeatIQ is a product of{" "}
            <span className="text-zinc-200">{company.name}</span>
          </p>
          <address className="mt-3 text-sm not-italic leading-relaxed text-zinc-500">
            {company.lines.map((line) => (
              <span key={line} className="block">
                {line}
              </span>
            ))}
          </address>
          <p className="mt-4 text-sm text-zinc-400">
            <a
              href={`mailto:${company.email}`}
              className="font-medium text-beatiq-accent hover:text-violet-200"
            >
              {company.email}
            </a>
          </p>
        </section>
      </main>
      <SiteFooter />
    </>
  );
}
