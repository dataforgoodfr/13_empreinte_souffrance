import { getScopedI18n } from '@/locales/server';

export default async function Terms() {
  const scopedT = await getScopedI18n('LegalMentionPage');

  return (
    <section className="p-section flex justify-center gap-8 ">
      <div className="flex flex-col max-w-[850px] gap-8">

      <h1>{scopedT('legalMention')}</h1>
      <p>{scopedT('conformingDispositions')}</p>
      <div className="flex flex-col gap-2">
        <h2>{scopedT('webSiteEdition.title')}</h2>
        <p>{scopedT('webSiteEdition.editionBy')}</p>
        <p>{scopedT('webSiteEdition.animaAssociation')}</p>
      </div>
       <div className="flex flex-col gap-2">
        <h2>{scopedT('webHost.title')}</h2>
        <p>{scopedT('webHost.description')}</p>
      </div>
      <div className="flex flex-col gap-2">
        <h2>{scopedT('publicationDirector.title')}</h2>
        <p>{scopedT('publicationDirector.description')}</p>
      </div>
      <div className="flex flex-col gap-2">
        <h2>{scopedT('contactUs.title')}</h2>
        <p>{scopedT('contactUs.email')}</p>
        <p>{scopedT('contactUs.mail')}</p>
      </div>
      <div className="flex flex-col gap-2">
        <h2>{scopedT('personalData.title')}</h2>
        <p>{scopedT('personalData.dataCollection')}</p>
        <p>{scopedT('personalData.externalServices')}
          <a className="hover:text-pink-3 underline transition-colors duration-200" href="https://www.brevo.com/fr/legal/privacypolicy/">Brevo - Politique de confidientialité </a>
        </p>
        <p>{scopedT('personalData.dataManagement')}</p>
      </div>
      </div>
    </section>
  );
}
