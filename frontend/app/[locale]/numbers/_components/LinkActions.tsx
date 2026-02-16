'use client';

type Props = {
  externalUrl: string;
  downloadImageUrl: string;
  downloadEmbedUrl?: string;
};

export default function LinkActions({ externalUrl, downloadImageUrl, downloadEmbedUrl }: Readonly<Props>) {
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
        <a
          href={downloadEmbedUrl}
          target="_blank"
          className="px-4 py-2 underline bg-grey/80 text-black hover:bg-black/70 hover:text-white transition w-1/2 cursor-pointer text-left"
        >
          Exporter la carte
        </a>
      )}
    </div>
  );
}
