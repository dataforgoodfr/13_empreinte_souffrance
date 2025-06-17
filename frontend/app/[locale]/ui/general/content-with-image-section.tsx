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
}: ContentWithImageSectionProps) {
  return (
    <section
      className={clsx(
        'text-[#3b0a0a] flex flex-col w-full',
        image_position === 'right' ? 'md:flex-row' : 'md:flex-row-reverse'
      )}
    >
      {' '}
      <div className="flex flex-col flex-1 md:basis-1/2">
        <div className="h-full  w-full  border-[#ff7f7f] border-2 flex flex-col justify-between items-start p-3">
          <h3 className="text-3xl sm:text-4xl font-extrabold tracking-wide text-[#3b0a0a] mb-10 flex justify-start items-center gap-3">
            <BoltIcon />
            {text_heading.toUpperCase()}
          </h3>
          <p className="text-base sm:text-lg font-light">{text_content}</p>
        </div>
      </div>
      <ImageInContent image_url={image_url} image_description={image_description} />
    </section>
  );
}

type ImageInContentProps = {
  image_url: string;
  image_description: string;
};

function ImageInContent({ image_url, image_description }: ImageInContentProps) {
  return (
    <div className="border-[#ff7f7f] border-2 flex justify-center items-center flex-1 md:basis-1/2">
      <Image
        src={'/' + image_url}
        alt={image_description}
        width={560}
        height={560}
        className="w-full h-auto object-cover"
        {...(image_description ? {} : { role: 'presentation' })}
      />
    </div>
  );
}
