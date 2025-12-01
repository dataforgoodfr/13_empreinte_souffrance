import StoreMap from '../_components/store-map';
import { getScopedI18n } from '@/locales/server';



export default async function CagedEggsMapSestion() {
  const scopedT = await getScopedI18n('NumbersPage');

  return (
    <section className="p-section flex justify-center">
      <div className='max-w-[1450px] flex flex-col md:flex-row md:justify-between md:items-start gap-8'>

      <div className = "flex flex-col gap-6 md:w-[45%]">
        <h2 className='text-pink-3 '>{scopedT('caged_eggs_map_section.caged_eggs_store_title')}</h2>
        <p>{scopedT('caged_eggs_map_section.caged_eggs_store_description')}</p>
          <div>
          <a href="">Sources</a>
          <a> Data </a>
          <a> Image </a>
        </div>
      </div>
      <div className='w-full overflow-hidden'>
      <StoreMap/>
      </div>
      </div>
    </section>
  );
}
