import Image from "next/image";
import Link from "next/link";
import { SiteFooter } from "@/components/SiteFooter";
import { SiteHeader } from "@/components/SiteHeader";
import { company } from "@/lib/site";

const features = [
  {
    title: "Discover",
    body: "Explore genres, artists, and moods tailored to how you listen — from trending picks to deep cuts.",
  },
  {
    title: "Your library",
    body: "Organise tracks, playlists, and favourites so every beat you love stays one tap away.",
  },
  {
    title: "Playlists & more",
    body: "Build playlists, revisit downloads, and keep your listening flow consistent across sessions.",
  },
  {
    title: "Built for listeners",
    body: "A focused, modern experience with performance and clarity at the centre of the design.",
  },
] as const;

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
          <div className="relative mx-auto max-w-5xl px-4 pb-20 pt-14 text-center sm:px-6 sm:pb-28 sm:pt-20 lg:px-8">
            <div className="mx-auto mb-8 flex justify-center">
              <Image
                src="/brand-logo.png"
                alt="BeatIQ logo"
                width={120}
                height={120}
                className="h-28 w-28 object-contain sm:h-32 sm:w-32"
                priority
              />
            </div>
            <h1 className="hero-gradient text-4xl font-extrabold tracking-tight sm:text-6xl">
              BeatIQ
            </h1>
            <p className="mx-auto mt-4 max-w-2xl text-lg text-beatiq-accent sm:text-2xl">
              Find Every Beat
            </p>
            <p className="mx-auto mt-6 max-w-2xl text-base text-zinc-400 sm:text-lg">
              Music discovery, streaming, playlists, and audio — designed to help you
              discover, organise, stream, and enjoy the sounds you care about.
            </p>
            <div className="mt-10 flex flex-wrap items-center justify-center gap-4">
              <Link
                href="/#download"
                className="rounded-full bg-violet-600 px-8 py-3 text-sm font-semibold text-white shadow-xl shadow-violet-900/50 transition hover:bg-violet-500"
              >
                Get the BeatIQ app
              </Link>
              <Link
                href="/privacy-policy"
                className="rounded-full border border-violet-500/40 px-6 py-3 text-sm font-medium text-zinc-200 transition hover:border-beatiq-accent hover:text-white"
              >
                Privacy
              </Link>
            </div>
          </div>
        </section>

        <section
          id="features"
          className="mx-auto max-w-5xl px-4 py-16 sm:px-6 sm:py-24 lg:px-8"
        >
          <h2 className="text-center text-2xl font-bold text-white sm:text-3xl">
            Why BeatIQ
          </h2>
          <p className="mx-auto mt-3 max-w-2xl text-center text-zinc-400">
            A modern listening companion with a dark, refined interface and purple-forward
            accents — built for clarity on every screen size.
          </p>
          <div className="mt-12 grid gap-6 sm:grid-cols-2">
            {features.map((f) => (
              <div
                key={f.title}
                className="rounded-2xl border border-violet-500/20 bg-beatiq-violet/50 p-6 shadow-lg shadow-black/20"
              >
                <h3 className="text-lg font-semibold text-beatiq-accent">{f.title}</h3>
                <p className="mt-2 text-sm text-zinc-300">{f.body}</p>
              </div>
            ))}
          </div>
        </section>

        <section
          id="download"
          className="border-y border-violet-500/20 bg-beatiq-violet/40 py-16 sm:py-20"
        >
          <div className="mx-auto max-w-3xl px-4 text-center sm:px-6 lg:px-8">
            <h2 className="text-2xl font-bold text-white sm:text-3xl">Download BeatIQ</h2>
            <p className="mt-3 text-zinc-400">
              The BeatIQ mobile app will be available on the Google Play Store. This
              section will be updated with the official store link when publication is
              complete.
            </p>
            <div className="mt-8 rounded-2xl border border-dashed border-violet-500/40 bg-beatiq-midnight/60 px-6 py-10">
              <p className="text-sm font-medium text-zinc-300">Play Store — coming soon</p>
              <p className="mt-2 text-xs text-zinc-500">
                No download is required to read our policies on this site.
              </p>
            </div>
          </div>
        </section>

        <section className="mx-auto max-w-3xl px-4 py-16 sm:px-6 lg:px-8">
          <h2 className="text-center text-2xl font-bold text-white">Contact &amp; company</h2>
          <p className="mt-4 text-center text-sm text-zinc-400">
            BeatIQ is a product of{" "}
            <span className="text-zinc-200">{company.name}</span>
          </p>
          <address className="mt-4 text-center text-sm not-italic leading-relaxed text-zinc-400">
            {company.lines.map((line) => (
              <span key={line} className="block">
                {line}
              </span>
            ))}
          </address>
          <p className="mt-4 text-center text-sm text-zinc-400">
            Email:{" "}
            <a
              href={`mailto:${company.email}`}
              className="text-beatiq-accent hover:text-violet-200"
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
