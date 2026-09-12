# Plateau portrait en bandes : plan d'implémentation

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Remplacer le plateau portrait « une colonne » par quatre bandes horizontales défilantes, la main derrière une encoche à droite, les piles derrière une encoche à gauche, le bandeau du haut portant le menu « … » et le bouton Fin du tour, sans barre en bas.

**Architecture:** `bandes-portrait.ts` (pur) répartit le `Plateau` en 4 bandes + main + piles. `PlateauPortrait` rend `BandeauPortrait`, une `.portrait-table` qui défile verticalement avec 4 `Bande`, et les couches (main en feuille, tiroir des piles, carte ouverte, pile regardée). Les cartes des bandes passent par `Unite` (exporté de `Board.tsx`) pour hériter des attachements, statuts, piles et pastilles du PC. Le Retour Android reste piloté par `retour-android.ts` (observation du DOM).

**Tech Stack:** React 18, TypeScript strict, vitest + Testing Library (`ui-app`), Playwright (`ui-check`, projet `s24` 480×1050 tactile, serveur local `serveur-dev.py --port 2345`, build `bash ui-app/deployer.sh`).

**Spec:** `docs/superpowers/specs/2026-09-12-plateau-portrait-en-bandes-design.md`

## Global Constraints

- Le plateau PC (`Board.tsx`, `board.css`) ne change pas de rendu : seuls des `export` sont ajoutés.
- Toute carte tactile porte `data-tactile` et fait ≥ 44×44 px ; les cartes des bandes font ≥ 140 px de large à 480 px.
- CSS : `@layer` cassé en production (`base` > `composants` > `utilitaires`) : surcharges de `board.css` en `!important`, surcharges de `ScanCard.css` en couche `utilitaires`. Pas de loupe (`transform: none`, `--inspect-scale: 1`).
- Textes en français via `t()`, dictionnaire `dico-en.ts` pour l'anglais.
- Pas de `any`. Un `useAppuiLong` par carte, jamais dans un `.map`.
- Vérification visuelle à 480×1050 avant de déclarer une tâche finie ; rien n'est déployé sans validation de l'utilisateur.

---

### Task 1 : `bandes-portrait.ts`, la répartition pure

**Files:** Create `ui-app/src/board/mobile/bandes-portrait.ts`, `bandes-portrait.test.ts`. Delete `blocs-portrait.ts`, `blocs-portrait.test.ts`, `blocs-portrait-vrai-plateau.test.ts` (Task 7).

**Interfaces (Produces):**
```ts
export type PileAffichee = { cle: string; titre: string; unite: UniteAffichee; compte?: number }
export type BandePortrait = { epinglee?: UniteAffichee; unites: UniteAffichee[] }
export type BandesPortrait = {
  vilain: BandePortrait; manigances: BandePortrait; engages: BandePortrait; heros: BandePortrait
  main: UniteAffichee[]; piles: PileAffichee[]
}
export function repartirEnBandes(plateau: Plateau): BandesPortrait
```
Règles : `vilain.epinglee` = `rencontre[0]`, `vilain.unites` = reste de `rencontre` + `terrain-combat` de `kind === 'environment'` ; `manigances.epinglee` = `complot-principal[0]`, `unites` = `complots-secondaires` ; `engages.unites` = `terrain-combat` sauf `ally`/`environment` ; `heros.epinglee` = première unité de `terrain-soutien` dont `kind` ∈ {`hero`,`alter-ego`}, `unites` = reste de `terrain-soutien` + alliés de `terrain-combat` + unités de `deck-special`/`reserve` **sans** `pileContenu` ; `piles` = toutes les unités de `piles-joueur`, `piles-rencontre`, `nemesis`, `annexes` + celles de `deck-special`/`reserve` **avec** `pileContenu` ou `pileCount`, `{ cle: unite.cle, titre: emplacement.titre + nom, compte: carte.pileCount }`.

- [ ] Tests : environnement chez le méchant, allié chez le héros, identité épinglée, manigance principale épinglée + annexes, piles repérées (deck joueur `joueur-deck`), bandes vides toujours présentes.
- [ ] Implémentation, `npx vitest run src/board/mobile/bandes-portrait.test.ts`.

### Task 2 : `Unite` et `PileRegardee` exportés, `actionPrincipale` dans `BoardProps`

**Files:** Modify `ui-app/src/board/Board.tsx` (`export function Unite`, `export function PileRegardee`, prop `actionPrincipale?: { libelle: string; suggere?: boolean; agir: () => void }` dans `BoardProps`, ignorée par `Board`), `ui-app/src/board.tsx` (passe `actionPrincipale` quand `afficherFinTourSimple`, ne rend pas `.bouton-fin-tour` si `modePlateau === 'mobile'`).

- [ ] `npx tsc --noEmit` vert.

### Task 3 : `Bande.tsx` et `CarteBande`

**Files:** Create `ui-app/src/board/mobile/Bande.tsx`, `Bande.test.tsx`.

```tsx
export function Bande({ cle, titre, epinglee, unites, texteVide, onglets, interactifs, effets, heroActifId, ouvrirPile, ouvrirCarte, agir }: {
  cle: 'vilain' | 'manigances' | 'engages' | 'heros'; titre: string
  epinglee?: UniteAffichee; unites: UniteAffichee[]; texteVide: string; onglets?: ReactNode
  interactifs: Map<number, EtatInteractif>; effets: Map<number, CardEffectDelta>; heroActifId?: number
  ouvrirPile: (titre: string, cartes: ScanCardProps[], groupes?: GroupeDePile[]) => void
  ouvrirCarte: (carte: ScanCardProps) => void
  agir: (carte: ScanCardProps) => void
})
```
`CarteBande` (une par unité) : `<div class="bande-carte" data-tactile="carte">` avec `useAppuiLong(() => agir(porteurDecoré))`, `onClickCapture` : trouve `.scan-card` visé (`data-card-id`), `stopPropagation`, `ouvrirCarte(carteDecorée)` (sauf `vientDeDeclencher()`). La carte décorée = `avecInteraction(carte, interactifs, effets)` (porteur ou attachée). Épinglée : `class="bande-carte est-epinglee"`. Vide : `<p class="bande-vide">`.

- [ ] Tests : titre, texte vide, épinglée première, tap ouvre, appui long agit, attachées rendues (`.est-attachee`).

### Task 4 : encoches, main en feuille, tiroir

**Files:** Create `Encoche.tsx` (+test), rewrite `MainPortrait.tsx` (+test), rewrite `TiroirPiles.tsx` (+test).

- `Encoche({ cote: 'droite'|'gauche', libelle, nombre?, onOuvrir })` : `<button class="encoche encoche-{main|piles}" data-tactile>` ; `pointerdown` mémorise x, `pointermove` de 24 px vers l'intérieur → `onOuvrir()` (une fois), `click` → `onOuvrir()`.
- `MainPortrait({ unites, ouverte, onFermer, onOuvrir, onJouer })` : si `!ouverte` → `null` ; sinon voile `.main-feuille-voile` (`pointerdown` → `onFermer`) + `<section class="main-feuille" role="dialog">` avec la rangée actuelle ; swipe droite ≥ 40 px sur la section → `onFermer`.
- `TiroirPiles({ piles, ouvert, onFermer, onOuvrirPile })` : voile `.tiroir-voile` + `<aside class="tiroir">`, `<button class="tiroir-pile" data-tactile="pile">` par pile (vignette `ScanCard` taille 48 px, nom, compte), `disabled` si pas de `pileContenu`.

### Task 5 : `BandeauPortrait` avec menu et action, `PlateauPortrait` réécrit, `PlateauMobile`

**Files:** Modify `BandeauPortrait.tsx` (+test), rewrite `PlateauPortrait.tsx` (+test réécrit), modify `PlateauMobile.tsx`, `retour-android.ts` (+test), delete `EcranPaysage.tsx`.

- Bandeau : `{ monde, quiAgit, menu?, actionPrincipale? }` → `.portrait-menu-bouton` (« … », `data-tactile="menu"`, `aria-expanded`) ouvre `.portrait-menu-voile` + `<nav class="portrait-menu">` contenant `menu` ; `.portrait-action` (`data-tactile="action"`, `est-suggere`).
- PlateauPortrait : `repartirEnBandes(props.plateau)` ; états `mainOuverte`, `tiroirOuvert`, `carteLue`, `pileRegardee` ; **ouverture automatique** : `useEffect` sur `questionSurLaMain = [...interactifs.keys()].some(id => idsMain.has(id))` → `setMainOuverte(true)`, et retour à `false` quand il redevient faux (souvenir `ouvertePourLaQuestion`). `agir(carte)` = `carte.onSelect?.() ?? props.onCardClick?.(carte)`. Onglets coop dans `Bande heros` (`onglets` = `<OngletsJoueurs>`).
- `FERMABLES` += `.portrait-menu-voile` (bouton `.portrait-menu-bouton`), `.main-feuille-voile`, `.tiroir-voile`, `.menu-actions-carte`.
- `PlateauMobile` : plus de `?medaillons`, plus d'`EcranPaysage`.

### Task 6 : CSS

**Files:** Rewrite `portrait.css` ; modify `menus-mobile.css` (`--feuille-bas: 0px` sur `body.mode-plateau-portrait`) ; `menus-mobile.test.ts` adapté.

Points : `.plateau-portrait` grille `auto 1fr` ; `.portrait-table` `overflow-y: auto` ; `.bande` (titre 0.7rem majuscules, `min-height` calc(card-h + 40px)) ; `.bande-rail` flex + `overflow-x: auto` + snap ; `.est-epinglee` sticky ; `--card-w: clamp(140px, calc((100vw - 48px) / 3), 200px)` (paysage : `/ 5`) ; `.plateau-unite` déjà stylé par board.css (vérifier le débordement des attachées : `padding-bottom` du rail) ; encoches (48×72, bord, `z-index: 45`) ; `.main-feuille` (bas, `z-index: 640`) ; `.tiroir` (gauche, 76 %, `z-index: 640`) ; `.portrait-menu` (feuille basse, `.board-actions` en colonne, `.bh-etat` masqué, boutons 48 px) ; `.carte-ouverte*` et `.pm-barre` déménagés depuis `medaillon.css`.

### Task 7 : retrait de l'ancien modèle et des tests morts

**Files:** Delete `PlateauMedaillons.tsx` (+test), `MainEventail.tsx`, `RangeeMedaillons.tsx`, `Medaillon.tsx`, `ZoneFocus.tsx` (+test), `bandes.ts` (+test), `couches.ts` (+test), `joueurs.ts` (+test), `BarreBas.tsx`, `CarteAvecChiffres.tsx` (+test), `CompteursPortrait.tsx` (+test), `BarreMenace.tsx` (+test), `medaillon.css`, `mobile.css`, `portrait-barre-bas.test.ts`, `portrait-largeur-colonne.test.ts`, `portrait-table-defilement.test.ts`, `blocs-portrait*`, `PlateauMobile.test.tsx` (adapter), `ui-check/tests/plateau-paysage.spec.ts`. Adapter `board.tsx` (props `carteFocalisee`/`onFermerCarte`/`selecteurOuvert`/`onFermerSelecteur` : conservées dans `BoardProps`, plus lues), `package.json`/`playwright.config.ts` de ui-check (script `plateau-paysage`).

- [ ] `npx tsc --noEmit`, `npx vitest run` verts.

### Task 8 : Playwright et vérification visuelle

**Files:** Rewrite `ui-check/tests/plateau-mobile.spec.ts`, adapt `menus-mobile.spec.ts`.

- plateau-mobile : par fixture, `.plateau-portrait` visible, pas de débordement horizontal, `.bande` ×4, cartes `.bande-carte .scan-card` ≥ 140 px, `[data-tactile]` ≥ 44, `.main-feuille` absente, tap `.encoche-main` → `.main-feuille` visible, tap voile → fermée, tap `.encoche-piles` → `.tiroir`, zéro erreur console.
- menus-mobile : `ouvrirLEtat` attend `.portrait-menu-bouton`, l'ouvre, puis `.bh-options` ; `verifierLaFeuille` sans `.pm-barre` (feuille jusqu'au bas ± 1) ; Retour Android : menu → Options → Retour ferme Options, Retour ferme le menu ; main : `.encoche-main` → `.main-feuille .scan-card` tap → `.carte-ouverte-voile`.
- Captures 480×1050 et 1050×480 (paysage) sur une vraie partie (Spider-Man / Rhino) et sur une fixture chargée en annexes et attachements ; lecture des captures avant de conclure.

### Task 9 : docs, nouveautés, commit

- `.planning/todos/2026-09-07-parcours-solo-mobile-portrait.md` : point du 12/09 au soir ; `nouveautes.js` : entrée FR/EN ; fiche du plan : bilan. Commit unique, pas de déploiement sans « déploie ».

## Bilan du 12/09/2026 (soir)

Tout livré en une fois, comme demandé. Ce qui s'est ajouté en route :

- **`Unite` et `PileRegardee` exportés de `Board.tsx`** : les bandes héritent
  des attachements glissés sous la porteuse, des statuts, des piles et des
  pastilles sans une seconde copie. Les statuts n'étaient réduits que sous
  `.plateau-scene` : `portrait.css` reprend les mêmes valeurs (50 / 74 px).
- **La main ne s'ouvre PAS pour une carte simplement jouable** (rôle
  `porteur`) : mesuré au premier essai, le voile de la main bloquait le
  bandeau dès la fin du mulligan. Seuls `cible` et `ressource` l'ouvrent.
- **`hauteur-de-question.ts`** : la feuille de question du bas
  (`.actions-flottantes`, `.demande-centrale`, `.evenement-centrale`)
  recouvrait la moitié des cartes à payer ; la main se pose désormais
  au-dessus d'elle (`--question-h`).
- **Le voile du menu recouvrait les boutons du bandeau** (même contexte
  d'empilement) : `z-index` sur les boutons. Le « … » devient « × » quand le
  menu est ouvert : les feuilles (Options, Historique) couvrent le menu et ne
  laissent libre que le haut de l'écran, où vit ce bouton. Le doublon
  « Fin du tour » de `.board-actions` est masqué dans le menu.
- **`--feuille-bas: 0px`** posé sur `body.mode-plateau-portrait` : les
  feuilles de `menus-mobile.css` descendent jusqu'au bord.
- Filets : vitest 92 tests sur `mobile/` (17 fichiers), Playwright
  `plateau-mobile` (34 états, quatre bandes, cartes ≥ 140 px, encoches,
  main et tiroir) et `menus-mobile` (menu du bandeau, Options, Historique,
  « … », Retour Android sur deux niveaux, main puis carte ouverte) verts.
  `plateau-paysage.spec.ts` (mort depuis `9f0b6fac`) supprimé.
