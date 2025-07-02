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
          className="w-full bg-[#ff7f7f] text-[#3b0a0a] font-mono font-bold py-4 px-6 rounded-full shadow-[4px_4px_0_#000] cursor-pointer transition-all duration-200 hover:bg-[#FFC3C3]"
      aria-label="Partager sur Twitter"
      onClick={shareOnTwitter}
      type="button"
    >
      {nameLien}
    </button>
  );
}
