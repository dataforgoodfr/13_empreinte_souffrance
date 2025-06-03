import Image from 'next/image';
import clsx from 'clsx';
import BoltIcon from '@/app/[locale]/ui/icons/BoltIcon';

type ContentWithImageSectionProps = {
  text_heading: string;
  text_content: string;
  image_url: string;
  image_description: string;
  image_position?: 'left' | 'right';
  hide_image_on_small_screen?: boolean;
};

export default function ContentWithImageSection({
  text_heading,
  text_content,
  image_url,
  image_description,
  image_position = 'left',
  hide_image_on_small_screen = false,
}: ContentWithImageSectionProps) {
  return (
    <section className="text-[#3b0a0a] grid grid-cols-1 md:grid-cols-2">
      {image_position === 'left' && (
        <ImageInContent
          image_url={image_url}
          image_description={image_description}
          hide_image_on_small_screen={hide_image_on_small_screen}
        />
      )}
      <div className="h-full w-full border-[#ff7f7f] border-2 flex flex-col justify-between items-start p-3">
        <h3
          id="results-heading"
          className="text-3xl sm:text-4xl font-extrabold tracking-wide text-[#3b0a0a] mb-10 flex justify-start items-center gap-3"
        >
          <BoltIcon />
          {text_heading.toUpperCase()}
        </h3>
        <p className="text-base sm:text-lg font-light">{text_content}</p>
      </div>
      {image_position === 'right' && (
        <ImageInContent
          image_url={image_url}
          image_description={image_description}
          hide_image_on_small_screen={hide_image_on_small_screen}
        />
      )}
    </section>
  );
}

type ImageInContentProps = {
  image_url: string;
  image_description: string;
  hide_image_on_small_screen?: boolean;
};

function ImageInContent({ image_url, image_description, hide_image_on_small_screen = false }: ImageInContentProps) {
  return (
    <div
      className={clsx('border-[#ff7f7f] border-2 flex justify-center items-center', {
        'hidden md:block': hide_image_on_small_screen,
      })}
    >
      <Image
        src={'/' + image_url}
        width={560}
        height={560}
        alt={image_description}
        {...(image_description ? {} : { role: 'presentation' })}
      />
    </div>
  );
}
