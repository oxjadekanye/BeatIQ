import type { Metadata } from "next";
import { TermsDocument } from "@/components/legal/TermsDocument";
import { SiteFooter } from "@/components/SiteFooter";
import { SiteHeader } from "@/components/SiteHeader";
import { siteUrl } from "@/lib/site";

export const metadata: Metadata = {
  title: "Terms and Conditions",
  description:
    "BeatIQ terms and conditions — rules for using the BeatIQ platform. Contact admin@beatiq.co.uk.",
  alternates: { canonical: `${siteUrl}/terms-and-conditions` },
  openGraph: {
    title: "BeatIQ Terms and Conditions",
    url: `${siteUrl}/terms-and-conditions`,
  },
};

export default function TermsPage() {
  return (
    <>
      <SiteHeader />
      <TermsDocument />
      <SiteFooter />
    </>
  );
}
