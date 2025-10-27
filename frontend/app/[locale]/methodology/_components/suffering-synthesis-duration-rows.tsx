interface SufferingSynthesisDurationRowsProps {
  agony_duration_text: string;
  pain_duration_text: string;
  suffering_duration_text: string;
  discomfort_duration_text: string;
}

export default function SufferingSynthesisDurationRows({
  agony_duration_text,
  pain_duration_text,
  suffering_duration_text,
  discomfort_duration_text,
}: SufferingSynthesisDurationRowsProps) {
  return (
    <>
      <p className="w-full h-1/4 p-1 text-center text-pink-2 bg-brown">{agony_duration_text}</p>
      <p className="w-full h-1/4 p-1 text-center bg-pink-3">{pain_duration_text}</p>
      <p className="w-full h-1/4 p-1 text-center bg-pink-2">{suffering_duration_text}</p>
      <p className="w-full h-1/4 p-1 text-center bg-pink-1">{discomfort_duration_text}</p>
    </>
  );
}
