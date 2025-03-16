import ContentWithImageSection from "@/app/ui/general/content-with-image-section";

export default async function Page() {
  return (
    <>
      <ContentWithImageSection
        text_content="Big interesting data about hens"
        image_url="tmp_chicken-image.webp"
        image_description="Picture of a chicken"
        image_position="left"
        hide_image_on_small_screen={false}
      />
      <ContentWithImageSection
        text_content="Here we will have a more detailed explanation about something interesting."
        image_url="tmp_chicken-image.webp"
        image_description="Picture of a chicken"
        image_position="left"
        hide_image_on_small_screen={false}
      />
    </>
  );
}
