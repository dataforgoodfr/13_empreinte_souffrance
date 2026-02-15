import { Metadata } from 'next';
import { ReactNode } from 'react';

export const metadata: Metadata = {
  title: "Bient\u00f4t disponible - L'heure des comptes",
  description:
    "Le site L'heure des comptes sera bient\u00f4t disponible. D\u00e9couvrez si les supermarch\u00e9s ont tenu leur promesse de bannir les \u0153ufs de poules en cage.",
  robots: {
    index: false,
  },
};

export default function CountdownLayout({ children }: { children: ReactNode }) {
  return <>{children}</>;
}
