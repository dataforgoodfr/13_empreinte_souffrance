'use client';

import { useCurrentLocale } from '@/locales/client';
import React, { useState, ChangeEvent } from 'react';

interface BrevoFormData {
  PRENOM: string;
  NOM: string;
  EMAIL: string;
}

type Step = 'closed' | 'form' | 'success';

export default function BrevoNewsletterSection() {
  const locale = useCurrentLocale() ?? 'fr';

  const [step, setStep] = useState<Step>('closed');
  const [formData, setFormData] = useState<BrevoFormData>({
    PRENOM: '',
    NOM: '',
    EMAIL: '',
  });

  const handleChange = (event: ChangeEvent<HTMLInputElement>) => {
    const { name, value } = event.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  return (
    <section className="m-5 rounded-[5px] bg-pink-1 p-6 flex flex-col gap-6 ">
      <h3 className="text-black">Rejoindre le mouvement </h3>

      {step === 'closed' && (
        <button type="button" onClick={() => setStep('form')} className="white-button">
          Je rejoins le mouvement !
        </button>
      )}

      {step === 'form' && (
        <form
          method="POST"
          action="https://2380490f.sibforms.com/serve/MUIFAOy6vdvkWDXGcqK9LTFr53-yrlYfCJIvV-h9BbbD_lDs-CH9suIo-kk0I29W3UtwbksOkFXRbJqaMOiJTn6lqgHujB-1--fNTUYtorsHtn98Cx6yOK52FS-Kkvy5wbqbxfZtDMskJy20NQa_U4dE6zf8ZVTjz_xqUDqBQgCzT2Zi6B-7nMvdHarKbkMky6JI9EmammCY7jIC"
          data-type="subscription"
          className="mt-2 flex flex-col text-left gap-6"
        >
          <div>
            <label htmlFor="PRENOM" className="text-body ">
              Prénom
            </label>
            <input
              id="PRENOM"
              type="text"
              name="PRENOM"
              placeholder="Votre prénom"
              required
              autoComplete="given-name"
              value={formData.PRENOM}
              onChange={handleChange}
              className="w-full rounded-[5px] bg-white mt-2 px-3 py-2 text-body"
            />
          </div>

          <div>
            <label htmlFor="NOM" className="text-left text-body">
              Nom
            </label>
            <input
              id="NOM"
              type="text"
              name="NOM"
              placeholder="Votre nom"
              required
              autoComplete="family-name"
              value={formData.NOM}
              onChange={handleChange}
              className="w-full rounded-[5px] bg-white mt-2  px-3 py-2 text-body"
            />
          </div>

          <div>
            <label htmlFor="EMAIL" className="mb-1 text-body">
              Email
            </label>
            <input
              id="EMAIL"
              type="email"
              name="EMAIL"
              placeholder="vous@exemple.com"
              required
              autoComplete="email"
              value={formData.EMAIL}
              onChange={handleChange}
              className="w-full rounded-[5px] bg-white mt-2    px-3 py-2 text-body"
            />
          </div>

          {/* Honeypot (anti-spam) : champ caché */}
          <div className="hidden" aria-hidden="true">
            <input type="text" name="email_address_check" tabIndex={-1} autoComplete="off" />
          </div>

          <input type="hidden" name="locale" value={locale} />

          <button type="submit" className="white-button">
            S'inscrire
          </button>
        </form>
      )}

      {step === 'success' && <p className="mt-2 text-lead ">Merci d&apos;avoir rempli le formulaire !</p>}
    </section>
  );
}
