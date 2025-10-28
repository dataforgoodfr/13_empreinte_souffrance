import Link from 'next/link';
import clsx from 'clsx';

const bgColorList = {
  pink: 'bg-pink-3',
  white: 'bg-white',
};

type CustomLinkButtonProps = {
  href: string;
  aria_label: string;
  button_text: string;
  download?: boolean;
  open_in_new_tab?: boolean;
  background_color_name?: keyof typeof bgColorList;
  width?: 'full' | 'small';
};

export default function ButtonLink({
  href,
  aria_label,
  button_text,
  download = false,
  open_in_new_tab = false,
  background_color_name = 'pink',
  width = 'full',
}: CustomLinkButtonProps) {
  return (
    <Link
      href={href}
      target={download || open_in_new_tab ? '_blank' : ''}
      download={download}
      className={clsx(
        'primary-button text-center dark-text text-caption font-bold py-2 px-6 rounded-md shadow-[0_4px_0_#000] flex items-center justify-center transition-all duration-200 hover:bg-violet ',
        bgColorList[background_color_name],
        {
          'w-full': width == 'full',
          'w-max': width == 'small',
        }
      )}
      aria-label={aria_label}
    >
      {button_text}
    </Link>
  );
}
