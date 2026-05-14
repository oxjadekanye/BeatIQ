/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  /** Static HTML export so Vercel can deploy from `website/out` when the Git root is the monorepo. */
  output: "export",
  /** Folder-based routes — reliable on static hosts (e.g. `/privacy-policy/index.html`). */
  trailingSlash: true,
  images: {
    unoptimized: true,
  },
};

export default nextConfig;
