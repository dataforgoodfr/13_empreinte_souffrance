type Props = {
  className?: string;
}

export default async function Supermarkets({className}: Props) {
  return (
      <div className={`relative aspect-video w-full h-full ${className}`}>
        <iframe
          title="Engagements hors cage des Supermarchés"
          width="1200"
          height="675"
          className="absolute inset-0 w-full h-full"
          src="https://view.genially.com/690cda4cc4779c62de2f6c1d"
          allowFullScreen
          allow="fullscreen"
        />
      </div>
  );
}
