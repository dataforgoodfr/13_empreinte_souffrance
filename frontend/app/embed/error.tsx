'use client';

export default function EmbedError() {
  return (
    <div className="flex items-center justify-center w-screen h-screen bg-gray-100">
      <div className="text-center p-8">
        <h2 className="text-xl text-gray-800">{"Une erreur est survenue"}</h2>
        <p className="text-sm text-gray-600 mb-6">
          {"La carte n'a pas pu se charger. Veuillez réessayer."}
        </p>
      </div>
    </div>
  );
}
