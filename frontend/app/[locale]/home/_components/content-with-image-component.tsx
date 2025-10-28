import Image from 'next/image';
import clsx from 'clsx';
import Link from 'next/link';
import { getI18n } from '@/locales/server';

type ContentWithImageComponentProps = {
  text_heading: string;
  text_content: string;
  image_url: string;
  image_description: string;
  image_position?: 'left' | 'right';
  hide_image_on_small_screen?: boolean;
};

export default async function ContentWithImageComponent({
  text_heading,
  text_content,
  image_url,
  image_description,
  image_position = 'left',
}: ContentWithImageComponentProps) {
  const t = await getI18n();
  return (
    <section
      className={clsx(
        'dark-text flex flex-col w-full',
        image_position === 'right' ? 'md:flex-row' : 'md:flex-row-reverse'
      )}
    >
      {' '}
      <div className="flex flex-col flex-1 md:basis-1/2">
        <div className="h-full  w-full flex flex-col items-start p-3">
          <h3 className="text-3xl sm:text-4xl font-extrabold tracking-wide dark-text mb-5 flex justify-start items-center">
            {text_heading.toUpperCase()}
          </h3>
          <p className="text-base sm:text-lg font-light">{text_content}</p>
          <Link
            href="/dashboard"
            className="inline-block py-3 px-6 text-lg bg-grey hover:bg-violet w-full font-mono dark-text tracking-wider transition-all duration-200"
            aria-label={t('PainEquationSection.cta')}
          >
            <span className='text-caption'>{t('PainEquationSection.cta')}</span> →
          </Link>
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
    <div className="flex justify-center items-center flex-1 md:basis-1/2">
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
