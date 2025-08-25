interface SufferingSynthesisDurationTableProps {
  agony_duration_text: string;
  pain_duration_text: string;
  suffering_duration_text: string;
  discomfort_duration_text: string;
}

export default function SufferingSynthesisDurationTable({
  agony_duration_text,
  pain_duration_text,
  suffering_duration_text,
  discomfort_duration_text,
}: SufferingSynthesisDurationTableProps) {
  return (
    <div className="w-full grid grid-cols-2 grid-rows-2 normal-case text-center">
      <div className="flex justify-center items-center bg-brown light-text p-2">{agony_duration_text}</div>
      <div className="flex justify-center items-center bg-pink-3 dark-text p-2">{pain_duration_text}</div>
      <div className="flex justify-center items-center bg-pink-2 dark-text p-2">{suffering_duration_text}</div>
      <div className="flex justify-center items-center bg-pink-1 dark-text p-2">{discomfort_duration_text}</div>
    </div>
  );
}
