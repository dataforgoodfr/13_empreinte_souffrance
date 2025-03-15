import ContentWithImageSection from "@/app/ui/general/content-with-image-section";

export default async function Page() {
  return (
    <>
      <h2>METHODE SCIENTIFIQUE</h2>
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
