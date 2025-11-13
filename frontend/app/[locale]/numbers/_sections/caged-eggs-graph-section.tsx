'use client';

import { useEffect } from 'react';

export default function CagedEggsGraphSection() {
  useEffect(() => {
    const script = document.createElement('script');
    script.src = 'https://public.flourish.studio/resources/embed.js';
    script.async = true;
    document.body.appendChild(script);

    return () => {
      document.body.removeChild(script);
    };
  }, []);

  return (
    <div className="flourish-embed flourish-chart" data-src="visualisation/26100156" style={{ width: '100%' }}>
      <noscript>
        <img
          src="https://public.flourish.studio/visualisation/26100156/thumbnail"
          width="100%"
          alt="chart visualization"
        />
      </noscript>
    </div>
  );
}
