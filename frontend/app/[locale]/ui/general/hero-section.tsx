import { getScopedI18n } from "@/locales/server";
import Image from "next/image";
import Link from "next/link";

export default async function HeroSection() {
  const scopedT = await getScopedI18n("Home");

  return (
    <section className="bg-gradient-to-r from-blue-600 via-blue-500 to-indigo-500 h-screen flex items-center justify-between px-8 sm:px-16">
      <div className="max-w-xl space-y-6">
        <div className="inline-block bg-indigo-800 text-white py-2 px-4 rounded-lg text-sm font-semibold tracking-wide">
          {scopedT("badge")}
        </div>
        <h1 className="text-5xl sm:text-6xl lg:text-7xl font-bold text-white">
          {scopedT("animal_welfare")}
          <br />
          <span className="text-green-300">{scopedT("science")}</span>
          <br />
          {scopedT("explained")}
        </h1>
        <p className="text-white text-justify text-base sm:text-lg font-light max-w-md">
          {scopedT("paragraph")}
        </p>
        <Link
          href="/science"
          className="bg-green-300 text-gray-800 px-6 py-3 text-lg font-medium rounded-lg shadow-lg hover:bg-green-400"
        >
          {scopedT("link")}
        </Link>
      </div>
      <div className="hidden lg:block">
        <Image
          src="/tmp_chicken-image.webp"
          width={560}
          height={620}
          className="block"
          alt="Picture of a chicken"
        />
      </div>
    </section>
  );
}
