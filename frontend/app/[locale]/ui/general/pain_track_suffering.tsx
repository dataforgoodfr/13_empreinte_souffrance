import React from 'react';
import { getI18n } from '@/locales/server';

export default async function PainTrackTable() {
  const t = await getI18n();

  return (
    <div className="flex px-0 lg:px-8 relative">
      <table className="table-auto w-full text-center text-xs md:text-base border-separate border-spacing-0.5">
        <thead>
          <tr>
            <th className="px-4 py-2 text-center italic" colSpan={7}>
              {t('MethodologyPage.QuantifySufferingByPain.painTrackTable.lesionPhase')}{' '}
            </th>
          </tr>
          <tr className="bg-white">
            <th className="bg-pink-50" />
            <th className="bg-pink-50" />
            <th className="p-2 font-medium">
              {t('MethodologyPage.QuantifySufferingByPain.painTrackTable.ruptureTissu')}
              <br />
              <span className="italic text-xs">0,5–2 min</span>
            </th>
            <th className="p-2 font-medium">
              {t('MethodologyPage.QuantifySufferingByPain.painTrackTable.coagulation')}
              <br />
              <span className="italic text-xs">5–15 min</span>
            </th>
            <th className="p-2 font-medium">
              {t('MethodologyPage.QuantifySufferingByPain.painTrackTable.inflammation')}
              <br />
              <span className="italic text-xs">16h–48h</span>
            </th>
            <th className="p-2 font-medium">
              {t('MethodologyPage.QuantifySufferingByPain.painTrackTable.proliferation')}
              <br />
              <span className="italic text-xs">22h–36h</span>
            </th>
            <th className="p-2 font-medium">Total</th>
          </tr>
        </thead>
        <tbody>
          <tr className="bg-white">
            <td
              className="px-4 py-2 text-center italic bg-pink-50 font-medium "
              style={{ textOrientation: 'mixed', writingMode: 'sideways-lr' }}
              rowSpan={6}
            >
              {t('MethodologyPage.QuantifySufferingByPain.painTrackTable.intensityOfSuffering')}
            </td>
            <th className=" font-semibold text-center p-2">
              {t('MethodologyPage.QuantifySufferingByPain.painTrackTable.discomfort')}
            </th>
            <td className=""></td>
            <td className=""></td>
            <td className=""></td>
            <td className="">70%</td>
            <td className="">196h ± 39.2h</td>
          </tr>
          <tr className="bg-white">
            <th className="bg-pink-200  font-semibold text-center p-2">
              {t('MethodologyPage.QuantifySufferingByPain.painTrackTable.pain')}
            </th>
            <td className="">50%</td>
            <td className="">80%</td>
            <td className="">100%</td>
            <td className="">30%</td>
            <td className="">116.14h ± 23.20h</td>
          </tr>
          <tr className="bg-white">
            <th className="bg-red-300 font-semibold text-center p-2">
              {t('MethodologyPage.QuantifySufferingByPain.painTrackTable.suffering')}
            </th>
            <td className="">50%</td>
            <td className="">20%</td>
            <td className=""></td>
            <td className=""></td>
            <td className="">2.63 min ± 1.07 min</td>
          </tr>
          <tr className="bg-white">
            <th className=" bg-red-900 font-semibold text-center p-2 text-white">
              {t('MethodologyPage.QuantifySufferingByPain.painTrackTable.agony')}
            </th>
            <td className=""></td>
            <td className=""></td>
            <td className=""></td>
            <td className=""></td>
            <td className="">0 min</td>
          </tr>
        </tbody>
      </table>
    </div>
  );
}
