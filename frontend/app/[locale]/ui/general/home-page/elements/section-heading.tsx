type SectionHeadingProps = {
  title: string;
  heading_number: string;
};

export default function SectionHeading({ title, heading_number }: SectionHeadingProps) {
  return (
    <h2
      id="results-heading"
      className="text-3xl sm:text-4xl font-extrabold tracking-wide text-[#3b0a0a] mb-10 text-center flex justify-start items-center gap-3"
    >
      <span className="text-[40px] text-black bg-[#ff7f7f] text-[#3b0a0a] w-18 h-13 rounded-full flex items-center justify-center shadow-[4px_4px_0_#000] inline-flex">
        {heading_number}.
      </span>
      {title.toUpperCase()}
    </h2>
  );
}
