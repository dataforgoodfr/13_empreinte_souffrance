import Link from 'next/link';
import SectionHeading from '@/app/[locale]/ui/general/home-page/elements/section-heading';

export default async function PainEquationSection() {
  return (
    <section aria-labelledby="pain-equation-title" className="py-16 px-4 md:px-8 bg-white text-gray-900">
      <SectionHeading title={"L'ÉQUATION DE LA DOULEUR"} heading_number="2" />

      {/* CONTENEUR GLOBAL UNIFIÉ */}
      <div className="max-w-screen-xl mx-auto px-4">
        {/* ÉQUATION */}
        {/* ÉQUATION */}
        <div className="mt-8 w-full flex flex-col md:grid md:grid-cols-3 items-center text-center border border-black divide-y md:divide-y-0 md:divide-x divide-black font-extrabold text-xl">
          <div className="py-2 w-full">DURÉE</div>
          <div className="py-2 w-full">X INTENSITÉ</div>
          <div className="py-2 w-full">= FARDEAU DE DOULEUR</div>
        </div>

        {/* TEXTE EXPLICATIF */}
        <p className="mt-12 mb-12 max-w-2xl mx-auto text-base text-center sm:text-lg">
          Comment ça marche ? Pour chaque source de douleur (fracture, infection, etc.), les chercheurs estiment combien
          de temps les poules passent dans un état d’inconfort, de douleur, de souffrance et d’agonie.
        </p>

        {/* ÉTAPES DE LA DOULEUR */}
        <section aria-labelledby="pain-stages" className="mb-12">
          <h3 id="pain-stages" className="sr-only">
            Étapes de la douleur
          </h3>

          <div className="grid grid-cols-1 md:grid-cols-4 ">
            <article className="bg-red-100 p-4 border border-red-200">
              <h4 className="font-bold uppercase mb-4 mt-4">Inconfort</h4>
              <p className="text-sm font-medium">
                Inconfort léger, sans impact sur le comportement. Comparable à une démangeaison ou des chaussures qui
                frottent légèrement.
              </p>
            </article>
            <article className="bg-red-200 p-4 border border-red-300">
              <h4 className="font-bold uppercase mb-4 mt-4">Douleur</h4>
              <p className="text-sm font-medium">
                Douleur persistante, altérant les comportements sans les empêcher. Semblable à un mal de tête ou un mal
                de dos chronique.
              </p>
            </article>
            <article className="bg-red-300 p-4 border border-red-400">
              <h4 className="font-bold uppercase mb-4 mt-4">Souffrance</h4>
              <p className="text-sm font-medium">
                Douleur constante, prioritaire sur tout. Réduit l’activité, le bien-être, l’attention. Semblable à une
                migraine ou une fracture.
              </p>
            </article>
            <article className="bg-red-900 text-white p-4 border border-red-700">
              <h4 className="font-bold uppercase mb-4 mt-4">Agonie</h4>
              <p className="text-sm font-medium">
                Douleur extrême, insupportable même brièvement. Provoque cris, tremblements. Comparable à une souffrance
                que l’on ne peut endurer.
              </p>
            </article>
          </div>

          {/* BOUTON */}
          <footer className="text-center mt-8">
            <Link
              href="/"
              className="inline-block border-[0.1px] border-[#ff7f7f] py-3 px-6 text-lg hover:bg-gray-100 transition w-full font-mono text-[#3b0a0a] tracking-wider"
              aria-label="Découvrir la méthodologie en détail"
            >
              DÉCOUVRIR LA MÉTHODOLOGIE EN DÉTAIL
            </Link>
          </footer>
        </section>
      </div>
    </section>
  );
}
