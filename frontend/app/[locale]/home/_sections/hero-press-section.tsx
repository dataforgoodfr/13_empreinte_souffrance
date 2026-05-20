import ArrowDown from '@/app/[locale]/ui/_logo/ArrowDown';
import { getI18n } from '@/locales/server';
import Image from 'next/image';
import Link from 'next/link';
import SectionTitle from '../_components/section-title';

export default async function HeroPressSection() {
  const t = await getI18n();

  return (
    <header className="relative flex flex-col items-center justify-between w-full overflow-hidden bg-gradient-to-b from-pink-2 to-pink-3">
      <div className="mt-15 md:mt-10">
        <div className="flex flex-wrap justify-center gap-6">
          <Link
            href="https://photos.app.goo.gl/jdmkpY5PHqsgYzPh9"
            target="_blank"
            className="w-[18%] md:w-[18%] lg:w-fit flex justify-center"
          >
            <Image
              src="/press-logos/France_2.png"
              width={120}
              height={60}
              alt="Logo France 2"
              className="object-contain h-10"
            />
          </Link>

          <Link
            href="https://photos.app.goo.gl/eJ5qrFGbo4FAtRoh6"
            target="_blank"
            className="w-[18%] md:w-[18%] lg:w-fit flex justify-center"
          >
            <Image
              src="/press-logos/BFMTV.png"
              width={120}
              height={60}
              alt="Logo BFMTV"
              className="object-contain h-10"
            />
          </Link>

          <Link
            href="https://www.leparisien.fr/economie/consommation/si-on-les-retire-on-sera-face-a-une-vraie-penurie-pourquoi-on-trouve-toujours-des-oeufs-cage-en-rayons-18-02-2026-NDYC5KWEVNA6ZFSWIHFPIOQ76I.php"
            target="_blank"
            className="w-[18%] md:w-[18%] lg:w-fit flex justify-center"
          >
            <Image
              src="/press-logos/Le_Parisien.png"
              width={120}
              height={60}
              alt="Logo Le Parisien"
              className="object-contain h-10"
            />
          </Link>
          <Link
            href="https://photos.app.goo.gl/5XFgLL4NRS5Jcrf67"
            target="_blank"
            className="w-[18%] md:w-[18%] lg:w-fit flex justify-center"
          >
            <Image src="/press-logos/M6.png" width={120} height={60} alt="Logo M6" className="object-contain h-10" />
          </Link>
          <Link
            href="https://www.lefigaro.fr/conso/carrefour-auchan-lidl-plus-de-7-supermarches-sur-10-vendraient-encore-des-oeufs-de-poules-en-cage-20260218"
            target="_blank"
            className="w-[18%] md:w-[18%] lg:w-fit flex justify-center"
          >
            <Image
              src="/press-logos/Le_Figaro.png"
              width={120}
              height={60}
              alt="Logo Le Figaro"
              className="object-contain h-10"
            />
          </Link>

          <Link
            href="https://www.liberation.fr/environnement/alimentation/poules-en-cage-les-promesses-non-tenues-de-la-grande-distribution-20260217_WOJMOAERENCHTLT3BJKW2N4LIQ/"
            target="_blank"
            className="w-[18%] md:w-[18%] lg:w-fit flex justify-center"
          >
            <Image
              src="/press-logos/Liberation.png"
              width={120}
              height={60}
              alt="Logo Libération"
              className="object-contain h-10"
            />
          </Link>
          <Link
            href="https://www.radiofrance.fr/franceinter/podcasts/l-info-de-france-inter/malgre-leurs-promesses-plus-de-70-des-supermarches-vendent-des-oeufs-de-poules-elevees-en-cage-denonce-anima-4056057"
            target="_blank"
            className="w-[18%] md:w-[18%] lg:w-fit flex justify-center"
          >
            <Image
              src="/press-logos/France_Inter.png"
              width={120}
              height={60}
              alt="Logo France Inter"
              className="object-contain h-10"
            />
          </Link>
          <Link
            href="https://www.tf1info.fr/conso/plus-aucun-oeuf-de-poules-elevees-en-cage-vendu-en-supermarche-magasins-rayons-france-grande-distribution-2026-promesse-tenue-2425079.html"
            target="_blank"
            className="w-[18%] md:w-[18%] lg:w-fit flex justify-center"
          >
            <Image src="/press-logos/TF1.png" width={120} height={60} alt="Logo TF1" className="object-contain h-10" />
          </Link>

          <Link
            href="https://www.rtl.fr/actu/economie-consommation/malgre-leurs-engagements-plus-de-70-des-supermarches-continuent-de-vendre-des-oeufs-de-poules-elevees-en-cage-7900602429"
            target="_blank"
            className="w-[18%] md:w-[18%] lg:w-fit flex justify-center"
          >
            <Image src="/press-logos/RTL.png" width={120} height={60} alt="Logo RTL" className="object-contain h-10" />
          </Link>

          <Link
            href="https://rmc.bfmtv.com/conso/alimentation/grande-distribution/7-supermarches-sur-10-vendent-encore-des-ufs-de-poules-elevees-en-cage-malgre-leurs-promesses-de-les-bannir_AN-202602180045.html"
            target="_blank"
            className="w-[18%] md:w-[18%] lg:w-fit flex justify-center"
          >
            <Image src="/press-logos/RMC.png" width={120} height={60} alt="Logo RMC" className="object-contain h-10" />
          </Link>
        </div>
      </div>
      <SectionTitle
        image_path="/full-bars_egg.svg"
        image_alt="egg shaped logo with a hen behind bars"
        title={
          <>
            {t('PressSection.ten_years_ago_supermarkets_pledged').toUpperCase()}{' '}
            <span className="underline">{t('PressSection.to_ban_eggs_from_caged_hens_by_2026').toUpperCase()}.</span>
          </>
        }
      />

      <div className="w-full relative">
        <div className="w-full sm:flex hidden justify-center ">
          <Image
            src="/press-articles.png"
            width={1512}
            height={704}
            alt="collage of press articles"
            className="w-full block"
          />
        </div>
        <div className="w-full sm:hidden flex justify-center">
          <Image
            src="/press-articles_mobile.png"
            width={1650}
            height={1350}
            alt="collage of press articles"
            className="w-full"
          />
        </div>
        <div className="absolute inset-0 bg-gradient-to-t from-white/40 to-transparent"></div>
      </div>
      <span className="absolute bottom-0 animate-bounce">
        <ArrowDown href="#PromiseKeptSection" />
      </span>
    </header>
  );
}
