import React from 'react';
import { getI18n } from '@/locales/server';

export default async function PainTrackTable() {
  const t = await getI18n();

  return (
    <div className="flex pr-4 lg:pr-8 lg:pl-2 pb-8 pt-2  overflow-x-auto">
      <table className=" table-auto w-full text-center text-xs md:text-base border-separate border-spacing-0.5">
        <thead>
          {/* Légende "Phase de lésion" */}
          <tr>
            <th colSpan={2}></th>
            <th className="px-4 py-2 text-center italic" colSpan={5}>
              {t('MethodologyPage.QuantifySufferingByPain.painTrackTable.lesionPhase')}{' '}
            </th>
          </tr>

          {/* Ligne en-têtes */}
          <tr>
            <th />
            <th />
            <th className="bg-grey p-2">
              {t('MethodologyPage.QuantifySufferingByPain.painTrackTable.ruptureTissu')}
              <br />
              <span className="italic text-caption">0,5–2 min</span>
            </th>
            <th className=" bg-grey p-2">
              {t('MethodologyPage.QuantifySufferingByPain.painTrackTable.coagulation')}
              <br />
              <span className="italic text-caption">5–15 min</span>
            </th>
            <th className="bg-grey p-2">
              {t('MethodologyPage.QuantifySufferingByPain.painTrackTable.inflammation')}
              <br />
              <span className="italic text-caption">16h–48h</span>
            </th>
            <th className="bg-grey p-2">
              {t('MethodologyPage.QuantifySufferingByPain.painTrackTable.proliferation')}
              <br />
              <span className="italic text-caption">22h–36h</span>
            </th>
            <th className="bg-grey p-6">Total</th>
          </tr>
        </thead>

        <tbody>
          {/* Ligne inconfort */}
          <tr>
            {/* Légende "Intensité de la souffrance" */}
            <td
              className="px-4 py-2 text-center italic font-bold text-nowrap"
              style={{ textOrientation: 'mixed', writingMode: 'sideways-lr' }}
              rowSpan={6}
            >
              {t('MethodologyPage.QuantifySufferingByPain.painTrackTable.intensityOfSuffering')}
            </td>

            <th className="bg-pink-1 text-center p-2 py-4">
              {t('MethodologyPage.QuantifySufferingByPain.painTrackTable.discomfort')}
            </th>
            <td className="bg-pink-1"></td>
            <td className="bg-pink-1"></td>
            <td className="bg-pink-1"></td>
            <td className="bg-pink-1">70%</td>
            <td className="bg-pink-1">
              196 h <br /> <p className="text-caption">± 39.2h</p>
            </td>
          </tr>

          {/* Ligne douleur */}
          <tr className="bg-white">
            <th className="bg-pink-2 font-semibold text-center p-2 py-4">
              {t('MethodologyPage.QuantifySufferingByPain.painTrackTable.pain')}
            </th>
            <td className="bg-pink-2">50%</td>
            <td className="bg-pink-2">80%</td>
            <td className="bg-pink-2">100%</td>
            <td className="bg-pink-2">30%</td>
            <td className="bg-pink-2">
              116.14 h<p className="text-caption"> ± 23.20h</p>
            </td>
          </tr>

          {/* Ligne souffrance */}
          <tr className="bg-white">
            <th className="bg-pink-3 font-semibold text-center p-2 py-4">
              {t('MethodologyPage.QuantifySufferingByPain.painTrackTable.suffering')}
            </th>
            <td className="bg-pink-3">50%</td>
            <td className="bg-pink-3">20%</td>
            <td className="bg-pink-3"></td>
            <td className="bg-pink-3"></td>
            <td className="bg-pink-3">
              2.63 min <p className="text-caption"> ± 1.07 min</p>
            </td>
          </tr>

          {/* Ligne Agony */}
          <tr className="bg-white">
            <th className="bg-brown font-semibold text-center p-2 py-4 text-pink-1">
              {t('MethodologyPage.QuantifySufferingByPain.painTrackTable.agony')}
            </th>
            <td className="bg-brown"></td>
            <td className="bg-brown"></td>
            <td className="bg-brown"></td>
            <td className="bg-brown"></td>
            <td className="bg-brown text-pink-1">0 min</td>
          </tr>
        </tbody>
      </table>
    </div>
  );
}
