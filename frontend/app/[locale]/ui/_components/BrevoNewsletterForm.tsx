'use client';

import { useCurrentLocale } from '@/locales/client';
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

  return (
    <form
      method="POST"
      action="https://2380490f.sibforms.com/serve/MUIFAOy6vdvkWDXGcqK9LTFr53-yrlYfCJIvV-h9BbbD_lDs-CH9suIo-kk0I29W3UtwbksOkFXRbJqaMOiJTn6lqgHujB-1--fNTUYtorsHtn98Cx6yOK52FS-Kkvy5wbqbxfZtDMskJy20NQa_U4dE6zf8ZVTjz_xqUDqBQgCzT2Zi6B-7nMvdHarKbkMky6JI9EmammCY7jIC"
      data-type="subscription"
      className="m-5 p-3 bg-white"
    >
      <h3>Inscription au mouvement</h3>

      <div>
        <input
          type="text"
          name="PRENOM"
          placeholder="Prénom"
          required
          value={formData.PRENOM}
          onChange={handleChange}
        />
      </div>

      <div>
        <input type="text" name="NOM" placeholder="Nom" required value={formData.NOM} onChange={handleChange} />
      </div>

      <div>
        <input type="email" name="EMAIL" placeholder="Email" required value={formData.EMAIL} onChange={handleChange} />
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

      <button type="submit" className="primary-button">
        S’inscrire
      </button>
    </form>
  );
}
