import type { MetadataRoute } from "next";
import { siteUrl } from "@/lib/site";

export default function sitemap(): MetadataRoute.Sitemap {
  const lastModified = new Date("2026-05-14");
  const paths = [
    "",
    "/privacy-policy",
    "/terms-and-conditions",
    "/cookie-policy",
  ];
  return paths.map((path) => ({
    url: `${siteUrl}${path}`,
    lastModified,
    changeFrequency: path === "" ? "monthly" : "yearly",
    priority: path === "" ? 1 : 0.7,
  }));
}
