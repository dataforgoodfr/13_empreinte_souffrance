import ContentWithImageSection from '@/app/[locale]/ui/general/content-with-image-section';

export default async function Page() {
  return (
    <>
      <ContentWithImageSection
        text_content="We are nice people"
        image_url="tmp_chicken-image.webp"
        image_description="Picture of a chicken"
        image_position="right"
        hide_image_on_small_screen={false}
      />
    </>
  );
}
