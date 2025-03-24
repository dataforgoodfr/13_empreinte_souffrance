import Link from "next/link";
import NavLinks from "@/app/[locale]/ui/general/nav-links";
import { LocaleSelect } from "../localselect";

export default function Navbar() {
  return (
    <>
      <div className="flex h-full w-full px-3 py-4 md:px-2 items-center justify-center bg-indigo-800">
        <Link
          className="flex h-4 items-center justify-center rounded-md bg-blue-600 p-4"
          href="/"
        >
          <div className="w-38 text-white">ES Logo placeholder</div>
        </Link>
        <div className="flex gap-1 grow justify-start w-full ml-3">
          <NavLinks />
        </div>
        <LocaleSelect />
      </div>
    </>
  );
}
