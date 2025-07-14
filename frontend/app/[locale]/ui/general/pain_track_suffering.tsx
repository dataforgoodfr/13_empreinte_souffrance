import React from 'react';

const PainTrackTable = () => {
  return (
    <div className="flex px-0 lg:px-8 relative">
      <p className=" rotate-[-90deg] absolute md:left-[-90] lg:left-[-80] left-[-75] md:top-[180] top-[190] text-nowrap text-xs md:text-base italic font-bold ">
        Intensité de la douleur
      </p>
      <table className="table-auto w-full text-center text-xs md:text-base border-separate border-spacing-0.5">
        <thead>
          <tr>
            <th className="px-4 py-2 text-center italic" colSpan={6}>
              Phase de la lésion
            </th>
          </tr>
          <tr className="bg-white">
            <th className="bg-pink-50" />
            <th className="p-2 font-medium">
              Rupture du tissu
              <br />
              <span className="italic text-xs">0,5–2 min</span>
            </th>
            <th className="p-2 font-medium">
              Coagulation
              <br />
              <span className="italic text-xs">5–15 min</span>
            </th>
            <th className="p-2 font-medium">
              Inflammation
              <br />
              <span className="italic text-xs">16h–48h</span>
            </th>
            <th className="p-2 font-medium">
              Prolifération
              <br />
              <span className="italic text-xs">22h–36h</span>
            </th>
            <th className="p-2 font-medium">Total</th>
          </tr>
        </thead>
        <tbody>
          <tr className="bg-white">
            <th className=" font-semibold text-center p-2">Inconfort</th>
            <td className=""></td>
            <td className=""></td>
            <td className=""></td>
            <td className="">70%</td>
            <td className="">196h ± 39.2h</td>
          </tr>
          <tr className="bg-white">
            <th className="bg-pink-200  font-semibold text-center p-2">Douleur</th>
            <td className="">50%</td>
            <td className="">80%</td>
            <td className="">100%</td>
            <td className="">30%</td>
            <td className="">116.14h ± 23.20h</td>
          </tr>
          <tr className="bg-white">
            <th className="bg-red-300 font-semibold text-center p-2">Souffrance</th>
            <td className="">50%</td>
            <td className="">20%</td>
            <td className=""></td>
            <td className=""></td>
            <td className="">2.63 min ± 1.07 min</td>
          </tr>
          <tr className="bg-white">
            <th className=" bg-red-900 font-semibold text-center p-2 text-white">Agonie</th>
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
};

export default PainTrackTable;
