'use client';

import { useEffect } from 'react';

export default function CagedEggsGraph() {
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
    <div className="flourish-embed flourish-chart w-[50vh]" data-src="visualisation/26100156">
      <noscript>
        <img
          src="https://public.flourish.studio/visualisation/26100156/thumbnail"
          alt="chart visualization"
        />
      </noscript>
    </div>
  );
}
