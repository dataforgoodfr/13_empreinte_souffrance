'use client';

import { useState, useEffect, ChangeEvent, FormEvent } from 'react';
import './knowledge_panel.css';
import Image from 'next/image';
import { useI18n, useCurrentLocale } from '../../../locales/client';

type TextElement = {
  html: string;
};

type PanelElement = {
  panel_id: string;
};

type Element = {
  element_type: 'text' | 'panel';
  text_element: TextElement | null;
  panel_element: PanelElement | null;
};

type TitleElement = {
  grade: string;
  title: string;
  type: string;
  subtitle: string | null;
  name: string | null;
  icon_url: string | null;
};

type Panel = {
  elements: Element[];
  level: string;
  title_element: TitleElement;
  topics: string[];
};

type KnowledgePanelData = {
  panels: {
    [key: string]: Panel;
  };
  product?: {
    name: string | null;
    image_url: string | null;
  };
};

export default function KnowledgePanel() {
  const [selectedBarcode, setSelectedBarcode] = useState<string>('3450970045360');
  const [customBarcode, setCustomBarcode] = useState<string>('3256229237063'); // Poultry chicken barcode
  const [productName, setProductName] = useState<string | null>(null);
  const [productImageUrl, setProductImageUrl] = useState<string | null>(null);
  const [productUrl, setProductUrl] = useState<string | null>(null);
  const [APIv2URL, setAPIv2URL] = useState<string | null>(null);
  const [showCustomInput, setShowCustomInput] = useState<boolean>(false);
  const [knowledgePanelData, setKnowledgePanelData] = useState<KnowledgePanelData | null>(null);
  const [expandedPanels, setExpandedPanels] = useState<Record<string, boolean>>({});
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const locale = useCurrentLocale() as 'fr' | 'en';
  const t = useI18n();

  const barcodes = [
    '3450970045360', // cage eggs from France
    '2000000124898', // cage eggs from usa
    '8003636004529', // no specific category
    '3560071098278', // both en:free-range-chicken-eggs AND en:cage-chicken-eggs
    '3270190205685', // free-range chicken eggs from France
    '0605388714565', // no specific category
    '50326686', // cage chicken eggs from UK
    '4311501688120', // barn chicken eggs from Germany
    '4056489292395 ', // free-range eggs from Germany
    '9413000012057', // free-range eggs from New-Zealand
    '9414674989591', // cage eggs from New-Zealand
    '5202930932252', // free-range eggs, no country
    '9313715907009', //
    '5010482558413', // cage, France and UK
    '3372140000101', // cage, 2 countries
    '3302740059193', // broiler chicken
    '3256229237063',
    '0451418000005',
    '3331354307611',
    'custom',
  ];

  const barcodeNames: { [key: string]: string } = {
    '3450970045360': '10 œufs frais calibre moyen - cage France',
    '2000000124898': 'Cage eggs from USA',
    '8003636004529': 'Sans quantité',
    '3560071098278': 'Free-range & cage chicken eggs',
    '3270190205685': 'Free-range chicken eggs from France',
    '0605388714565': "Medium grade A eggs - sans mode d'elevage",
    '50326686': 'Cage chicken eggs from UK',
    '4311501688120': 'Barn chicken eggs from Germany',
    '4056489292395 ': 'Free-range eggs from Germany',
    '9413000012057': 'Free-range eggs from New-Zealand',
    '9414674989591': 'Cage eggs from New-Zealand',
    '5202930932252': 'Free-range eggs, no country',
    '9313715907009': 'Oeufs cage Australie',
    '5010482558413': 'Cage, France and UK',
    '3372140000101': 'Cage, 2 countries',
    '3302740059193': 'Poulet de chair taggué en:chickens',
    '3256229237063': 'Poulet de chair non taggué en:chickens',
    '0451418000005': 'Oeufs barn sans product_name',
    '3331354307611': 'Oeufs barn et poids sans product_name',
  };

  useEffect(() => {
    if (selectedBarcode && selectedBarcode !== 'custom') {
      fetchKnowledgePanelData(selectedBarcode);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [selectedBarcode, locale]);

  const handleBarcodeChange = (e: ChangeEvent<HTMLSelectElement>) => {
    const value = e.target.value;
    setSelectedBarcode(value);

    if (value === 'custom') {
      setShowCustomInput(true);
    } else {
      setShowCustomInput(false);
      setCustomBarcode('');
    }
  };

  const handleCustomBarcodeChange = (e: ChangeEvent<HTMLInputElement>) => {
    setCustomBarcode(e.target.value);
  };

  const handleCustomBarcodeSubmit = (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (customBarcode.trim()) {
      fetchKnowledgePanelData(customBarcode.trim());
    }
  };

  const fetchKnowledgePanelData = async (barcode: string) => {
    setIsLoading(true);
    setError(null);
    setProductName(null);
    setProductImageUrl(null);
    try {
      const response = await fetch(`http://127.0.0.1:8000/off/v1/knowledge-panel/${barcode}?lang=${locale}`);

      if (response.status === 404) {
        setError(t('KnowledgePanel.productNotFound'));
        setKnowledgePanelData(null);
        return;
      } else if (!response.ok) {
        throw new Error(`HTTP Error: ${response.status}`);
      }

      const data = await response.json();
      setKnowledgePanelData(data);

      if (data.product) {
        setProductName(data.product.name);
        setProductImageUrl(data.product.image_url);
        setAPIv2URL(`https://world.openfoodfacts.net/api/v2/product/${selectedBarcode}`);
        setProductUrl(`https://fr.openfoodfacts.org/produit/${selectedBarcode}`);
      }

      // Init panels as expanded by default
      const initialExpandedState: Record<string, boolean> = {};
      Object.keys(data.panels).forEach((panelId) => {
        initialExpandedState[panelId] = true;
      });
      setExpandedPanels(initialExpandedState);
    } catch (err) {
      setError(`Error fetching knowledge panel: ${err instanceof Error ? err.message : String(err)}`);
      setKnowledgePanelData(null);
    } finally {
      setIsLoading(false);
    }
  };

  const togglePanel = (panelId: string) => {
    setExpandedPanels((prev) => ({
      ...prev,
      [panelId]: !prev[panelId],
    }));
  };

  const renderElement = (element: Element, panelsData: { [key: string]: Panel }, isSubPanel: boolean = false) => {
    if (element.element_type === 'text' && element.text_element) {
      return <div className="my-2 panel-content" dangerouslySetInnerHTML={{ __html: element.text_element.html }} />;
    } else if (element.element_type === 'panel' && element.panel_element) {
      const subPanelId = element.panel_element.panel_id;
      const subPanel = panelsData[subPanelId];

      if (subPanel) {
        // Add margin-top if this is a sub-panel
        return <div className={isSubPanel ? 'mt-6' : ''}>{renderPanel(subPanelId, subPanel, panelsData, true)}</div>;
      }
    }

    return null;
  };

  const renderPanel = (
    panelId: string,
    panel: Panel,
    panelsData: { [key: string]: Panel },
    isSubPanel: boolean = false
  ) => {
    const { title_element, elements } = panel;
    const isExpanded = expandedPanels[panelId];

    return (
      <div key={panelId} className={`border rounded-lg mb-4 overflow-hidden shadow-sm ${isSubPanel ? 'mt-4' : ''}`}>
        <div
          className="flex items-center justify-between p-4 bg-orange-100 cursor-pointer"
          onClick={() => togglePanel(panelId)}
        >
          <div className="flex items-center space-x-3">
            {title_element.icon_url && (
              <Image // Will use the url image passed from the API
                src="/tmp_logo.webp"
                alt={title_element.title}
                width={48}
                height={48}
                className="w-6 h-6"
              />
            )}
            <div>
              <h3 className="font-semibold text-lg">{title_element.title}</h3>
              {title_element.subtitle && <p className="text-sm text-gray-600">{title_element.subtitle}</p>}
            </div>
          </div>
          {isExpanded ? <span className="text-lg">▲</span> : <span className="text-lg">▼</span>}
        </div>

        {isExpanded && (
          <div className="p-4 bg-white panel-content">
            {elements.map((element, index) => (
              <div key={index}>{renderElement(element, panelsData, isSubPanel)}</div>
            ))}
          </div>
        )}
      </div>
    );
  };

  return (
    <div className="container mx-auto p-4 max-w-4xl">
      <h1 className="text-2xl font-bold mb-6">{t('KnowledgePanel.title')}</h1>

      <div className="mb-8 p-4 bg-gray-50 rounded-lg">
        <h2 className="text-lg font-semibold mb-3">{t('KnowledgePanel.selectBarcode')}</h2>

        <select
          value={selectedBarcode}
          onChange={handleBarcodeChange}
          className="w-full p-2 border rounded focus:outline-none focus:ring-2 focus:ring-orange-200 mb-3"
        >
          {barcodes.map((barcode) => (
            <option key={barcode} value={barcode}>
              {
                barcode === 'custom'
                  ? t('KnowledgePanel.otherBarcode') // Si c'est 'custom', affiche le texte traduit
                  : barcodeNames[barcode] // Vérifie si un nom existe pour ce barcode
                    ? `${barcode} - ${barcodeNames[barcode]}` // Si oui, affiche "code - nom"
                    : barcode // Sinon, affiche juste le code
              }
            </option>
          ))}
        </select>

        {showCustomInput && (
          <form onSubmit={handleCustomBarcodeSubmit} className="mt-3">
            <div className="flex gap-2">
              <input
                type="text"
                value={customBarcode}
                onChange={handleCustomBarcodeChange}
                placeholder={t('KnowledgePanel.enterBarcode')}
                className="flex-1 p-2 border rounded focus:outline-none focus:ring-2 focus:ring-orange-200"
                pattern="[0-9]+"
                title={t('KnowledgePanel.numericBarcodeError')}
              />
              <button
                type="submit"
                className="bg-orange-500 hover:bg-orange-600 text-white px-4 py-2 rounded"
                disabled={!customBarcode.trim()}
              >
                {t('KnowledgePanel.search')}
              </button>
            </div>
          </form>
        )}
      </div>

      {/* Product info */}
      {!isLoading && (productName !== null || productImageUrl !== null) && (
        <div className="mb-8 p-4 bg-white rounded-lg border shadow-sm">
          <div className="flex flex-col md:flex-row items-start md:items-center gap-6">
            {productImageUrl && (
              <div className="flex-shrink-0">
                <Image
                  src={productImageUrl}
                  alt={productName || 'Product image'}
                  width={400}
                  height={300}
                  className="product-image"
                />
              </div>
            )}
            <div className="flex-grow">
              <h2 className="text-xl font-bold">{productName}</h2>
              {productUrl && (
                <p>
                  <a
                    href={productUrl}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-blue-600 hover:underline"
                  >
                    Fiche produit OpenFoodFacts
                  </a>
                </p>
              )}
              {APIv2URL && (
                <p>
                  <a
                    href={APIv2URL}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-blue-600 hover:underline"
                  >
                    API V2 OpenFoodFacts
                  </a>
                </p>
              )}
            </div>
          </div>
        </div>
      )}

      {isLoading && (
        <div className="text-center py-8">
          <p className="text-gray-600">{t('KnowledgePanel.loading')}</p>
        </div>
      )}

      {error && <div className="bg-red-100 text-red-700 p-4 rounded mb-4">{error}</div>}

      {knowledgePanelData && !isLoading && (
        <div className="space-y-4">
          {knowledgePanelData.panels.main &&
            renderPanel('main', knowledgePanelData.panels.main, knowledgePanelData.panels)}
        </div>
      )}
    </div>
  );
}
