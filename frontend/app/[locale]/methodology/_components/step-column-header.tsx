// Components uses as title bloc for step column components

interface StepColumnHeaderProps {
  title: string;
  number: number | string;
}

async function StepColumnHeader({ title, number }: StepColumnHeaderProps) {
  return (
    <div className="text-center rounded-[10px] mb-[10px] font-extrabold font-mono bg-pink-2 py-3 px-2">
      <h2 className="font-extrabold">{number}</h2>
      <h4 className="">{title}</h4>
    </div>
  );
}

export default StepColumnHeader;
