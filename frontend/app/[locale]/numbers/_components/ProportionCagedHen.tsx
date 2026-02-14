'use client';
import Image from 'next/image';
import LinkActions from './LinkActions';

export default function ProportionCagedHen() {
  return (
    <div className="">
      <Image src="/dashboard/proportion_caged_hen.svg" alt="chart visualization" width={1900} height={900} />
      <LinkActions externalUrl="/about/" downloadImageUrl="/dashboard/proportion_caged_hen.png" />
    </div>
  );
}
