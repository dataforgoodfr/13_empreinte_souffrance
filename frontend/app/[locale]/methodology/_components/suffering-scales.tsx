interface SufferingScalesProps {
  agony_duration_text: string;
  pain_duration_text: string;
  suffering_duration_text: string;
  discomfort_duration_text: string;
}

export default function SufferingScales({
  agony_duration_text,
  pain_duration_text,
  suffering_duration_text,
  discomfort_duration_text,
}: SufferingScalesProps) {
  return (
    <>
      <p className="flex justify-center items-center w-full p-1 text-center text-pink-1 bg-brown">
        {agony_duration_text}
      </p>
      <p className="flex justify-center items-center w-full p-1 text-center bg-pink-3">{pain_duration_text}</p>
      <p className="flex justify-center items-center w-full p-1 text-center bg-pink-2">{suffering_duration_text}</p>
      <p className="flex justify-center items-center w-full p-1 text-center bg-pink-1">{discomfort_duration_text}</p>
    </>
  );
}
