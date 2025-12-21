'use client';

import dynamic from 'next/dynamic';

const StoreMap = dynamic(() => import('./store-map'), { ssr: false });

export default StoreMap;
