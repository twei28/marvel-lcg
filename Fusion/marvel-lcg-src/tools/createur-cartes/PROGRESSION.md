# Createur de cartes : etat d'avancement

Objectif : un createur de cartes Marvel Champions maison, « en mieux » que https://champions-card-maker.pages.dev/ (Landstander) :
**bilingue FR/EN, rendu plus fidele, plus simple et plus rapide**, tous ses types de cartes (23), fonctionnel a 100 %.
Decisions de l'utilisateur et methode : voir la memoire `createur-de-cartes-chantier`. Credits a ajouter sur la page credits :
Landstander (outil), Hitch et les createurs de templates.

## Methode
On ne copie pas le code de Landstander. On **mesure** sa page rendue (positions, polices, matrices, couleurs) avec Chromium, on en tire
`public/createur-cartes/donnees/types.json`, et on ecrit NOTRE rendu canvas. Calques PNG et polices : recuperes de son site (accord de
l'utilisateur), copies dans `public/createur-cartes/img/` et `polices/`.

## Fichiers
- `public/createur-cartes/rendu.js` : pile de calques (teinte par role = forme pleine a l'alpha du calque, `gradient` = degrade CSS « to right top » decoupe par le masque, **visible HORS de la fenetre du masque**), illustration (`photo` derriere, `photofront` devant). Paysage : calques pivotes d'un quart de tour horaire.
- `public/createur-cartes/polices.js` : @font-face de toutes les polices (memes familles que Landstander), `ICONES` = lettres de ChampionsIcons.
- `public/createur-cartes/texte.js` : mini-HTML (`<b> <i> <em> <u> <code> [energy] <br> <hr>`), mise en page par ligne avec **contrainte de largeur par ligne** (coins coupes), `ajuster` (reduction auto), `dessinerPage`.
- `public/createur-cartes/carte.js` : `dessinerCarte(canvas, spec, contenu, etat)` : calques, puis nombres, lignes (titre, ligne d'ensemble, createur), flux traits/regles/citation. Chaine de transformations (rotate/scale/translate/matrix + origine) recomposee comme CSS.
- `public/createur-cartes/donnees/types.json` (genere) et `palettes.json` (316 palettes : 74 heros avec left_color/right_color/..., 242 vilains avec background_upper/lower, shading, accent, outer, middle, cracks).
- `tools/createur-cartes/` : `mesurer-*.mjs` (sondes Playwright sur le site de Landstander), `generer-specs.py <mesures.json>` (=> types.json ; lit aussi `arbre.json` a cote), `mesures/` (arbre.json, mesures.json, types-options.json), `reference/` (captures de reference, GITIGNORE : regenerables avec les sondes), `essai/` (banc d'essai).

## Banc d'essai (comparer au modele)
1. `python3 -m http.server 8765 --directory Fusion/marvel-lcg-src/public/createur-cartes` (le dossier `_essai/` est gitignore : y copier `essai/essai.html`, `reference/kamala-photo.png` et `kamala-photo-paysage.png`).
2. `node tools/createur-cartes/essai/rendre-tout.mjs <dossier-sortie> [types...]` (adapter les chemins : il lit `types-options.json` et ecrit `mine/<type>.png`), comparer a `reference/<type>.png` cote a cote (PIL).

## Fait (compare au modele)
- Calques et couleurs : les 23 types, hero et vilain, paysage compris.
- Texte : titre (petites capitales, icone « unique »), traits (KomikaTitle majuscules), regles (gras/italique/icones), citation, ligne d'ensemble, createur, **flux** traits->regles->citation (ecarts 20/30 px), ajustement automatique, **coins coupes** (`pinchleft/pinchright`, polygones dans `FORMES`).
- Constat : le libelle du type (ALLY, VILLAIN, MAIN SCHEME...) est **dans l'image du calque** ; `typestr` n'est que l'option « Overwrite card type ».

- **Coins coupes** (fait) : formes `shape-outside` mesurees (`clipPath` garde dans types.json), la ligne evite la forme sur toute sa hauteur, regles + citation se reduisent d'un meme facteur pour tenir dans le panneau (en dessous de leur propre rendu, qui deborde).
- **Nombres** (fait, compare au modele avec les MEMES valeurs) : filtre `codeshadow` (contour noir 4 px + 4 ombres en cascade), etoile (taille, ecart, decalage mesures par element), etoile seule, degats consequents, menace de depart, accélération, cible, phase (numero + lettre), PV, renforts (ancre a droite, pas 95, fond noir `sidescheme/boostbox<N>.png`), 3 ressources, attachement (boites ATK/SCH + titre qui monte : 1865/1560/1310).
- Piege : la boite d'un element mesuree a vide peut faire 0 de haut -> `ajouter-nombres.py` reprend boite et origine de l'etat REMPLI.

## Banc d'essai « nombres »
1. `node tools/createur-cartes/mesures/mesurer-nombres.mjs <dossier> [types]` (+ `ETOILE=0 SUFFIXE=-sans`) : remplit tous les champs sur le site de reference (une page neuve par type : la rotation paysage se casse sinon), ecrit `ref-nombres/<type>.png|json`. ~25 s par type.
2. `python3 tools/createur-cartes/ajouter-nombres.py <dossier>/ref-nombres <dossier>/ref-nombres-sans` : met a jour types.json (etoile, phase, renforts, ressources, boites).
3. `node tools/createur-cartes/essai/rendre-nombres.mjs <dossier> [types]` : rend nos cartes avec les valeurs relues dans les json -> `mine-nombres/`. Comparer cote a cote.

- **Ecarts fins** (fait) : hauteur des traits = boite mesuree, ecarts entre blocs mesures, gras des regles = 500, etoile des nombres en italique gras, etape du vilain (`villainstagenew`).
- **Variantes** (fait, comparees a la reference avec les cases cochees) : fissures on/off (`*-nocracks.png`), eclat de la tete + variante etoile (`splash*-star.png`), etoile des PV (pseudo-element mesure), tete d'angle (zoom/x/y/rotation, au-dessus des nombres ; `etat.tete = {image, afficher, etoile, zoom, x, y, rotation}`, `etat.fissures`), promos (fonds blancs/noirs du panneau, bulle de PV posee, `base-ally` des qu'une valeur THW existe, traits hors panneau).
- Sondes : `mesures/mesurer-nombres.mjs`, `mesurer-renforts.mjs`, `essai/rendre-nombres.mjs`, `essai/rendre-variantes.mjs` ; `ajouter-nombres.py` regenere tout ce qui vient des releves (apres `generer-specs.py`).

## Reste a faire (dans cet ordre)
1. **Promos** : bordure / ombre noire du panneau blanc (non mesuree), ligne d'ensemble des promos.
2. **Types a verifier un par un** contre la reference avec le banc « nombres » : obligation-villain, treachery, environment, support, upgrade, starter-deck (rendu de la liste), alter-ego-promo.
3. **Bilingue** : libelle du type baked en anglais -> pour le FR, recouvrir la bande (echantillonner la couleur du calque) et redessiner le libelle FR (ALLIE, EVENEMENT, AMELIORATION, SOUTIEN, RESSOURCE, HEROS, ALTER-EGO, MECHANT, SBIRE, TRAHISON, ENVIRONNEMENT, ATTACHEMENT, MANIGANCE PRINCIPALE/ANNEXE, OBLIGATION) ; textes FR/EN par carte, traits via `ui-app/src/board/traits-fr.ts`, ligne d'ensemble FR (« TAILLE DE MAIN 6 / POINTS DE VIE 10 »).
4. **Interface** (page `public/createur-cartes.html` ou `index.html`) : liste de cartes, choix du type, formulaire guide par type avec valeurs par defaut, apercu en direct, palettes (aspects Basic/Agression/Direction/Protection/Justice/Pool + presets heros et vilains), illustration (zoom/position/rotation, avant/arriere, glisser), sauvegarde JSON + navigateur, export PNG/JPG/WebP (taille reglable, fond perdu), export des deux langues, impression PDF, tables (TTS/OCTGN/DragnCards si utile).
5. Bouton dans l'en-tete (`public/js/prepare/lien-admin.js`, a cote de « Atelier de couvertures »), cle EN, `nouveautes.js`, page credits, tests Chromium de chaque type, optimisation des PNG (18 Mo -> webp sans perte).

## Fait ensuite (29/10)
Page `public/createur-cartes.html` + `public/createur-cartes/app.js` (liste de cartes, formulaire par type, aperçu, couleurs/aspects, illustration, tête d'angle, FR/EN, exports PNG/JPG/WebP + FR+EN + fond perdu, planche à imprimer, planche TTS, sauvegarde IndexedDB + .json), bouton admin (`lien-admin.js`), crédits, nouveautés, calques en WebP sans perte (16 -> 7,6 Mo, `optimiser-images.py`). Testé dans Chromium (23 types, langues, exports, import/export du projet, impression, TTS). Non fait : OCTGN / DragnCards.

## Idées retenues par l'utilisateur (29/10) : « pas une copie de Landstander, des trucs en plus »
1. **Calques PNG libres** : plusieurs PNG posés sur la carte, déplaçables, zoom, rotation, ordre, opacité, miroir, couleur (teinte), contour/ombre, + bibliothèque d'icônes prêtes.
2. **Confort** : annuler / rétablir (Ctrl+Z / Ctrl+Y), contrôle de lisibilité (texte trop réduit, débordement, nombre illisible), modèles de cartes.
3. **Contenu** : verso de carte et recto-verso, pack complet d'un héros (vue qui regroupe ses cartes, export en un clic), export pour le jeu (carte custom jouable).
4. **Création** : recadrage d'image assisté (détourage, tête d'angle), styles de cadre alternatifs (pleine illustration, sans cadre, cadre sombre).
5. **Sauvegarde / reprise** : sauvegarde auto + historique des versions, dossiers par héros, cartes gardées SUR LE SERVEUR du jeu.
6. **Comptes « créateur »** : invitation par l'admin (lien « créateur »), accès limité au seul créateur de cartes (ni le jeu ni l'admin), chaque créateur ne voit que SES cartes, l'admin voit tout. A faire côté serveur ; rien ne se déploie sans le mot « déploie ».
Non retenues : import depuis le jeu, traduction assistée, mots-clés prêts à insérer.

## Ajouts demandes ensuite (29/10)
- **Import des fichiers du Card Maker de reference** (fait) : leur « Save card » = un .json par carte (UTF-8 + BOM, cles a plat : selectType, title, rules, paycost..., images en data URL), leur « Save .zip » = un .json par carte dans un zip. `app.js` lit les deux (`carteDepuisReference`, `lireZip`). Leur derniere mise a jour : aout 2026 (version 2026.2) ; avant : mai, avril, mars... 2026.
- **Editeur de texte sans balises** : selectionner puis cliquer (gras, italique, souligne, taille, couleur, icones en un clic) ; pour les regles et la citation. Le texte garde le mini-HTML en interne.
- **Autres retenues** : clic direct sur la carte pour editer ; ajustement auto + reglage manuel de la taille d'un bloc ; styles reutilisables ; chercher / remplacer sur une carte, tout un heros ou tout le set (FR et EN).

## Styles de texte en un clic (decide avec l'utilisateur le 29/10)
Familles voulues : declencheurs d'action (Action, Reaction forcee... en gras + « : »), phrase d'ambiance (italique), mots-cles du jeu, limites et rappels, conditions et prerequis, lignes d'effet de heros, mots des cartes de rencontre (avec icones), styles perso reutilisables.
Choix dans l'editeur : menu « Styles » avec apercu ET saisie rapide « / » (liste cherchable). Les mots suivent la langue de la carte ; un mot-cle insere sa phrase de rappel officielle (FR et EN).
**ATTENTION vocabulaire FR** : ne JAMAIS le deviner. Exemple d'erreur corrigee par l'utilisateur : Surge = **Renfort** en FR (pas « Surtension »). Source des mots FR : `public/js/traduction/textes-fr*.js`, les scans FR et `docs/reference/mots-cles/` ; liste a faire valider par l'utilisateur pour tout mot sans source.

## Idee de l'utilisateur (29/10) : « voir une vraie carte comparable »
Un bouton a cote de l'apercu cherche dans le catalogue une carte OFFICIELLE ANGLAISE du meme type, au nombre de mots proche et au meme style (declencheurs, citation), et montre son texte (scan recadre) a la meme echelle, pour juger la longueur et la taille. Source : `data/cards.json` (type, texte) + `assets/pics-hd/<code>.jpg`. A DECIDER : les comptes createur n'ont acces qu'au createur ; montrer des scans officiels demande une route dediee (et la question des droits sur les scans pour des createurs exterieurs).

## ETAT AU 29/10 (fin de session) : a lire en premier pour reprendre
**Fait et teste dans Chromium** (page `public/createur-cartes.html`, modules dans `public/createur-cartes/`) :
- rendu des 23 types (compare a la reference ET a une vraie carte officielle : Valkyrie 25001a ; regles a 70/59 de la taille de la reference) ; page en ANGLAIS par defaut, FR d'un clic (`i18n.js`, dictionnaire FR->EN + motifs) ; cartes en anglais par defaut ; bilingue FR/EN des cartes (libelle du type, traits, textes par defaut).
- calques PNG libres (`libres.js`, `panneau-libres.js`), annuler / retablir, versions auto (IndexedDB, 10), dossiers, recherche, modeles, chercher / remplacer, appliquer au dossier, lisibilite (alertes), taille manuelle du texte, styles de cadre (sombre, pleine illustration), editeur de texte sans balises (`app.js` editeurRiche), styles de texte en un clic + saisie « / » (`styles-texte.js`, mots OFFICIELS extraits par `extraire-styles.py`), clic sur la carte pour editer (`clic-carte.js`), detourage / recadrage (`recadrage.js`), dos de carte + impression recto-verso, pack .zip (`export-pack.js`, `zip.js`) avec kit pour le jeu, import des fichiers du Card Maker de reference, tete d'angle, TTS.
- SERVEUR (branche fusionnee, `site/createur_cartes.py` + `site/orchestrateur.py`, tests `site/test_createur_cartes.py` verts) : comptes « createur » sur invitation de l'admin, isolement strict des routes, API `/api/createur/projets`, `/projet/<id>` (GET/PUT/DELETE, 25 Mo, quota 500 Mo), versions. RIEN n'est deploye.

**Reste a faire**
1. ~~Brancher la page sur l'API serveur~~ **FAIT (28/10)** : `public/createur-cartes/serveur.js` (detection 200/401/autre, un projet par dossier `d-<nom>-<empreinte>`, `_reglages`, envoi 5 s apres un changement, fusion au demarrage « le plus recent gagne », indicateur `#etat-serveur`, versions du serveur dans « Versions »). Dates du serveur passees en UTC (`Z`). Teste dans Chromium sur une COPIE de la base : `essai/sync-serveur/` (lancer.py + test-sync.mjs). Limites connues : un navigateur neuf envoie sa carte vide dans « Sans dossier » ; supprimer un dossier supprime aussi ses versions serveur ; `_reglages` en conflit = union par id (pas « le plus recent »).
2. **« Voir une vraie carte comparable »** : FAIT (28/10), teste dans Chromium (EN + FR, connecte, mode local). Decision : tous les createurs, scans complets. `extraire-comparables.py` -> `donnees/comparables.json` (6652 cartes, sans image) ; route `GET /api/createur/scan/<code>` (liste blanche sur le code, `assets/pics-hd` sinon `assets/pics`, session obligatoire, lecture seule, tests dans `site/test_createur_cartes.py`) ; `comparable.js` + bouton sous l'apercu (meme type, mots et declencheurs proches, precedente / suivante, a la meme taille). Limite : hors HD (heros, vilains) les scans font 300 px. A rappeler avant le deploiement : droits sur les scans officiels.
3. **Backup serveur** : FAIT (28/10) `deploiement/sauvegarde.sh` inclut `donnees-createur/` (+ ligne dans `--verifier`, teste). DECISION (28/10) : le createur est ouvert a TOUT compte connecte (joueurs compris) ; `?compte=` de l'admin lit n'importe quel compte (lecture seule) ; tests mis a jour. A FAIRE : un lien vers le createur depuis le site pour les joueurs (aujourd'hui seule l'URL `/createur-cartes.html`).
4. Mots-cles sans source (28/10) : PDF officiel FR consulte (`assets/docs/mc01_guide_de_reference_fr.pdf`, jeu de base). SOURCES TROUVEES : Acceleration = Accélération, Crisis = Crise, Hazard (icone) = **Aléas**, boost (icone) = **Boost** (« icône de boost » ; « Renfort » = le mot-cle Surge), per hero = **Par joueur**, icone d'etoile. Libelles corriges dans `app.js` (ICONES_BARRE), `libres.js` (NOMS_ICONES, IMAGES_JEU) et `i18n.js` (avant : Danger, Renfort pour l'icone boost, Par héros : devines, FAUX). TOUJOURS SANS SOURCE FR OFFICIELLE : Overkill, Piercing, Ranged (absents du guide FR du jeu de base ; seuls les PDF EN les definissent), Amplify (seul « amplification » dans le PDF FR **non officiel** `la-ville-ne-dort-jamais-regles-fr-v1.pdf`) : restent absents du menu FR. A verifier encore : « Dégâts conséquents » (consequential), « Infini », « Amplification » (libelles d'icones), « Renforts et ressources » (titre de section) : aucun guide FR ne les cite.
5. Integration : tests Chromium des fonctions FAIT (28/10) : `essai/fumee-createur.mjs` (30 controles, mode local : 23 types, langue de la carte et de la page, annuler / retablir, cartes, dossiers, recherche, modeles, chercher / remplacer, appliquer, versions, illustration, recadrage, clic sur la carte, exports PNG / pack .zip / TTS / projet .json + reimport, carte comparable, persistance). Tous verts. `nouveautes.js` : entree du 2026-10-29 mise a jour (sauvegarde serveur, carte comparable, ouvert a tous) ; reste : OCTGN / DragnCards non faits ; `PROCESSUS-CARTE.md` non concerne.
6. Deploiement : UNIQUEMENT sur le mot « deploie » de l'utilisateur (annonce de 15 minutes ; 13 commits createur + 6 commits en attente d'avant, dont le merge serveur).
