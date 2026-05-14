import type { Metadata } from "next";
import { PrivacyPolicyDocument } from "@/components/legal/PrivacyPolicyDocument";
import { SiteFooter } from "@/components/SiteFooter";
import { SiteHeader } from "@/components/SiteHeader";
import { siteUrl } from "@/lib/site";

export const metadata: Metadata = {
  title: "Privacy Policy",
  description:
    "BeatIQ privacy policy — how we collect, use, and protect your information. Contact admin@beatiq.co.uk.",
  alternates: { canonical: `${siteUrl}/privacy-policy` },
  openGraph: {
    title: "BeatIQ Privacy Policy",
    url: `${siteUrl}/privacy-policy`,
  },
};

export default function PrivacyPolicyPage() {
  return (
    <>
      <SiteHeader />
      <PrivacyPolicyDocument />
      <SiteFooter />
    </>
  );
}
