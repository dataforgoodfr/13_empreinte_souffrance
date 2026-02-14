'use client';
import Image from 'next/image';
import LinkActions from './LinkActions';

export default function EggsSalesFarmingMethod() {
  return (
    <div className="">
      <Image src="/dashboard/eggs_sales_farming_method.svg" alt="chart visualization" width={1900} height={900} />
      <LinkActions
        externalUrl="/about/#eggs_sales_farming_method"
        downloadImageUrl="/dashboard/eggs_sales_farming_method.png"
      />
    </div>
  );
}
