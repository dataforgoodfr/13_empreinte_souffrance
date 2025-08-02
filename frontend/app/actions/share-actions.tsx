'use client';

import { useEffect, useState } from 'react';
import ButtonLink from '@/app/[locale]/ui/_components/button-link';

interface TwitterShareButtonProps {
  nameLien: string;
  shareMessage: string;
}

export default function TwitterShareButton({ nameLien, shareMessage }: TwitterShareButtonProps) {
  const [url, setUrl] = useState('');

  useEffect(() => {
    // runs only on the client where window is set
    setUrl(window.location.href);
  }, []);

  const shareUrl = `https://twitter.com/intent/tweet?url=${encodeURIComponent(url)}&text=${encodeURIComponent(shareMessage)}`;

  return (
    <ButtonLink
      href={shareUrl}
      aria_label={nameLien}
      button_text={nameLien}
      background_color_name="white"
      open_in_new_tab={true}
    />
  );
}
