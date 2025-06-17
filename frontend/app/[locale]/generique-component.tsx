// Composant générique temporaire utilisé pour représenter visuellement une section de la page Méthodologie, en attendant le contenu final.
// Temporary generic component used to visually represent a section of the Methodology page while waiting for the final content.

import React from 'react';

type GenericSectionProps = {
  title: string;
  page: string;
};

export default function GenericSection({ title, page }: GenericSectionProps) {
  return (
    <section className="w-full p-20 px-4 border-b border-gray-200 bg-gradient-to-br from-blue-900 via-blue-600 to-blue-400">
      <div className="max-w-5xl mx-auto p-24">
        <h2 className="text-2xl font-bold text-white mb-6">{title}</h2>
        <div className="flex flex-col md:flex-row items-center gap-6 p-24 rounded-xl shadow-lg border border-white/20 backdrop-blur-md bg-white/30">
          <div className="w-full md:w-1/3 flex justify-center">
            <div className="w-48 h-48 rounded overflow-hidden shadow-md">
              <img src="/suffering_reduction.PNG" alt={title} className="w-full h-full object-cover" />
            </div>
          </div>
          <div className="w-full md:w-2/3 text-gray-800">
            <p>
              Ceci est un bloc pour le composant <strong>{title}</strong> de la page <strong>{page}</strong>.
              <br />
              <br />
              Le code de ce composant est à remplacer par celui de la maquette.
            </p>
          </div>
        </div>
      </div>
    </section>
  );
}
