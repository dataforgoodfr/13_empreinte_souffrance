'use client';
import { useState } from 'react';

interface ListOfAfflictionProps {
  listOfPain: string[];
  seeMore: string;
  seeLess: string;
}

export default function ListOfAffliction({ listOfPain, seeMore, seeLess }: ListOfAfflictionProps) {
  const [showAll, setShowAll] = useState(false);
  const toggleShowAll = () => setShowAll((prev) => !prev);
  const displayedList = showAll ? listOfPain : listOfPain.slice(0, 4);

  return (
    <>
      <div className=" grid grid-cols-2 w-full text-center uppercase text-bold gap-[5px] text-xs md:text-sm text-pink-1">
        {displayedList.map((pain, index) => (
          <p key={index} className="bg-brown flex items-center justify-center p-2 rounded-[5px]">
            {pain}
          </p>
        ))}
      </div>

      {listOfPain.length > 4 && (
        <button className="white-button mt-4 w-full" onClick={toggleShowAll}>
          {showAll ? seeLess : seeMore}
        </button>
      )}
    </>
  );
}
