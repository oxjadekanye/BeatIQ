import type { Metadata, Viewport } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { siteUrl } from "@/lib/site";

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-geist-sans",
  display: "swap",
});

export const metadata: Metadata = {
  metadataBase: new URL(siteUrl),
  title: {
    default: "BeatIQ — Find Every Beat",
    template: "%s | BeatIQ",
  },
  description:
    "BeatIQ is a music discovery, streaming, playlist, and audio platform. Find every beat — from discovery to your personal library.",
  keywords: [
    "BeatIQ",
    "music",
    "streaming",
    "playlists",
    "discovery",
    "audio",
    "Aurexus Group",
  ],
  authors: [{ name: "Aurexus Group Ltd" }],
  openGraph: {
    type: "website",
    locale: "en_GB",
    url: siteUrl,
    siteName: "BeatIQ",
    title: "BeatIQ — Find Every Beat",
    description:
      "Discover, organise, and stream music with BeatIQ. Official site for the BeatIQ app and legal information.",
  },
  twitter: {
    card: "summary_large_image",
    title: "BeatIQ — Find Every Beat",
    description:
      "Discover, organise, and stream music with BeatIQ. Official site for the BeatIQ app and legal information.",
  },
  robots: {
    index: true,
    follow: true,
  },
};

export const viewport: Viewport = {
  themeColor: "#0a0610",
  width: "device-width",
  initialScale: 1,
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en-GB" className={inter.variable}>
        <body className="min-h-screen font-sans">{children}</body>
      </html>
  );
}
