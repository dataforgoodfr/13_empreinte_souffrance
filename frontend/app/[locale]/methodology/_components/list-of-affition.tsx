'use client';
import { useState } from "react";

interface ListOfAfflictionProps {
  listOfPain: string[];
  seeMore:string
  seeLess:string
}

export default function ListOfAffliction({ listOfPain, seeMore, seeLess }: ListOfAfflictionProps) {

    const [showAll, setShowAll] = useState(false);
  const toggleShowAll = () => setShowAll((prev) => !prev);
    const displayedList = showAll ? listOfPain : listOfPain.slice(0, 4);

  return (
    <>
      <div className="mt-4 grid grid-cols-2 w-full text-center font-mono uppercase font-bold gap-1 text-xs md:text-sm ">
        {displayedList.map((pain, index) => (
          <p key={index} className="bg-pink-3 p-2 transition-all duration-200">
            {pain}
          </p>
        ))}
      </div>

      {listOfPain.length > 4 && (
        <button
          className="text-sm mt-1 bg-pink-2 font-mono font-bold py-4 px-6 rounded-full shadow-[4px_4px_0_#000] w-full block cursor-pointer text-center transition-all duration-200 hover:bg-pink-3"
          onClick={toggleShowAll}
        >
          {showAll ? seeLess : seeMore}
        </button>
      )}
    </>
  );
}
