import { getI18n } from '@/locales/server';
import Link from 'next/link';

export default async function LinkSection() {
  const t = await getI18n();

  type LinkSectionType = {
    description: string;
    section_id: string;
  };

  const links: LinkSectionType[] = [
    { description: t('LinkSection.WFI'), section_id: '#WFIArticleSection' },
    { description: t('LinkSection.SufferingCauses'), section_id: '#SufferingCausesSection' },
    { description: t('LinkSection.PainEquation'), section_id: '#PainEquationSection' },
    { description: t('LinkSection.Results'), section_id: '#ResultSection' },
    { description: t('LinkSection.BookAnnouncement'), section_id: '#BookAnnouncementSection' },
    { description: t('LinkSection.GoFurther'), section_id: '#GoFurtherSection' },
  ];

  return (
    <section className="w-full bg-white flex flex-wrap items-center justify-center">
      {links.map((link) => (
        <Link
          key={link.description}
          className="py-2 px-4 text-center font-mono tracking-widest text-[#3b0a0a] border border-red-300 hover:bg-gray-200 text-nowrap min-w-35 md:min-w-100 lg:min-w-120 grow transition-all duration-200"
          href={link.section_id}
        >
          {link.description}
        </Link>
      ))}
    </section>
  );
}
