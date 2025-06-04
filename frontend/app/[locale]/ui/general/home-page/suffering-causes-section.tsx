import SectionHeading from '@/app/[locale]/ui/general/home-page/elements/section-heading';
import BoltIcon from '@/app/[locale]/ui/icons/BoltIcon';

export default function SufferingCausesSection() {
  return (
    <section className="py-16 bg-white text-[#3b0a0a]">
      <div className="max-w-screen-xl mx-auto px-4">
        <SectionHeading title={'De quoi souffrent les poules en cage ?'} heading_number="1" />

        <div className="flex flex-col md:flex-row justify-center gap-6 relative mt-12">
          <div className="flex flex-col justify-between  md:w-1/3">
            <SufferingBox title="Blessures dues au picage">
              Stressées, les poules s’arrachent les plumes entre elles, causant blessures, infections... et parfois la
              mort par cannibalisme.
            </SufferingBox>
            <SufferingBox title="Fracture du bréchet" className="md:ml-10">
              L’os de la poitrine se fracture souvent à cause de l’ostéoporose liée à la ponte intensive : c’est leur
              plus grande source de douleur.
            </SufferingBox>
          </div>

          <div className="hidden md:flex justify-center relative">
            <img src="suffering_logo.PNG" alt="Silhouette d'une poule" className="w-full " />
          </div>

          <div className="flex flex-col justify-between gap-6 text-left md:w-1/3">
            <SufferingBox title="Restriction de mouvement" className="md:-ml-48 md:-mt-10">
              En cage, les poules ne peuvent ni étendre leurs ailes, ni se retourner : un inconfort permanent, loin de
              tout comportement naturel.
            </SufferingBox>
            <SufferingBox title="Peur et stress">
              Avant l’abattoir, les poules sont capturées, entassées sans eau ni nourriture, et soumises à une peur
              extrême.
            </SufferingBox>
            <SufferingBox title="Privation de comportements naturels" className="md:-ml-24">
              Privées de nidification et d’exploration, les poules vivent une frustration intense, incapables de
              répondre à leurs besoins naturels.
            </SufferingBox>
          </div>
        </div>

        <div className=" max-w-xl  md:w-1/3 mx-auto">
          <SufferingBox title="Péritonite de l’œuf">
            Cette inflammation, due à des débris d’œuf dans l’abdomen, est la maladie la plus fréquente et mortelle chez
            les poules pondeuses.
          </SufferingBox>
        </div>

        <div className="mt-8 text-center text-xs font-semibold tracking-wider uppercase">
          + 24 autres sources de douleur
        </div>
      </div>
    </section>
  );
}

interface SufferingBoxProps {
  title: string;
  children: React.ReactNode;
  className?: string;
}

// 🔁 Composant réutilisable pour chaque cause
function SufferingBox({ title, children, className = '' }: SufferingBoxProps) {
  return (
    <div className={`${className} max-w-xs`}>
      <div className="flex items-center gap-2 mb-2">
        <BoltIcon />
        <h3 className="font-bold uppercase">{title}</h3>
      </div>
      <p className="text-sm font-medium">{children}</p>
    </div>
  );
}
