import type { NextConfig } from "next";

const backend = process.env.BACKEND_URL ?? "http://clawdevs-panel-backend:8000";

const nextConfig: NextConfig = {
  output: "standalone",
  images: {
    unoptimized: true,
  },
  async rewrites() {
    return [
      {
        source: "/api/ws/:path*",
        destination: `${backend}/ws/:path*`,
      },
      {
        source: "/api/:path*",
        destination: `${backend}/:path*`,
      },
    ];
  },
};

export default nextConfig;
