// Components uses as title bloc for step column components

interface StepColumnHeaderProps {
  title: string;
  number: number | string;
}

async function StepColumnHeader({ title, number }: StepColumnHeaderProps) {
  return (
    <div className="text-center rounded-[10px] mb-[10px] bg-pink-2 py-3 px-2">
      <h3>{number}</h3>
      <h4>{title}</h4>
    </div>
  );
}

export default StepColumnHeader;
