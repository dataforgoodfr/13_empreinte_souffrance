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
        source: '/embed/:path*',
        headers: [
          {
            key: 'X-Frame-Options',
            value: 'ALLOWALL', // Permet l'iframe uniquement depuis votre propre domaine
            // Utilisez 'ALLOWALL' ou supprimez cette ligne pour autoriser tous les domaines
          },
          {
            key: 'Content-Security-Policy',
            value: "frame-ancestors *", // Autorise uniquement votre domaine
            // Pour autoriser des domaines spécifiques : "frame-ancestors 'self' https://exemple.com https://autredomaine.com"
            // Pour autoriser tous les domaines : "frame-ancestors *"
          },
        ],
      },
    ];
  },
};

module.exports = nextConfig;
