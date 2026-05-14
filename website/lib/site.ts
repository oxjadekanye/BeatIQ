/**
 * Canonical public site URL. Override in Vercel with NEXT_PUBLIC_SITE_URL if needed.
 */
export const siteUrl =
  (process.env.NEXT_PUBLIC_SITE_URL || "https://www.beatiq.co.uk").replace(
    /\/$/,
    "",
  );

export const company = {
  name: "Aurexus Group Ltd",
  lines: [
    "Unit A, 82 James Carter Road",
    "Mildenhall",
    "Bury St Edmunds",
    "Suffolk",
    "IP28 7DE",
    "United Kingdom",
  ] as const,
  email: "admin@beatiq.co.uk",
};
