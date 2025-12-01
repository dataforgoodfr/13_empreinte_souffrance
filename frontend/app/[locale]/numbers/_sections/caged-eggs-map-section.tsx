import StoreMap from '../_components/store-map';
import { getScopedI18n } from '@/locales/server';



export default async function CagedEggsMapSestion() {
  const scopedT = await getScopedI18n('NumbersPage');
  return (
    <section className="p-section min-h-[100dvh] flex justify-center border">
      <div className='max-w-[1450px] flex flex-col md:flex-row md:justify-between md:items-start border'>

      <div className = "flex md:flex-col gap-6 w-1/3">
        <h2 className='text-pink-3 '>{scopedT('caged_eggs_map_section.caged_eggs_store_title')}</h2>
        <p>{scopedT('caged_eggs_map_section.caged_eggs_store_description')}</p>
          <div>
          <a href="">Sources</a>
          <a> Data </a>
          <a> Image </a>
        </div>
      </div>
      <div className='border'>
      <StoreMap/>
      </div>
      </div>
    </section>
  );
}
