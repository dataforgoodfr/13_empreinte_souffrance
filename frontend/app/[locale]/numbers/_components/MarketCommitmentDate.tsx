'use client';
import Image from 'next/image';
import LinkActions from './LinkActions';

export default function MarketCommitmentDate() {
  return (
    <div className="">
      <Image src="/dashboard/market_commitment_date.svg" alt="chart visualization" width={1900} height={900} />
      <LinkActions externalUrl="/about/" downloadImageUrl="/dashboard/market_commitment_date.png" />
    </div>
  );
}
