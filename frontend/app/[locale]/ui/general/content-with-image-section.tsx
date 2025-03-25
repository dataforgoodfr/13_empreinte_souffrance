import Image from 'next/image';
import clsx from 'clsx';

type ContentWithImageSectionProps = {
  text_content: string;
  image_url: string;
  image_description: string;
  image_position?: 'left' | 'right';
  hide_image_on_small_screen?: boolean;
};

export default function ContentWithImageSection({
  text_content,
  image_url,
  image_description,
  image_position = 'left',
  hide_image_on_small_screen = false,
}: ContentWithImageSectionProps) {
  return (
    <section
      className={clsx(
        'bg-gradient-to-r from-blue-600 via-blue-500 to-indigo-500 h-screen md:flex items-center justify-center gap-8 px-8 sm:px-16',
        { 'md:flex-row-reverse': image_position === 'right' }
      )}
    >
      <div className={clsx({ 'hidden lg:block': hide_image_on_small_screen })}>
        <Image src={'/' + image_url} width={560} height={620} alt={image_description} />
      </div>
      <div className="text-center w-fit mx-6">
        <p className="text-white text-center text-base sm:text-lg font-light">{text_content}</p>
      </div>
    </section>
  );
}
