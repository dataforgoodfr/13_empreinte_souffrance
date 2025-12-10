'use client';

import { useCurrentLocale } from '@/locales/client';
import clsx from 'clsx';
import Link from 'next/link';
import React, { useState, ChangeEvent } from 'react';

interface BrevoFormData {
  PRENOM: string;
  NOM: string;
  EMAIL: string;
  email_address_check: string;
  locale: string;
}

export default function BrevoNewsletterForm() {
  const locale = useCurrentLocale();

  const [formData, setFormData] = useState<BrevoFormData>({
    PRENOM: '',
    NOM: '',
    EMAIL: '',
    email_address_check: '',
    locale: locale,
  });

  const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const showNameFields = formData.EMAIL.trim().length > 0;

  return (
    <form
      method="POST"
      action="https://2380490f.sibforms.com/serve/MUIFAOy6vdvkWDXGcqK9LTFr53-yrlYfCJIvV-h9BbbD_lDs-CH9suIo-kk0I29W3UtwbksOkFXRbJqaMOiJTn6lqgHujB-1--fNTUYtorsHtn98Cx6yOK52FS-Kkvy5wbqbxfZtDMskJy20NQa_U4dE6zf8ZVTjz_xqUDqBQgCzT2Zi6B-7nMvdHarKbkMky6JI9EmammCY7jIC"
      data-type="subscription"
      className="mx-5 px-3 mb-5 pb-3"
    >
      <div className="flex flex-wrap justify-center items-center gap-3.5 mb-1">
        <div>
          <div
            className={clsx('overflow-hidden transition-all duration-800 ease-out', {
              'h-0': !showNameFields,
              'h-34': showNameFields,
            })}
          >
            <div
              className={clsx('flex flex-col items-center gap-3.5 w-full transition-all duration-800 ease-out', {
                'opacity-0 translate-y-12': !showNameFields,
                'opacity-100 translate-y-0': showNameFields,
              })}
            >
              <input
                type="text"
                tabIndex={showNameFields ? 0 : -1}
                className={clsx('border-2 border-pink-3 rounded-[10px] text-pink-3 p-4 font-black w-48', {
                  'pointer-events-none': !showNameFields,
                  'pointer-events-auto': showNameFields,
                })}
                name="PRENOM"
                placeholder="Prénom"
                required
                value={formData.PRENOM}
                onChange={handleChange}
              />

              <input
                type="text"
                tabIndex={showNameFields ? 0 : -1}
                className={`border-2 border-pink-3 rounded-[10px] text-pink-3 p-4 font-black w-48
                              ${showNameFields ? 'pointer-events-auto' : 'pointer-events-none'}
                  `}
                name="NOM"
                placeholder="Nom"
                required
                value={formData.NOM}
                onChange={handleChange}
              />
            </div>
          </div>
          <input
            type="email"
            className="border-2 border-pink-3 rounded-[10px] text-pink-3 p-4 font-black w-48"
            name="EMAIL"
            placeholder="Email"
            required
            value={formData.EMAIL}
            onChange={handleChange}
          />
        </div>

        {/* Required Brevo fields */}
        <input
          type="text"
          name="email_address_check"
          value={formData.email_address_check}
          style={{ display: 'none' }}
          readOnly
        />

        <input type="hidden" name="locale" value={formData.locale} />

        <button type="submit" className="pink-3-button w-48">
          S’inscrire
        </button>
      </div>
      <span className="text-xs text-white" style={{ fontStyle: 'italic' }}>
        En soumettant ce formulaire, vous acceptez le traitement de vos données personnelles par Brevo selon sa{' '}
        <Link
          href="https://www.brevo.com/fr/legal/privacypolicy/"
          className="underline"
          style={{ fontStyle: 'italic' }}
        >
          politique de confidentialité
        </Link>
        .
      </span>
    </form>
  );
}
