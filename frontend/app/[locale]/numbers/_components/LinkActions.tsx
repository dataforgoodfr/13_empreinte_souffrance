'use client';

import { useState } from 'react';

type Props = {
  externalUrl: string;
  downloadImageUrl: string;
  downloadEmbedUrl?: string;
};

export default function LinkActions({ externalUrl, downloadImageUrl, downloadEmbedUrl }: Readonly<Props>) {
  const [copied, setCopied] = useState(false);

  const handleCopyEmbed = async () => {
    if (!downloadEmbedUrl) return;
    const iframeCode = `<iframe src="${downloadEmbedUrl}" width="500" height="700"></iframe>`;
    await navigator.clipboard.writeText(iframeCode);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="flex flex-row gap-4 items-center">
      <a
        href={externalUrl}
        rel="noopener noreferrer"
        className="px-4 py-2 underline bg-grey/80 text-black hover:bg-black/70 hover:text-white transition w-1/2 cursor-pointer"
      >
        Voir la source
      </a>
      <a
        href={downloadImageUrl}
        download
        className="px-4 py-2 underline bg-grey/80 text-black hover:bg-black/70 hover:text-white transition w-1/2 cursor-pointer"
      >
        Télécharger l'image
      </a>
      {downloadEmbedUrl && (
        <button
          onClick={handleCopyEmbed}
          className="px-4 py-2 underline bg-grey/80 text-black hover:bg-black/70 hover:text-white transition w-1/2 cursor-pointer text-left"
        >
          {copied ? 'Copié !' : "Copier l'iframe"}
        </button>
      )}
    </div>
  );
}
