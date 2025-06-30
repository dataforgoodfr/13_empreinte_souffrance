import QuantifySufferingByPain from '@/app/[locale]/methodology/quantify-suffering-by-pain';
import SectionHeading from '../ui/general/home-page/elements/section-heading';
import Link from 'next/link';


const listOfPain = [
  'fracture du bréchet',
  'péritonite de l’oeuf',
  'restriction de la possibilité de nidifier',
  'fracture du bréchet',
  'péritonite de l’oeuf',
  'restriction de la possibilité de nidifier',
  'fracture du bréchet',
  'péritonite de l’oeuf',
  'restriction de la possibilité de nidifier',
  'fracture du bréchet',
  'péritonite de l’oeuf',
  'restriction de la possibilité de nidifier',
  'fracture du bréchet',
  'péritonite de l’oeuf',
  'restriction de la possibilité de nidifier',
  'fracture du bréchet',
  'péritonite de l’oeuf',
  'restriction de la possibilité de nidifier',
  'fracture du bréchet',
  'péritonite de l’oeuf',
  'restriction de la possibilité de nidifier',
  'fracture du bréchet',
  'péritonite de l’oeuf',
  'restriction de la possibilité de nidifier',
  'etc',
];

export default function MethodDetailsSection() {
  return (
    <>
      <div className="w-full max-w-screen-xl mx-auto mt-12 text-[#3C1212]">
        <SectionHeading title="La méthode en détail" heading_number="2" />
        <div className="flex flex-col p-6  sm:p-20 lg:p-0 md:w-2/3  lg:m-auto">
          <h2 className="text-2xl font-extrabold mb-4 uppercase ">
            2.1 Lister toutes les sources de douleur pour les poules{' '}
          </h2>
          <p className="text-md mb-6">De quoi souffrent les poules ?</p>
          <p className="text-md mb-6">
            Une revue approfondie de la littérature scientifique est menée pour identifier les principales sources de
            douleur pour les poules en élevage, et à quelle fréquence elles surviennent selon le mode d’élevage. Il peut
            s’agir de douleurs physiques (fractures, blessures cutanées, infections...) ou psychologiques (peur,
            restriction des besoins comportementaux...).Au total, ce sont xx sources de douleurs qui ont été
            répertoriées et étudiées par le Welfare Footprint Institute, grâce à l'étude de yy articles.
          </p>
        </div>
        <div className=" mx-auto ">
          <article className="p-6">
            <h3 className="uppercase font-bold ">Quelques douleurs psychologiques</h3>
            <hr className="border-1  border-[#FF7B7B] my-2" />
            <div className="flex flex-col sm:flex-row m-auto gap-3 mt-4 ">
              <div className="">
                <img src="/agony.PNG" alt="" />
                <p>a</p>
                <p>a</p>
              </div>
              <div>
                <img src="/agony.PNG" alt="" />
                <p>a</p>
                <p>a</p>
              </div>
              <div>
                <img src="/agony.PNG" alt="" />
                <p>a</p>
                <p>a</p>
              </div>
            </div>
          </article>
          <article className=" p-6">
            <h3 className="uppercase font-bold ">Quelques douleurs physiques</h3>
            <hr className="border-1  border-[#FF7B7B] my-2" />
            <div className="flex flex-col sm:flex-row m-auto gap-3 mt-4 ">
              <div className="">
                <img src="/agony.PNG" alt="" />
                <p>a</p>
                <p>a</p>
              </div>
              <div>
                <img src="/agony.PNG" alt="" />
                <p>a</p>
                <p>a</p>
              </div>
              <div>
                <img src="/agony.PNG" alt="" />
                <p>a</p>
                <p>a</p>
              </div>
            </div>
          </article>
          <article className=" p-6">
            <h3 className="uppercase font-bold ">Liste de toutes les sources de douleur </h3>
            <hr className="border-1  border-[#FF7B7B] my-2" />
            <div className="mt-4 grid grid-cols-2 w-full text-center font-mono uppercase font-bold gap-1 text-xs md:text-sm ">
              {listOfPain.map((pain, index) => (
                <p key={index} className="bg-[#FF7B7B] p-2 transition-all duration-200">
                  {pain}
                </p>
              ))}{' '}
            </div>
            <Link
              className="text-sm mt-1 bg-[#FFC3C3] font-mono font-bold py-4 px-6 rounded-full shadow-[4px_4px_0_#000] w-full block cursor-pointer text-center  transition-all duration-200 hover:bg-[#FF7B7B]  "
              href="/methodology"
            >
              Voir toutes les sources
            </Link>
          </article>
        </div>
      </div>

      <QuantifySufferingByPain />
    </>
  );
}
