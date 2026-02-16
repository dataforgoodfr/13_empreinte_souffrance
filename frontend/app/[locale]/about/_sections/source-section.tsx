export default async function SourceSection() {
  return (
    <section className="p-section  bg-grey text-black  ">
      <div className="max-w-[900px] gap-12 mx-auto flex flex-col items-start justify-center">
        {' '}
        <h2>SOURCES</h2>
        {/* ------- Enquête en supermarchés -------- */}
        <div id="proportion_market_visited" className="max-w-contain flex flex-col items-start justify-center gap-6">
          <h3>Enquête en supermarchés</h3>
          <p>
            Retrouvez la liste de tous les supermarchés visités ici :{' '}
            <a
              className="underline"
              href="https://docs.google.com/spreadsheets/d/104TB_u3znzFcsFlUDJ1rMeGN_QBnPwfebiZDtRSwSCw/edit?gid=0#gid=0"
            >
              Supermarchés visités
            </a>
          </p>
          <div className="max-w-contain flex flex-col items-start justify-center gap-2 lg:max-w-2/3 body">
            <p className=" font-bold">Périmètre de l'enquête</p>
            <p>
              L'enquête porte sur les supermarchés et hypermarchés appartenant à huit enseignes : Leclerc, Carrefour,
              Intermarché, U, Auchan, Lidl, Monoprix (groupe Casino) et Aldi. Seuls les points de vente de plus de 400
              m² ont été inclus, ce qui exclut les formats de proximité tels que Franprix ou Carrefour Express. Ces
              canaux de distribution représentent plus de 75 % des achats alimentaires en France.
            </p>
            <p className="font-bold">Collecte des données</p>
            <p>
              545 magasins ont été initialement visités : environ 200 par l'équipe salariée d'Anima et plus de 300 par
              des bénévoles. Les données ont été recueillies via un formulaire en ligne. Les répondants devaient
              renseigner pour chaque visite : le nom de l'enseigne, l'adresse du point de vente, la présence ou
              l'absence d'œufs cage en rayon, ou l'impossibilité de statuer en raison d'un rayon insuffisamment garni.
              Des preuves photographiques des passages en rayon étaient systématiquement demandées.
            </p>
            <p>
              L'équipe salariée a utilisé l'application CertiPhoto, qui certifie l'heure, la date et le lieu de prise de
              chaque photographie. La valeur de cet outil a déjà été reconnue par un tribunal qui l’a intégré
              positivement dans la jurisprudence.
            </p>
            <p className="font-bold">Critères de classification</p>
            <p>
              Un magasin était considéré comme vendant des œufs de cage si au moins l'un des éléments suivants était
              identifié :
            </p>
            <ul className="pl-8 list-disc">
              <li>Une boîte d'œufs portant la mention « élevage en cage », « Code 3 » ou « 3FR »</li>
              <li>Une étiquette en rayon indiquant « œufs cage »</li>
              <li>Un carton de boîtes d'œufs indiquant « œufs cage »</li>
            </ul>
            <p>
              Un magasin était considéré comme ne vendant pas d'œufs de cage si toutes les boîtes d'œufs et toutes les
              étiquettes en rayon indiquaient explicitement un mode d'élevage hors cage (sol, plein air ou bio). En cas
              d'étiquette ambiguë, une confirmation a été demandée directement à l’enseigne.
            </p>
            <p className="font-bold">Traitement et validation des données</p>
            <p>
              Les retours des bénévoles ont été systématiquement vérifiés par l'équipe salariée. Des demandes de
              clarification ont été formulées lorsque nécessaire.
            </p>
            <p>
              Sur les 545 magasins visités, 386 ont été retenus pour l'analyse finale. Les exclusions résultent soit
              d'un rayon œufs insuffisamment garni pour permettre une classification, soit de retours bénévoles
              incomplets ou peu clairs.
            </p>
            <p className="font-bold">
              Définition d’une référence d’œufs cage (pour le comptage du nombre de références d’œufs cage vendues)
            </p>
            <p>
              Une référence d'œufs de cage correspond à une combinaison unique de marque et de conditionnement. Par
              exemple, des boîtes d'œufs cage Matines de 6, des boîtes d’œufs cage Matines de 12 et des boîtes Simpl de
              30 œufs cage constituent trois références distinctes.
            </p>
            <p className="font-bold">Données complémentaires fournies par les enseignes</p>
            <p>
              En complément de l'enquête de terrain, et afin de précisément refléter la réalité de la transition hors
              cage du secteur, les enseignes ont été sollicitées pour communiquer la part d'œufs de cage dans leur
              volume de ventes pour le mois de septembre 2025. Ce mois a été choisi pour garantir un recul suffisant
              permettant la consolidation des données.
            </p>
            <p>
              Trois enseignes ont transmis leurs chiffres : Aldi a déclaré être à 97,8 % hors cage en septembre 2025,
              Intermarché 98 % hors cage sur ses achats nationaux (excluant les achats directs locaux représentant une
              part très faible selon l'enseigne), et le groupe Casino a indiqué que Monoprix atteignait 98 % hors cage à
              cette période.
            </p>
            <p className="font-bold">Non-conformités réglementaires observées</p>
            <p>
              Certaines boîtes d'œufs cage identifiées durant l'enquête sont non conformes à la réglementation
              européenne. Cette réglementation impose l'indication en toutes lettres du mode d'élevage sur l'emballage.
            </p>
            <p>Deux niveaux de non-conformité ont été observés :</p>
            <p>
              Non-conformité majeure : Des boîtes d'œufs ne mentionnant aucun mode d'élevage sur l'emballage, pas même
              le Code 3 qui correspond à l’élevage cage. Le consommateur ne peut identifier qu'il s'agit d'œufs de cage
              qu'en ouvrant la boîte et en consultant le code imprimé directement sur les œufs.
            </p>
            <p>
              Non-conformité probable : D'autres boîtes indiquent le code 3 sur l'emballage sans mentionner
              explicitement « élevage en cage » en toutes lettres, ce qui est pourtant obligatoire
            </p>
            <p>Un signalement sera transmis à la DGCCRF concernant les cas de non-conformité majeure.</p>
          </div>
        </div>
        {/* /* ------- Enquête sur les œufs ingrédients /* ------- */}
        <div id="proportion_cake_caged_eggs" className="max-w-contain flex flex-col items-start justify-center gap-6">
          <h3>Enquête sur les œufs ingrédients dans les brioches, gâteaux… de marque distributeur</h3>
          <p>
            Les résultats détaillés de l’enquête sont à retrouver ici :{''}
            <a
              className="underline"
              href="https://docs.google.com/spreadsheets/d/104TB_u3znzFcsFlUDJ1rMeGN_QBnPwfebiZDtRSwSCw/edit?gid=0#gid=0"
            >
              Enquête œufs ingrédients des brioches, gâteaux... de marque distributeur
            </a>
          </p>
          <div className="max-w-contain flex flex-col items-start justify-center gap-2 lg:max-w-2/3 body">
            <p className=" font-bold">Sélection des produits</p>
            <p>25 références génériques communes à l'ensemble des enseignes ont été sélectionnées :{''}</p>
            <p>
              Cake aux fruits, Boudoir, Barquette chocolat noisette, Brownie, Petit lapin/petit ourson au chocolat,
              Goûter moelleux chocolat coco, Goûter cœur fondant fraise, Goûter marbré chocolat, Crêpe fourrée chocolat,
              Barre pâtissière nature, Quatre-quarts, Madeleines nature, Madeleines pépites de chocolat / marbrées
              chocolat, Ravioli frais au bœuf (frigo), Tagliatelles fraîches (frigo), Coquillettes fraîches aux œufs
              (tempéré), Quenelles fraiches, Tortilla, Chinois à la crème pâtissière, Pains au lait, Brioche tranchée,
              Flan aux œufs, Cœur fondant chocolat, Crème brûlée, Crème au chocolat aux œufs
            </p>
            <p>
              La sélection s'est concentrée sur les quatre catégories de produits utilisant le plus d'œufs parmi
              l’ensemble de leurs produits, selon les informations fournies par l'un des distributeurs :{''}
            </p>

            <ol className="pl-8 list-decimal">
              <li>Pâtisseries industrielles</li>
              <li>Desserts aux œufs (crème aux œufs, îles flottantes)</li>
              <li>Viennoiseries, brioches et pain au lait</li>
              <li>Pâtes aux œufs</li>
            </ol>
            <p>
              Pour chacun de ces 25 produits génériques, une référence de marque distributeur correspondante a été
              identifiée dans chaque enseigne. Par exemple, pour le produit générique "Crêpe fourrée chocolat", la
              référence spécifique chez Leclerc est "Crêpes fourrées P'tit déli Chocolat”. Seules les marques
              distributeurs de cœur de gamme ont été retenues, excluant les marques distributeurs premier prix ainsi que
              les marques distributeurs premium.
            </p>
            <p className="font-bold">Méthode de vérification du mode d’élevage des oeufs</p>
            <p className="font-bold">Enquête en ligne</p>
            <p>
              Une vérification a été effectuée sur le site internet de chaque enseigne. Un produit était considéré comme
              contenant exclusivement des œufs hors cage (plein air ou sol) si l'une des conditions suivantes était
              remplie :
            </p>
            <ul className="pl-8 list-disc">
              <li>La photographie du produit sur le site mentionnait un mode d'élevage hors cage</li>
              <li>La liste des ingrédients affichée en ligne mentionnait un mode d'élevage hors cage</li>
            </ul>
            <p>
              Lorsqu'il fallait se géolocaliser pour avoir accès au drive d'une enseigne, nous nous sommes géolocalisés
              à Montreuil en Seine-Saint-Denis.
            </p>
            <p>
              Une vérification préalable avait confirmé la correspondance entre les informations présentes sur les
              emballages physiques en magasin et celles disponibles en ligne sur les sites des distributeurs.
            </p>
            <p>
              Lorsque plusieurs références correspondaient à un même produit générique au sein d'une enseigne (par
              exemple, plusieurs madeleines de marques distributeurs de cœur de gamme chez Carrefour), la priorité a été
              donnée à la référence affichant un mode d'élevage hors cage, si au moins l'une d'entre elles présentait
              cette mention.
            </p>
            <p className="font-bold">Contact direct avec les enseignes</p>
            <p>
              Puis, pour les produits ne portant pas d'indication explicite de mode d'élevage hors cage, un contact a
              été établi directement avec les distributeurs afin d'obtenir des informations complémentaires. Plusieurs
              distributeurs ont fourni ces précisions, permettant de compléter l'enquête.
            </p>
          </div>
        </div>
        {/* ------- Evolution du pourcentage de poules en cage ------- */}
        <div id="proportion_caged_hen" className="max-w-contain flex flex-col items-start justify-center gap-6">
          <h3>évolution du pourcentage de poules en cage en France</h3>
          <p>Nous avons utilisé les données du CNPO (interprofession des œufs) :{''}</p>
          <ul className="pl-8 list-disc">
            <li>
              <a
                className="underline"
                target="_blank"
                href="https://lesoeufs.fr/la-filiere-francaise-avance-a-grands-pas-dans-la-transition-13-de-poules-hors-cages-entre-2016-et-2017/"
              >
                67% de poules en cage en 2016
              </a>
            </li>
            <li>
              <a
                className="underline"
                target="_blank"
                href="https://lesoeufs.fr/la-filiere-francaise-avance-a-grands-pas-dans-la-transition-13-de-poules-hors-cages-entre-2016-et-2017/"
              >
                63,3% en 2017
              </a>
            </li>
            <li>
              <a
                className="underline"
                target="_blank"
                href="https://lesoeufs.fr/la-filiere-francaise-des-oeufs-a-releve-son-defi-de-la-transition-deja-plus-d1-poule-sur-2-elevee-hors-cage/#:~:text=De%202018%20%C3%A0%202019%2C%20le,47%25%20de%20la%20production%20fran%C3%A7aise."
              >
                55% en 2018
              </a>
            </li>
            <li>
              <a
                className="underline"
                target="_blank"
                href="https://lesoeufs.fr/la-filiere-des-oeufs-poursuit-sa-transition-et-confirme-sa-position-de-n1-de-la-production-doeufs-en-europe/"
              >
                47% en 2019
              </a>
            </li>
            <li>
              <a
                className="underline"
                target="_blank"
                href="https://lesoeufs.fr/la-filiere-des-oeufs-poursuit-sa-transition-et-confirme-sa-position-de-n1-de-la-production-doeufs-en-europe/"
              >
                36% en 2020
              </a>
            </li>
            <li>
              <a
                className="underline"
                target="_blank"
                href="https://lesoeufs.fr/plus-des-2-3-des-poules-en-elevages-alternatifs/"
              >
                33% en 2021
              </a>
            </li>
            <li>
              <a
                className="underline"
                target="_blank"
                href="https://lesoeufs.fr/plus-des-2-3-des-poules-en-elevages-alternatifs/"
              >
                23% en 2022
              </a>
            </li>
            <li>
              <a
                className="underline"
                target="_blank"
                href="https://lesoeufs.fr/wp-content/uploads/2024/12/DP_CNPO_OCTOBRE_val_BD.pdf"
              >
                27% en 2023
              </a>
            </li>
            <li>
              <a className="underline" target="_blank" href="https://oeuf-info.fr/les-chiffres-cles/">
                25% en 2024
              </a>
            </li>
          </ul>
        </div>
        {/* ------- Evolution de la vente d’œufs ------- */}
        <div id="eggs_sales_farming_method" className="max-w-contain flex flex-col items-start justify-center gap-6">
          <h3>Evolution de la vente d’œufs selon le mode d’élevage</h3>
          <p>Chiffres communiqués directement par l’ITAVI, d’après WorldPanel pour FranceAgriMer.</p>
        </div>
        {/* ------- Dates des engagements  ------- */}
        <div id="market_commitment_date" className="max-w-contain flex flex-col items-start justify-center gap-6">
          <h3>Dates des engagements hors cage des enseignes</h3>
          <p>
            Lien vers les engagements hors cage : {''}
            <a
              className="underline"
              target="_blank"
              href="https://www.lineaires.com/la-distribution/poules-en-cage-l-effet-domino#:~:text=En%20janvier%202017,ce%2010%20janvier"
            >
              Leclerc,{' '}
            </a>
            <a
              className="underline"
              target="_blank"
              href="https://www.huffingtonpost.fr/life/article/carrefour-va-arreter-de-vendre-des-ufs-de-poules-elevees-en-cage_90955.html"
            >
              Carrefour,{' '}
            </a>
            <a
              className="underline"
              target="_blank"
              href="https://www.quechoisir.org/actualite-oeufs-de-poules-en-cage-des-distributeurs-disent-stop-n23757/"
            >
              Intermarché,{' '}
            </a>
            <a
              className="underline"
              target="_blank"
              href="https://www.lsa-conso.fr/systeme-u-s-engage-a-ne-plus-vendre-d-oeufs-de-poule-elevees-en-cage-pour-sa-mdd-d-ici-a-2020,247602"
            >
              U,{' '}
            </a>
            <a
              className="underline"
              target="_blank"
              href="https://www.lefigaro.fr/flash-eco/2017/04/14/97002-20170414FILWWW00042-auchan-ne-vendra-plus-d-ufs-de-poules-en-cage.php"
            >
              Auchan,{' '}
            </a>
            <a
              className="underline"
              target="_blank"
              href="https://www.lafranceagricole.fr/2016/article/776953/lidl-france-annonce-larrt-des-ufs-de-poules-leves-en-cage"
            >
              Lidl,{' '}
            </a>
            <a
              className="underline"
              target="_blank"
              href="https://www.tf1info.fr/conso-argent/fini-les-oeufs-de-poules-en-batterie-chez-monoprix-cage-plein-air-bio-rappel-des-codes-1508102.html"
            >
              Monoprix,{' '}
            </a>
            <a
              className="underline"
              target="_blank"
              href="https://www.ouest-france.fr/europe/allemagne/son-tour-aldi-promet-den-finir-avec-les-oeufs-de-batterie-4402574"
            >
              {' '}
              et ALDI,{' '}
            </a>
          </p>
        </div>
      </div>
    </section>
  );
}
