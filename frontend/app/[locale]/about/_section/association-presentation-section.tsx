import { getScopedI18n } from '@/locales/server';

export default async function AssociationPresentationSection() {
  const scopedT = await getScopedI18n('AboutPage.association_presentation_section');

  return (
    <>
      <h1 className="mx-16 my-8 max-w-xl text-3xl sm:text-4xl ">
        {scopedT('two_hens_out_five_title').toUpperCase()}
      </h1>
    </>
  );
}