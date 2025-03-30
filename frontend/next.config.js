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
};

module.exports = nextConfig;
