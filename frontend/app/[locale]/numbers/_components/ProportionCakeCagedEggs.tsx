'use client';
import Image from 'next/image';
import LinkActions from './LinkActions';

export default function ProportionCakeCagedEggs() {
  return (
    <div className="">
      <Image src="/dashboard/proportion_cake_caged_eggs.svg" alt="chart visualization" width={1900} height={900} />
      <LinkActions externalUrl="/about/" downloadImageUrl="/dashboard/proportion_cake_caged_eggs.png" />
    </div>
  );
}
