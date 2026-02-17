'use client';

import { useEffect, useState } from 'react';
import Image from 'next/image';

const RELEASE_DATE = new Date(process.env.NEXT_PUBLIC_RELEASE_DATE || '2026-02-18T05:00:00.000Z');

function calculateTimeLeft() {
  const diff = RELEASE_DATE.getTime() - Date.now();
  if (diff <= 0) return { days: 0, hours: 0, minutes: 0, seconds: 0 };
  return {
    days: Math.floor(diff / (1000 * 60 * 60 * 24)),
    hours: Math.floor((diff / (1000 * 60 * 60)) % 24),
    minutes: Math.floor((diff / (1000 * 60)) % 60),
    seconds: Math.floor((diff / 1000) % 60),
  };
}

function TimeUnit({ value, label }: { value: number; label: string }) {
  const digits = String(value).padStart(2, '0');
  return (
    <div className="flex flex-col items-center gap-1.5">
      <div className="flex gap-[3px] sm:gap-[5px]">
        <span className="flex items-center justify-center w-[30px] h-[42px] sm:w-12 sm:h-[66px] bg-pink-3 text-white rounded-md sm:rounded-lg font-black text-2xl sm:text-[40px] leading-none tabular-nums">
          {digits[0]}
        </span>
        <span className="flex items-center justify-center w-[30px] h-[42px] sm:w-12 sm:h-[66px] bg-pink-3 text-white rounded-md sm:rounded-lg font-black text-2xl sm:text-[40px] leading-none tabular-nums">
          {digits[1]}
        </span>
      </div>
      <span className="font-bold text-[9px] sm:text-[11px] text-white/40 uppercase tracking-[1.5px]">
        {label}
      </span>
    </div>
  );
}

function Separator() {
  return (
    <span
      className="font-black text-2xl sm:text-[40px] text-pink-3/60 leading-[42px] sm:leading-[66px] select-none"
      aria-hidden="true"
    >
      :
    </span>
  );
}

export default function CountdownPage() {
  const [timeLeft, setTimeLeft] = useState<ReturnType<typeof calculateTimeLeft> | null>(null);

  useEffect(() => {
    setTimeLeft(calculateTimeLeft());
    const timer = setInterval(() => {
      const t = calculateTimeLeft();
      setTimeLeft(t);
      // redirect to main page when website is released
      if (t.days + t.hours + t.minutes + t.seconds === 0) {
        clearInterval(timer);
        window.location.href = '/';
      }
    }, 1000);
    return () => clearInterval(timer);
  }, []);

  return (
    <main className="min-h-screen flex items-center justify-center bg-black px-5 py-8">
      <div className="flex flex-col items-center gap-8 sm:gap-10 text-center">
        <Image
          src="/logotype-heure-comptes.svg"
          width={260}
          height={60}
          alt="L'heure des comptes"
          className="w-[200px] sm:w-[280px] h-auto brightness-0 invert"
        />

        <p className="text-body sm:text-lead font-bold text-white/60">
          {RELEASE_DATE.toLocaleDateString('fr-FR', {
            weekday: 'long',
            day: 'numeric',
            month: 'long',
            year: 'numeric',
            hour: '2-digit',
            minute: '2-digit',
          })}
        </p>

        {timeLeft && (
          <div
            className="flex items-start justify-center gap-1.5 sm:gap-2.5"
            aria-label="Temps restant avant le lancement"
          >
            <TimeUnit value={timeLeft.days} label="jours" />
            <Separator />
            <TimeUnit value={timeLeft.hours} label="heures" />
            <Separator />
            <TimeUnit value={timeLeft.minutes} label="minutes" />
            <Separator />
            <TimeUnit value={timeLeft.seconds} label="secondes" />
          </div>
        )}

        <p className="text-caption sm:text-body font-medium text-white/30 tracking-wide">
          {"Un projet d'Anima et Data For Good"}
        </p>
      </div>
    </main>
  );
}
