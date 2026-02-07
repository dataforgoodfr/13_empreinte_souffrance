/** @type {import('next').NextConfig} */
const nextConfig = {
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: 'images.openfoodfacts.org',
        port: '',
        pathname: '/images/products/**',
      },
    ],
  },

  async headers() {
    return [
      {
        // Default: prevent iframe embedding for all routes
        source: '/:path*',
        headers: [
          {
            key: 'X-Frame-Options',
            value: 'SAMEORIGIN',
          },
          {
            key: 'Content-Security-Policy',
            value: "frame-ancestors 'self'",
          },
        ],
      },
      {
        // allow iframe embedding for /embed/* routes
        source: '/embed/:path*',
        headers: [
          {
            key: 'X-Frame-Options',
            value: '',
          },
          {
            key: 'Content-Security-Policy',
            value: "frame-ancestors *; img-src 'self' https://*.openstreetmap.fr https://*.tile.openstreetmap.fr data:; style-src 'self' 'unsafe-inline'",
          },
        ],
      },
    ];
  },
};

module.exports = nextConfig;
