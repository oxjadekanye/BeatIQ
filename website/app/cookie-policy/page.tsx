import type { Metadata } from "next";
import { CookiePolicyDocument } from "@/components/legal/CookiePolicyDocument";
import { SiteFooter } from "@/components/SiteFooter";
import { SiteHeader } from "@/components/SiteHeader";
import { siteUrl } from "@/lib/site";

export const metadata: Metadata = {
  title: "Cookie Policy",
  description:
    "BeatIQ cookie policy — how we use cookies and similar technologies. Contact admin@beatiq.co.uk.",
  alternates: { canonical: `${siteUrl}/cookie-policy` },
  openGraph: {
    title: "BeatIQ Cookie Policy",
    url: `${siteUrl}/cookie-policy`,
  },
};

export default function CookiePolicyPage() {
  return (
    <>
      <SiteHeader />
      <CookiePolicyDocument />
      <SiteFooter />
    </>
  );
}
