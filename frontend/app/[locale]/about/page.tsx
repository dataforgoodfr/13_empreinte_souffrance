import ThankingSection from './_sections/thanking_section';
import WhyNameSection from './_sections/why_name_section';
import AssociationPresentationSection from './_sections/association-presentation-section';
import GoFurtherSection from '../ui/_sections/go-further-section';
import { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'À propos',
  description: "Découvrez Anima et Data For Good, les associations à l'origine de L'heure des comptes.",
  keywords: ['Anima association', 'Data For Good', 'bien-être animal France', 'engagement citoyen'],
  openGraph: {
    title: "À propos - L'heure des comptes",
    description: "Découvrez Anima et Data For Good, les associations à l'origine de L'heure des comptes.",
    images: ['/og-about.png'],
  },
  twitter: {
    title: "À propos - L'heure des comptes",
    description: "Découvrez Anima et Data For Good, les associations à l'origine de L'heure des comptes.",
    images: ['/og-about.png'],
  },
  alternates: {
    canonical: '/about',
  },
};

export default async function About() {
  return (
    <>
      <AssociationPresentationSection />
      <WhyNameSection />
      <ThankingSection />
      <GoFurtherSection />
    </>
  );
}
