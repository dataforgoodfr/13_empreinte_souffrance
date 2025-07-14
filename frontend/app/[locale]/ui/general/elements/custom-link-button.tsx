import Link from 'next/link';
import clsx from "clsx";

type CustomLinkButtonType = {
    href : string;
    aria_label : string;
    button_text : string;
    download?: boolean;
    open_in_new_tab?: boolean;
    width?: 'full' | 'small';
}

export default async function CustomLinkButton({href, aria_label, button_text, download = false, open_in_new_tab = false, width = 'full'}: CustomLinkButtonType) {

    return (
        <Link
            href={href}
            target={download || open_in_new_tab ? '_blank' : '' }
            download={download}
            className={clsx("text-center  dark-text font-mono font-bold py-4 px-6 rounded-full shadow-[4px_4px_0_#000] flex items-center justify-center transition-all duration-200 bg-(--pink-3) hover:bg-(--violet-1) ", {
                'w-full' : width == 'full',
                'w-max': width == 'small',
            })}
            aria-label={aria_label}
        >
            {button_text}
        </Link>
    )
}
