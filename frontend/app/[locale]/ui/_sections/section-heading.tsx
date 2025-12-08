type SectionHeadingProps = {
  title: string;
  heading_number: string;
};

export default function SectionHeading({ title, heading_number }: SectionHeadingProps) {
  return (
    <h2
      id="results-heading"
      className="flex flex-col text-center justify-center items-center md:flex-row md:justify-start md:text-left gap-8 mb-8 text-black"
    >
      <span className="flex items-center justify-center p-[8px_84px_8px_84px] text-numbers md:text-numbers-desktop bg-pink-3 text-black rounded-[1.6rem]  ">
        {heading_number}.
      </span>
      {title.toUpperCase()}
    </h2>
  );
}
