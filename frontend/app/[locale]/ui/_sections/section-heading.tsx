type SectionHeadingProps = {
  title: string;
  heading_number: string;
};

export default function SectionHeading({ title, heading_number }: SectionHeadingProps) {
  return (
    <h1
      id="results-heading"
      className="text-black flex flex-col text-center justify-center md:flex-row md:justify-start md:text-left items-center gap-8 mb-8"
    >
      <span className="w-[50vw] h-[12vh] md:w-[23vw] md:h-[20vh] text-numbers md:text-numbers-desktop bg-pink-3 text-black rounded-[1.6rem] inline-flex items-center justify-center ">
        {heading_number}.
      </span>
      {title.toUpperCase()}
    </h1>
  );
}
