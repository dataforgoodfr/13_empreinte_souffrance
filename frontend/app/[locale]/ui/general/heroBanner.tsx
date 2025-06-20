
// Déclaration du type des props attendues par le composant
type HeroBannerProps = {
  title: string;
}

// Composant fonctionnel qui reçoit un titre en prop
export default function HeroBanner({ title }: HeroBannerProps) {
  return (
    <h1 className=" uppercase pt-28 pb-20 text-3xl sm:text-5xl font-bold tracking-wide text-[#3C1212] text-center">
      {title}
    </h1>
  );
}