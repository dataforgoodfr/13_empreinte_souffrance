'use client';

interface TwitterShareButtonProps {
  nameLien: string;
}

export default function TwitterShareButton({nameLien}:TwitterShareButtonProps) {

  // eslint-disable-next-line no-undef
  const shareOnTwitter = (e: React.MouseEvent<HTMLButtonElement>) => {
    e.preventDefault();
    const url = window.location.href;
    const shareUrl = `https://twitter.com/intent/tweet?url=${encodeURIComponent(url)}&text=Découvrez+ce+site+!`;
    window.open(shareUrl, '_blank', 'noopener,noreferrer');
  };

  return (
    <button
          className="w-full dark-text font-mono font-bold py-4 px-6 rounded-full shadow-[4px_4px_0_#000] cursor-pointer transition-all duration-200 bg-(--pink-3) hover:bg-(--violet-1)"
      aria-label="Partager sur Twitter"
      onClick={shareOnTwitter}
      type="button"
    >
      {nameLien}
    </button>
  );
}
