"use client";

import { useState, useEffect } from "react";
import "./knowledge_panel.css";

type TextElement = {
  html: string;
};

type PanelElement = {
  panel_id: string;
};

type Element = {
  element_type: "text" | "panel";
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
};

export default function KnowledgePanel() {
  const [selectedBarcode, setSelectedBarcode] =
    useState<string>("3450970045360");
  const [customBarcode, setCustomBarcode] = useState<string>("3256229237063"); // Poultry chicken barcode
  const [showCustomInput, setShowCustomInput] = useState<boolean>(false);
  const [knowledgePanelData, setKnowledgePanelData] =
    useState<KnowledgePanelData | null>(null);
  const [expandedPanels, setExpandedPanels] = useState<Record<string, boolean>>(
    {},
  );
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const barcodes = ["3450970045360", "3270190205685", "custom"];

  useEffect(() => {
    if (selectedBarcode && selectedBarcode !== "custom") {
      fetchKnowledgePanelData(selectedBarcode);
    }
  }, [selectedBarcode]);

  const handleBarcodeChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const value = e.target.value;
    setSelectedBarcode(value);

    if (value === "custom") {
      setShowCustomInput(true);
    } else {
      setShowCustomInput(false);
      setCustomBarcode("");
    }
  };

  const handleCustomBarcodeChange = (
    e: React.ChangeEvent<HTMLInputElement>,
  ) => {
    setCustomBarcode(e.target.value);
  };

  const handleCustomBarcodeSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (customBarcode.trim()) {
      fetchKnowledgePanelData(customBarcode.trim());
    }
  };

  const fetchKnowledgePanelData = async (barcode: string) => {
    setIsLoading(true);
    setError(null);

    try {
      const response = await fetch(
        `http://127.0.0.1:8000/off/v1/knowledge-panel/${barcode}`,
      );

      if (response.status === 404) {
        setError("This product doesn't contains supported animal products");
        setKnowledgePanelData(null);
        return;
      } else if (!response.ok) {
        throw new Error(`HTTP Error: ${response.status}`);
      }

      const data = await response.json();
      setKnowledgePanelData(data);

      // Init panels as expanded by default
      const initialExpandedState: Record<string, boolean> = {};
      Object.keys(data.panels).forEach((panelId) => {
        initialExpandedState[panelId] = true;
      });
      setExpandedPanels(initialExpandedState);
    } catch (err) {
      setError(
        `Error fetching knowledge panel: ${err instanceof Error ? err.message : String(err)}`,
      );
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

  const renderElement = (
    element: Element,
    panelsData: { [key: string]: Panel },
    isSubPanel: boolean = false,
  ) => {
    if (element.element_type === "text" && element.text_element) {
      return (
        <div
          className="my-2 panel-content"
          dangerouslySetInnerHTML={{ __html: element.text_element.html }}
        />
      );
    } else if (element.element_type === "panel" && element.panel_element) {
      const subPanelId = element.panel_element.panel_id;
      const subPanel = panelsData[subPanelId];

      if (subPanel) {
        // Add margin-top if this is a sub-panel
        return (
          <div className={isSubPanel ? "mt-6" : ""}>
            {renderPanel(subPanelId, subPanel, panelsData, true)}
          </div>
        );
      }
    }

    return null;
  };

  const renderPanel = (
    panelId: string,
    panel: Panel,
    panelsData: { [key: string]: Panel },
    isSubPanel: boolean = false,
  ) => {
    const { title_element, elements } = panel;
    const isExpanded = expandedPanels[panelId];

    return (
      <div
        key={panelId}
        className={`border rounded-lg mb-4 overflow-hidden shadow-sm ${isSubPanel ? "mt-4" : ""}`}
      >
        <div
          className="flex items-center justify-between p-4 bg-orange-100 cursor-pointer"
          onClick={() => togglePanel(panelId)}
        >
          <div className="flex items-center space-x-3">
            {title_element.icon_url && (
              <img
                src={title_element.icon_url}
                alt={title_element.title}
                className="w-6 h-6"
              />
            )}
            <div>
              <h3 className="font-semibold text-lg">{title_element.title}</h3>
              {title_element.subtitle && (
                <p className="text-sm text-gray-600">
                  {title_element.subtitle}
                </p>
              )}
            </div>
          </div>
          {isExpanded ? (
            <span className="text-lg">▲</span>
          ) : (
            <span className="text-lg">▼</span>
          )}
        </div>

        {isExpanded && (
          <div className="p-4 bg-white panel-content">
            {elements.map((element, index) => (
              <div key={index}>
                {renderElement(element, panelsData, isSubPanel)}
              </div>
            ))}
          </div>
        )}
      </div>
    );
  };

  return (
    <div className="container mx-auto p-4 max-w-4xl">
      <h1 className="text-2xl font-bold mb-6">Knowledge Panel</h1>

      <div className="mb-8 p-4 bg-gray-50 rounded-lg">
        <h2 className="text-lg font-semibold mb-3">
          Sélectionner un code-barres
        </h2>

        <select
          value={selectedBarcode}
          onChange={handleBarcodeChange}
          className="w-full p-2 border rounded focus:outline-none focus:ring-2 focus:ring-orange-200 mb-3"
        >
          {barcodes.map((barcode) => (
            <option key={barcode} value={barcode}>
              {barcode === "custom" ? "Autre code-barres..." : barcode}
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
                placeholder="Entrez un code-barres"
                className="flex-1 p-2 border rounded focus:outline-none focus:ring-2 focus:ring-orange-200"
                pattern="[0-9]+"
                title="Veuillez saisir un code-barres numérique"
              />
              <button
                type="submit"
                className="bg-orange-500 hover:bg-orange-600 text-white px-4 py-2 rounded"
                disabled={!customBarcode.trim()}
              >
                Rechercher
              </button>
            </div>
          </form>
        )}
      </div>

      {isLoading && (
        <div className="text-center py-8">
          <p className="text-gray-600">Chargement des données...</p>
        </div>
      )}

      {error && (
        <div className="bg-red-100 text-red-700 p-4 rounded mb-4">{error}</div>
      )}

      {knowledgePanelData && !isLoading && (
        <div className="space-y-4">
          {knowledgePanelData.panels.main &&
            renderPanel(
              "main",
              knowledgePanelData.panels.main,
              knowledgePanelData.panels,
            )}
        </div>
      )}
    </div>
  );
}
