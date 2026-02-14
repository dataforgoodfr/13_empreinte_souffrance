type Props = {
  externalUrl: string;
  downloadImageUrl: string;
};

export default function LinkActions({ externalUrl, downloadImageUrl }: Readonly<Props>) {
  return (
    <div className="flex flex-row gap-4 items-center">
      <a
        href={externalUrl}
        
        rel="noopener noreferrer"
        className="px-4 py-2 underline bg-grey/80 text-black hover:bg-black/70 hover:text-white transition w-1/2"
      >
        Voir la source
      </a>
      <a
        href={downloadImageUrl}
        download
        className="px-4 py-2 underline bg-grey/80 text-black hover:bg-black/70 hover:text-white transition w-1/2"
      >
        Télécharger l'image
      </a>
    </div>
  );
}