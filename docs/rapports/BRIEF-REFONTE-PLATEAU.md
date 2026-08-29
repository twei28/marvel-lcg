# Brief complet - Refonte du plateau Marvel Champions LCG

Ce document sert de passation pour une autre IA. Il decrit le contexte, les contraintes fortes, les decisions UX deja validees par l'utilisateur, le prototype actuel, et la marche a suivre pour transformer ce prototype en vrai plateau de jeu sans casser le moteur ni l'ancien runtime.

## 1. Objectif

Refaire l'interface de partie du jeu Marvel Champions LCG pour obtenir un plateau plus moderne, plus lisible et plus agreable, tout en gardant le comportement de jeu intact.

Le travail demande ici concerne le plateau en cours de partie :

- rendu des cartes sur le plateau ;
- lisibilite des scans ;
- etiquettes de types de cartes ;
- compteurs essentiels directement visibles ;
- zoom au survol/focus ;
- integration progressive dans le jeu reel via les donnees `get_world`.

Important : l'utilisateur ne veut pas perdre l'aspect visuel du plateau. Il ne veut pas une interface qui masque tout derriere des zones exclusives ou des panneaux. Il veut conserver une vraie vue de table, avec les cartes visibles.

## 2. Contraintes absolues

### 2.1 Ne pas toucher au moteur

Ne jamais modifier les regles du jeu ni le moteur Python.

Le moteur est considere valide carte par carte. Toute refonte doit etre purement presentationnelle.

### 2.2 Ne pas toucher au runtime historique de partie

Ne pas modifier `public/js/marvel/`.

Dans la planification du projet, ce dossier a le meme statut que le moteur :

- sources perdues / runtime compile ;
- ne pas le modifier ;
- ne pas construire la nouvelle UI en patchant ses classes ;
- ne pas faire dependre le nouveau rendu de ses objets internes.

Le nouveau plateau doit etre une fonction pure du descripteur renvoye par `/get_world?p=0`.

### 2.3 Garder l'ancien plateau comme secours

Le nouveau plateau doit etre ajoute a cote de l'ancien, pas remplacer brutalement l'existant.

Il faut garder un retour vers l'ancienne interface tant que le nouveau plateau n'est pas valide sur une vraie partie.

### 2.4 Ne pas travailler dans le mauvais codebase

Il y a deux copies importantes :

- `Fusion/marvel-lcg-src/` dans ce depot Windows : extraction de distribution perimee, utile pour lire des images/donnees de reference, mais a ne pas traiter comme codebase vivant.
- `~/marvel-work/fusion/marvel-lcg-src` sous WSL : codebase vivant du jeu, cible du deploiement via `ui-app/deployer.sh`.

Le script `ui-app/deployer.sh` est le chemin officiel pour deposer les builds React dans le jeu vivant.

Ne pas copier `dist/` a la main vers le jeu.

### 2.5 Server / assets

Le serveur Python du jeu a un routage par extension strict. Les assets du build Vite doivent rester inlines.

La config Vite actuelle force :

```ts
assetsInlineLimit: () => true
```

Le build ne doit sortir que :

- `.html`
- `.js`
- `.css`

La commande de garde-fou est :

```bash
npm run verifier-sortie
```

## 3. Etat actuel du prototype

Prototype dans :

- `ui-app/src/vitrine.tsx`
- `ui-app/src/vitrine.css`
- page HTML : `ui-app/vitrine.html`

URL locale Vite :

```text
http://127.0.0.1:5173/app/vitrine.html
```

Attention : le `base` Vite est `/app/`, donc l'URL correcte contient `/app/`.

Le serveur Vite etait lance sur :

```text
http://127.0.0.1:5173
```

Si besoin :

```bash
cd ui-app
npm run build
```

ou serveur de dev :

```bash
cd ui-app
npx vite --host 127.0.0.1 --port 5173
```

## 4. Decisions UX deja validees avec l'utilisateur

### 4.1 Rejete : trop d'overlays sur les cartes

Premiere version : infos posees sur les scans.

Retour utilisateur :

> l'overlay sur les cartes cache toute la carte

Decision :

- ne pas recouvrir les scans avec des panneaux d'information ;
- garder les cartes visuellement intactes ;
- seules de petites pastilles strictement necessaires sont autorisees.

### 4.2 Rejete : trop d'informations autour des cartes

Deuxieme version : rail lateral avec nom, ressources, stats, statuts.

Retour utilisateur :

> finalement il y a trop d'infos

Decision :

- supprimer les rails ;
- supprimer les stats completes ;
- supprimer nom/cout/ressources/statuts sur la vue compacte ;
- ne garder que les informations indispensables.

### 4.3 Valide : affichage minimal des cartes

Informations a garder en vue compacte :

- type de carte ;
- PV sur les allies ;
- menace sur les schemes ;
- hover/focus qui agrandit fortement la carte pour lire le scan.

### 4.4 Valide : schemes en paysage

Retour utilisateur :

> les cartes scheme sont en portrait, alors qu'elles doivent etre en paysage

Decision :

- les `SideScheme` doivent utiliser un ratio paysage ;
- ratio CSS utilise dans le prototype : `176 / 127`.

### 4.5 Valide : vrai zoom au hover

Retour utilisateur :

> quand je hover sur la carte elle doit s'aggrandir, la tout est illisible

Decision :

- au hover ou focus clavier, la carte passe au premier plan ;
- portrait : environ 300 px de large au hover ;
- scheme paysage : scale adapte ;
- pas de modale obligatoire pour inspecter ;
- le scan agrandi doit rester directement lisible.

## 5. Rendu minimal valide dans la vitrine

Le composant actuel s'appelle :

```tsx
EnhancedScanCard
```

Il rend :

- un `article.scan-card` focusable (`tabIndex={0}`) ;
- une etiquette type au-dessus ;
- un scan image ;
- un fallback texte si image manquante ;
- un badge PV si `allyHp` est present ;
- un badge MEN si `schemeThreat` est present.

Le type TypeScript actuel :

```ts
type CardKind = 'hero' | 'ally' | 'minion' | 'side-scheme' | 'attachment' | 'treachery'
type CardState = 'ready' | 'exhausted' | 'selected' | 'playable' | 'targetable' | 'disabled'

type EnhancedCardData = {
  id: string
  name: string
  kind: CardKind
  state: CardState
  image: string
  allyHp?: string
  schemeThreat?: string
}
```

Mapping de labels actuel :

```ts
const kindLabel: Record<CardKind, string> = {
  hero: 'Heros',
  ally: 'Allie',
  minion: 'Minion',
  'side-scheme': 'Scheme',
  attachment: 'Attachment',
  treachery: 'Treachery',
}
```

Il faut probablement conserver des labels courts, car les cartes sont petites.

## 6. Donnees de reference utilisees dans le prototype

Les cartes utilisees dans la vitrine :

| Card ID | Nom | Type jeu | Rendu prototype |
|---|---|---|---|
| `16001a` | Groot | `Hero` | `hero` |
| `60039` | Daredevil | `Ally` | `ally`, badge PV |
| `90001` | Ronan the Accuser | `Minion` | `minion` |
| `90002` | Judge, Jury, Executioner | `SideScheme` | `side-scheme`, badge MEN |
| `90003` | The Accused | `Attachment` | `attachment` |
| `90004` | Bring the Hammer Down | `Treachery` | `treachery` |

Scans du prototype :

```ts
import grootScan from '../../Fusion/marvel-lcg-src/assets/pics/16001a.jpg'
import ronanScan from '../../Fusion/marvel-lcg-src/assets/pics/90001.jpg'
import ronanSchemeScan from '../../Fusion/marvel-lcg-src/assets/pics/90002.jpg'
import accusedScan from '../../Fusion/marvel-lcg-src/assets/pics/90003.jpg'
import hammerScan from '../../Fusion/marvel-lcg-src/assets/pics/90004.jpg'
import daredevilScan from '../../Fusion/marvel-lcg-src/assets/pics/60039.jpg'
```

Pour le vrai plateau, ne pas hardcoder ces imports. Il faudra construire l'URL de scan depuis l'id de carte, en suivant les routes serveur deja existantes.

## 7. Couleurs et grammaire visuelle validees

La couleur doit suivre les scans et les donnees du jeu, pas une palette arbitraire.

### 7.1 Types de cartes

Correction deja faite apres verification des scans et de `data/cards.json` :

- Ronan est `Minion`, pas `Vilain`.
- The Accused est `Attachment`, pas `Amelioration`.
- Bring the Hammer Down est `Treachery`, pas `Evenement`.
- Judge, Jury, Executioner est `SideScheme`, pas une carte portrait.

### 7.2 Familles de couleurs

Dans le prototype actuel :

- cartes joueur (`hero`, `ally`) : accent blanc/acier ;
- cartes rencontre (`minion`, `side-scheme`, `attachment`, `treachery`) : accent cyan/noir, proche des cadres des scans rencontre ;
- menace scheme : jaune, car dans le moteur `Symbol.threat` est jaune ;
- PV / health : rouge, car dans le moteur `Symbol.health` est rouge clair ;
- selection / cible / jouable : glow externe, pas overlay couvrant la carte.

Source moteur pour les symboles :

```text
Fusion/marvel-lcg-src/src/game/render/symbol.py
```

Extrait important :

```py
health = Fore.LIGHTRED_EX
threat = Fore.YELLOW
scheme = Fore.CYAN
```

## 8. CSS important du prototype

### 8.1 Taille normale

Portrait :

```css
.scan-card {
  --card-w: 116px;
}
```

Desktop large :

```css
@media (min-width: 1180px) {
  .scan-card {
    --card-w: 120px;
  }
}
```

Scheme paysage :

```css
.scan-card.kind-side-scheme {
  --card-w: 170px;
}

.scan-card.kind-side-scheme .scan-frame {
  aspect-ratio: 176 / 127;
}
```

### 8.2 Hover / focus

Le hover actuel :

```css
.scan-card {
  --inspect-scale: 2.5;
  transform-origin: center;
  transition: transform 180ms ease, filter 180ms ease;
  cursor: zoom-in;
}

.scan-card:hover,
.scan-card:focus-visible {
  z-index: 40;
  transform: scale(var(--inspect-scale));
  filter: brightness(1.06);
  outline: none;
}

.scan-card.kind-side-scheme {
  --inspect-scale: 2.1;
}
```

Origine selon la rangee :

```css
.encounter-row .scan-card {
  transform-origin: top center;
}

.player-row .scan-card {
  transform-origin: center;
}

.hand-row .scan-card {
  transform-origin: bottom center;
}
```

Sur desktop, la mesure faite par Playwright sur Groot apres hover donne environ :

```json
{
  "width": 300,
  "height": 488
}
```

Donc la carte devient vraiment lisible.

### 8.3 Badges

PV allie :

- rouge ;
- coin superieur droit ;
- contenu actuel : `1/3` + `PV`.

Menace scheme :

- jaune ;
- coin superieur droit ;
- contenu actuel : `3` + `MEN`.

Important : ces badges sont les seuls overlays acceptes actuellement.

## 9. Architecture recommandee pour la suite

Ne pas faire un remplacement direct de `marvel.html`.

Ordre recommande :

1. Extraire le composant carte du prototype.
2. Creer une petite couche `card-model` qui transforme les donnees jeu en props UI.
3. Rendre les fixtures `get_world` existantes avec le nouveau composant.
4. Ajouter une page de prototype plateau reelle, par exemple `board.html` dans `ui-app`.
5. Brancher `board.html` sur `/get_world?p=0` en lecture seule.
6. Ajouter le retour vers l'ancien plateau.
7. Seulement ensuite envisager la bascule comme plateau principal.

## 10. Integration dans `ui-app`

Actuellement `vite.config.ts` ne build que `vitrine.html` :

```ts
rolldownOptions: {
  input: {
    vitrine: resolve(import.meta.dirname, 'vitrine.html'),
  },
},
```

Pour ajouter un plateau React, ajouter un input :

```ts
rolldownOptions: {
  input: {
    vitrine: resolve(import.meta.dirname, 'vitrine.html'),
    board: resolve(import.meta.dirname, 'board.html'),
  },
},
```

Fichiers probables a creer :

```text
ui-app/board.html
ui-app/src/board.tsx
ui-app/src/board.css
ui-app/src/components/ScanCard.tsx
ui-app/src/components/ScanCard.css
ui-app/src/board/world-model.ts
```

Le composant `ScanCard` doit reutiliser exactement la logique UX validee dans `vitrine.tsx`.

## 11. Modele de donnees cible pour le composant carte

Proposition de props generiques :

```ts
type CardKind =
  | 'hero'
  | 'alter-ego'
  | 'ally'
  | 'support'
  | 'upgrade'
  | 'event'
  | 'resource'
  | 'villain'
  | 'minion'
  | 'main-scheme'
  | 'side-scheme'
  | 'attachment'
  | 'treachery'
  | 'environment'
  | 'obligation'
  | 'status'
  | 'unknown'

type CardState =
  | 'ready'
  | 'exhausted'
  | 'selected'
  | 'playable'
  | 'targetable'
  | 'disabled'
  | 'hidden'

type ScanCardProps = {
  id: string
  name: string
  kind: CardKind
  state?: CardState
  imageUrl: string
  isLandscape?: boolean
  allyHp?: string
  schemeThreat?: string
  facedown?: boolean
}
```

Les props visibles en mode compact doivent rester limitees :

- `kind`
- `allyHp`
- `schemeThreat`
- etat par contour/glow

Ne pas rajouter toutes les stats sur la carte compacte sans revalidation utilisateur.

## 12. Mapping depuis `cards.json`

Source :

```text
Fusion/marvel-lcg-src/data/cards.json
```

Types observes :

- `Hero`
- `Ally`
- `Minion`
- `SideScheme`
- `Attachment`
- `Treachery`

Champs observes :

```json
{
  "card_id": "90002",
  "type": "SideScheme",
  "name": "Judge, Jury, Executioner",
  "desc": {
    "Acceleration": "1",
    "StartingThreat": "3*"
  }
}
```

Pour `SideScheme`, utiliser `desc.StartingThreat` ou la valeur courante de menace depuis `get_world` si disponible. En plateau live, il faut afficher la menace courante, pas seulement la menace imprimee.

Pour `Ally`, utiliser :

- PV courants depuis `get_world`, si disponible ;
- PV max depuis `cards.json` ou depuis le descriptor si deja present.

Format souhaite :

```text
1/3 PV
```

## 13. Ce qu'il faut inspecter dans `get_world`

Le contrat exact du descriptor doit etre mesure depuis les fixtures ou depuis `/get_world`.

Ne pas supposer la forme du JSON.

Endroit a utiliser :

```text
/get_world?p=0
```

Tests existants autour de `get_world` :

```text
ui-check/tests/lancement-partie.spec.ts
ui-check/tests/fixtures.spec.ts
```

Commentaires importants dans `ui-check/tests/fixtures.spec.ts` :

- ouvre `/fixtures.html` ;
- parcourt les etats du catalogue ;
- ces etats viennent de `public/js/fixtures/index.js` dans le codebase vivant.

Il faut trouver, dans les fixtures :

- ou sont les zones du plateau ;
- comment une carte est representee ;
- son id de scan ;
- son type ou son `card_id` ;
- ses compteurs courants ;
- son etat engage / pret ;
- les cibles possibles pendant un ask.

## 14. Fixtures

Les fixtures sont centrales pour developper le plateau sans lancer une vraie partie.

Contrainte projet :

- fixtures au format module `.js`, pas `.json` ;
- elles vivent dans le codebase vivant, hors depot git ;
- ne jamais les editer a la main.

Chemin vivant indique par la planification :

```text
~/marvel-work/fusion/marvel-lcg-src/public/js/fixtures/
```

Page existante :

```text
public/fixtures.html
```

Le projet prevoit justement qu'en phase plateau, cette page accueille le composant React.

Recommendation :

1. Ajouter une page React de lecture des fixtures dans `ui-app`.
2. Ne pas lancer de partie pour tester le rendu.
3. Afficher plusieurs fixtures : main pleine, side scheme, minions, etats de ciblage, etc.
4. Ajouter une capture Playwright dediee quand le rendu est stable.

## 15. Page live recommandee

Quand le rendu fixtures est bon, creer une page live :

```text
public/app/board.html
```

Elle peut fetcher :

```ts
const response = await fetch('/get_world?p=0')
const world = await response.json()
```

La page doit poller proprement ou utiliser le mecanisme existant si un endpoint de sync est documente. Pour commencer, polling simple suffit :

```ts
setInterval(loadWorld, 500)
```

Mais attention :

- ne pas envoyer d'actions au moteur au debut ;
- commencer par lecture seule ;
- ensuite seulement brancher les interactions.

## 16. Rendu plateau recommande

Conserver une vue de table :

- rangee rencontre : minions, villain, schemes ;
- rangee joueur : identite, allies, supports/upgrades ;
- main en bas ;
- barre d'action attendue en bas ;
- zones visibles, mais pas de navigation qui remplace tout le plateau.

L'utilisateur a refuse l'idee qui ferait perdre trop de visuel. Donc eviter :

- onglets exclusifs qui cachent le plateau entier ;
- focus zone obligatoire ;
- UI trop dashboard au detriment de la table.

Pour mobile, garder un scroll horizontal ou une solution progressive. Ne pas ecraser les cartes a une taille illisible.

## 17. Interaction hover / tactile

Desktop :

- hover = zoom ;
- focus clavier = zoom ;
- cursor `zoom-in`.

Mobile / tactile :

- prevoir tap ou appui long pour zoom ;
- le premier tap peut selectionner/inspecter ;
- attention a ne pas bloquer les actions de jeu.

Ne pas utiliser une modale plein ecran pour chaque inspection au premier palier. L'utilisateur a valide le zoom direct de la carte.

## 18. Tests et commandes

Dans `ui-app` :

```bash
npm run typecheck
npm run build
npm run verifier-sortie
```

Captures rapides avec Playwright depuis `ui-check` :

```bash
npx playwright screenshot --viewport-size=1440,900 http://127.0.0.1:5173/app/vitrine.html test-results\scan-enrichi-vitrine.png
```

Capture hover deja utilisee :

```bash
node -e "const { chromium } = require('@playwright/test'); (async () => { const browser = await chromium.launch(); const page = await browser.newPage({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 1 }); await page.goto('http://127.0.0.1:5173/app/vitrine.html', { waitUntil: 'networkidle' }); const card = page.locator('.scan-card.kind-hero'); await card.hover(); await page.waitForTimeout(250); await page.screenshot({ path: 'test-results/scan-enrichi-hover.png' }); await browser.close(); })();"
```

Pour deploiement dans le jeu vivant :

```bash
bash ui-app/deployer.sh
```

Ce script doit etre lance depuis WSL, pas depuis un script npm.

## 19. Qualite attendue avant de brancher au jeu reel

Avant toute bascule live :

- `typecheck` vert ;
- `build` vert ;
- `verifier-sortie` vert ;
- capture desktop normale ;
- capture desktop hover ;
- capture mobile ;
- pas d'asset hors `.html/.js/.css` dans `dist/` ;
- ancien plateau encore accessible ;
- aucune modification de `public/js/marvel/`.

Pour une vraie livraison projet :

- deploiement via `deployer.sh` ;
- re-zip vers `Fusion/` selon le rituel du projet ;
- test autoplay sans traceback si le plateau live est branche.

## 20. Pieges connus

### 20.1 `Fusion/marvel-lcg-src` n'est pas le codebase vivant

Ne pas livrer en modifiant cette copie.

### 20.2 `ui-app/dist/` est ignore

Ne pas supposer que `dist/` est versionne.

### 20.3 Le serveur ne sert pas n'importe quel asset

Ne pas ajouter `.png`, `.webp`, `.woff2`, `.json` en sortie Vite.

### 20.4 Ne pas figer des references visuelles au hasard

Dans `ui-check`, les references sont validees par script dedie. Ne pas lancer un update snapshot direct.

### 20.5 Ne pas mettre trop d'informations sur les cartes

L'utilisateur a explicitement rejete :

- overlays larges ;
- rails de stats ;
- noms et couts en plus du scan ;
- trop de badges.

Vue compacte = type + PV allie + menace scheme.

### 20.6 Le scheme doit rester paysage

Tout `SideScheme` doit etre en paysage.

Probablement aussi `MainScheme`, a verifier sur les scans.

## 21. Definition of done proposee pour le prochain palier

Palier 1 : composant reusable

- `ScanCard` extrait de `vitrine.tsx`.
- Meme rendu que la vitrine.
- `vitrine.tsx` consomme le composant extrait.
- Tests `typecheck/build/verifier-sortie` verts.

Palier 2 : donnees reelles

- lecture de `cards.json` ou d'une representation catalogue ;
- mapping `card_id -> type, name, scan`;
- plus de donnees hardcodees dans la vitrine, sauf le choix des exemples.

Palier 3 : fixtures

- page React qui rend une fixture `get_world`;
- cartes groupees par zones ;
- aucun fetch live obligatoire ;
- hover lisible.

Palier 4 : live read-only

- page React qui fetch `/get_world?p=0`;
- rendu du plateau courant ;
- pas encore d'actions ;
- ancien plateau intact.

Palier 5 : interactions

- ciblage ;
- selection ;
- ask bar ;
- actions moteur ;
- undo/annuler si disponible ;
- tests de vraie partie.

## 22. Resume court pour l'autre IA

Tu dois transformer le prototype `ui-app/src/vitrine.tsx` + `vitrine.css` en vrai composant plateau.

Ne touche pas au moteur. Ne touche pas a `public/js/marvel/`.

La carte compacte validee par l'utilisateur affiche seulement :

- le type de carte ;
- les PV pour les allies ;
- la menace pour les schemes ;
- un zoom fort au hover/focus.

Les schemes sont en paysage.

Les couleurs doivent suivre les scans et le moteur :

- encounter : cyan/noir ;
- health/PV : rouge ;
- threat/menace : jaune ;
- joueur : blanc/acier.

Le nouveau plateau doit lire `/get_world?p=0` ou les fixtures, et rester reversible vers l'ancien plateau.

