'use client';
import Image from 'next/image';
import LinkActions from './LinkActions';

export default function ProportionMarketVisited() {
  return (
    <div className="">
      <Image src="/dashboard/proportion_market_visited.svg" alt="chart visualization" width={1900} height={900} />
      <LinkActions externalUrl="/about/" downloadImageUrl="/dashboard/proportion_market_visited.png" />
    </div>
  );
}
