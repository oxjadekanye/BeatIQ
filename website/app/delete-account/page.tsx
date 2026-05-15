import type { Metadata } from "next";
import { DeleteAccountDocument } from "@/components/legal/DeleteAccountDocument";
import { SiteFooter } from "@/components/SiteFooter";
import { SiteHeader } from "@/components/SiteHeader";
import { siteUrl } from "@/lib/site";

export const metadata: Metadata = {
  title: "Delete Your BeatIQ Account",
  description:
    "Request deletion of your BeatIQ account and personal data. Email admin@beatiq.co.uk from your registered address.",
  alternates: { canonical: `${siteUrl}/delete-account/` },
  openGraph: {
    title: "Delete Your BeatIQ Account — BeatIQ",
    url: `${siteUrl}/delete-account/`,
  },
};

export default function DeleteAccountPage() {
  return (
    <>
      <SiteHeader />
      <DeleteAccountDocument />
      <SiteFooter />
    </>
  );
}
