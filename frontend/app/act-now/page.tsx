import ContentWithImageSection from "@/app/ui/general/content-with-image-section";

export default async function Page() {
  return (
    <>
      <ContentWithImageSection
        text_content="YOU CAN DO SOMETHING"
        image_url="tmp_chicken-image.webp"
        image_description="Picture of a chicken"
        image_position="right"
        hide_image_on_small_screen={false}
      />
    </>
  );
}
