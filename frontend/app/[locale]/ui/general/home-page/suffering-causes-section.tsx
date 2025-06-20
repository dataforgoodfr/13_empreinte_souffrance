import { getI18n } from '@/locales/server';
import SectionHeading from '@/app/[locale]/ui/general/home-page/elements/section-heading';
import BoltIcon from '@/app/[locale]/ui/icons/BoltIcon';

export default async function SufferingCausesSection() {
  const t = await getI18n();

  return (
    <section className="py-16 bg-white text-[#3b0a0a] scroll-mt-18" id="SufferingCausesSection">
      <div className="max-w-screen-xl mx-auto px-4">
        <SectionHeading title={t('SufferingCausesSection.title')} heading_number="1" />

        <div className="flex flex-col md:flex-row justify-center gap-6 relative mt-12">
          <div className="flex flex-col justify-between  md:w-1/3">
            <SufferingBox title={t('SufferingCausesSection.box1.title')}>
              {t('SufferingCausesSection.box1.text')}
            </SufferingBox>

            <SufferingBox title={t('SufferingCausesSection.box2.title')} className="md:ml-10">
              {t('SufferingCausesSection.box2.text')}
            </SufferingBox>
          </div>

          <div className="hidden md:flex justify-center relative">
            <img src="suffering_logo.PNG" alt="Silhouette d'une poule" className="w-full h-auto object-contain " />
          </div>

          <div className="flex flex-col justify-between gap-6 text-left md:w-1/3">
            <SufferingBox title={t('SufferingCausesSection.box3.title')} className="md:-ml-48 md:-mt-10">
              {t('SufferingCausesSection.box3.text')}
            </SufferingBox>
            <SufferingBox title={t('SufferingCausesSection.box4.title')}>
              {t('SufferingCausesSection.box4.text')}
            </SufferingBox>
            <SufferingBox title={t('SufferingCausesSection.box5.title')} className="md:-ml-24">
              {t('SufferingCausesSection.box5.text')}
            </SufferingBox>
          </div>
        </div>

        <div className="md:w-1/3 mx-auto">
          <SufferingBox title={t('SufferingCausesSection.box6.title')}>
            {t('SufferingCausesSection.box6.text')}
          </SufferingBox>
        </div>

        <div className="mt-8 text-center text-xs font-semibold tracking-wider uppercase">
          {t('SufferingCausesSection.othersSources')}
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
