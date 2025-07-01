type SectionHeadingProps = {
  title: string;
  heading_number: string;
};

export default function SectionHeading({ title, heading_number }: SectionHeadingProps) {
  return (
    <h2
      id="results-heading"
      className="text-3xl sm:text-4xl font-extrabold tracking-wide text-[#3b0a0a] mb-10  flex justify-start items-center gap-3 p-2 m-2"
    >
      <span className=" p-6 text-[40px] bg-[#ff7f7f] text-[#3b0a0a] w-18 h-13 rounded-full  items-center justify-center shadow-[4px_4px_0_#000] inline-flex">
        {heading_number}.
      </span>
      {title.toUpperCase()}
    </h2>
  );
}
