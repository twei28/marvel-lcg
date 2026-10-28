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

## Reste a faire (dans cet ordre)
1. **Corriger le texte des cartes a coin coupe** : sur `event/identity/resource`, des lignes debordent encore (a gauche et en bas : verifier `bordureForme`, y de la ligne = bas, hauteur max du panneau) ; `playersidescheme` : retrait a gauche trop fort.
2. **Nombres** : valeurs de cout, THW/SCH, ATK, DEF, REC, PV (polices ElektraMed, boites mesurees, `scl 0.95`), etoiles (`CODE s`), degats consequents (`CODE dd`), menace de depart/cible, acceleration, numero/lettre de phase, etape du vilain (`villainstagenew`, police `ancbi`), attachement (ATK/SCH), taille de main, icones de renfort (3 + etoile, `general/boost_*.png`), 3 ressources (`general/resource-*.png`, positions a mesurer : le tool les place a gauche en bas).
3. **Variantes -star** des calques `splash*` (`general/splash-star.png`...), `hp_bubble`, cracks on/off, light_boxes, dots.
4. **Tete (headshot)** `img/headshot.png` + son cadre, etoile de splash.
5. **Types restants a verifier un par un** contre `reference/` : alter-ego, starter-deck, obligation, support, upgrade, promos (4), attachment, environment, main_scheme_a/b, minion, obligation-villain, sidescheme, treachery.
6. **Bilingue** : libelle du type baked en anglais -> pour le FR, recouvrir la bande (echantillonner la couleur du calque) et redessiner le libelle FR (ALLIE, EVENEMENT, AMELIORATION, SOUTIEN, RESSOURCE, HEROS, ALTER-EGO, MECHANT, SBIRE, TRAHISON, ENVIRONNEMENT, ATTACHEMENT, MANIGANCE PRINCIPALE/ANNEXE, OBLIGATION) ; textes FR/EN par carte, traits via `ui-app/src/board/traits-fr.ts`, ligne d'ensemble FR (« TAILLE DE MAIN 6 / POINTS DE VIE 10 »).
7. **Interface** (page `public/createur-cartes.html` ou `index.html`) : liste de cartes, choix du type, formulaire guide par type avec valeurs par defaut, apercu en direct, palettes (aspects Basic/Agression/Direction/Protection/Justice/Pool + presets heros et vilains), illustration (zoom/position/rotation, avant/arriere, glisser), sauvegarde JSON + navigateur, export PNG/JPG/WebP (taille reglable, fond perdu), export des deux langues, impression PDF, tables (TTS/OCTGN/DragnCards si utile).
8. Bouton dans l'en-tete (`public/js/prepare/lien-admin.js`, a cote de « Atelier de couvertures »), cle EN, `nouveautes.js`, page credits, tests Chromium de chaque type, optimisation des PNG (18 Mo -> webp sans perte).
