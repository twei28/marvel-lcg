# Recherche d'architecture : v1.1 Tablette et téléphone

**Domaine :** plateau de jeu de cartes web (React 19 + TS, Vite) et pages en JS non compilé, à rendre tactiles
**Recherché le :** 13/10/2026
**Confiance :** HAUTE pour les points d'intégration (lus dans le code), MOYENNE pour la détection iPad + trackpad (une source WebKit / GitHub), BASSE pour tout ce qui touche un vrai iPad (jamais essayé sur l'appareil)

## Constat de départ (lu dans le code, pas supposé)

1. **Le choix de la mise en page est déjà centralisé** : `ui-app/src/board/mobile/useModeMobile.ts` (`REQUETE_MOBILE = '(max-width: 767px)'`, réglage `mode-plateau` en localStorage, `?mobile` en échappatoire). Il est lu à trois endroits de `ui-app/src/board.tsx` : l. 1482 (vue d'état enregistré, aiguillage l. 1545), l. 1977 (partie en cours), aiguillage `RenduPartie` l. 4213. L'assistant JS a sa propre copie du même seuil : `public/js/prepare/tel.js` l. 8 (`html.tel`), réutilisée par `public/js/tel-pages.js`.
2. **Il n'existe AUCUNE notion de « mode de saisie »** (doigt contre souris) partagée. On trouve à la place une demi-douzaine de détections locales et incohérentes :
   - `REQUETE_TELEPHONE` (`mobile/telephone.ts` l. 17) : fonctions du téléphone (écran allumé, vibrations, verrou portrait) ;
   - `REQUETE_PAYSAGE_TEL` (`Board.tsx` l. 149) : échelle minimale du téléphone couché ;
   - `(pointer: coarse)` dans `board.css` l. 2163 (menu d'une carte en feuille basse), l. 5602 (bouton Fin du tour masqué), l. 6017 (barre qui s'enroule) ;
   - `ECRAN_SANS_AIDE_AUTO` (`manuel/VoletAideManuel.tsx` l. 114) ;
   - `evenement.pointerType` lu au cas par cas (`NomsDeCartes.tsx` l. 47, `RecapPhaseMechant.tsx` l. 828, `CartouchePhase.tsx` l. 1647, `manuel/appui-tactile.ts` l. 25) ;
   - côté assistant, `SANS_SURVOL = !matchMedia("(hover: hover)")` lu UNE fois au chargement (`public/js/prepare/app.js` l. 76).
3. **Le défaut bloquant de la tablette est mécanique** : `Board.tsx` l. 1133 (`survol`) est branché sur `onMouseOver` du `.plateau-cadre` (l. 1423). Un toucher iOS émet des événements souris de compatibilité : `mouseover` arrive, l'aperçu s'ouvre après 200 ms, et `mouseleave` (l. 1424, `quitter`) ne vient jamais. Le clic (`cliquerCarte`, l. 1153, appelé dans `onPointerUp` l. 1457) ouvre en plus le menu : c'est le « aperçu + menu ensemble » que la décision 1 garde, mais rien ne referme l'aperçu.
4. **Le paysage du téléphone est déjà le plateau PC** : `PlateauPaysage.tsx` n'existe plus (supprimé par `9f0b6fac`, « plus rendu nulle part »). Un téléphone couché de 768 px et plus reçoit `Board` avec `ECHELLE_MIN_PAYSAGE_TEL = 0.75` et la table qui se fait glisser (`body.plateau-paysage-tel`, `Board.tsx` l. 143 à 175) ; sous 768 px couché (667 x 375), il reçoit `PlateauPortrait` avec ses règles `@media (orientation: landscape)` (`portrait.css` l. 768). Le brief du jalon cite `PlateauPaysage.tsx` : c'est périmé.
5. **Le précédent du réglage partagé existe** : « Affichage : Normal / Sobre » vit sous la même clé `mc_affichage_v1` dans `public/js/prepare/affichage.js` et `ui-app/src/board/affichage.ts`, se traduit par `html[data-affichage]`, et chaque côté a son petit lecteur. Le précédent du **script de tête partagé** existe aussi : `public/js/ui-version.js`, chargé sans `defer` dans `<head>` par `ui-app/board.html` ET par `prepare.html`, `cards.html`, `deck.html`, `replay.html`, « pour que l'attribut existe avant le premier calcul de style ».
6. **Les primitives tactiles existent, mais rangées sous `mobile/`** : `useAppuiLong` (450 ms, déjà importé par `manuel/appui-tactile.ts`), `issueAppui` (glisser ou menu), `CarteOuverte` (agrandissement, glisser latéral entre voisines, autre face), `retour-android.ts`, `installerSuiviDuGeste` (horodatage du dernier geste, `telephone.ts` l. 52).
7. **Le filet Playwright ne simule pas de tablette tactile** : le gabarit `tablette` (1180 x 820, `ui-check/playwright.config.ts` l. 25) tourne SANS `hasTouch`. Seul `s24` a `hasTouch: true, isMobile: true`.

## Architecture recommandée

### Vue d'ensemble : deux axes indépendants, pas trois mises en page

```
┌──────────────────────────────────────────────────────────────────────┐
│  AXE 1 : DISPOSITION (existant, inchangé)                            │
│  largeur < 768 px  -> PlateauMobile / PlateauPortrait, html.tel       │
│  largeur >= 768 px -> Board (plateau PC, mis à l'échelle)             │
│  Source : useModeMobile.ts (React), tel.js (pages JS)                 │
├──────────────────────────────────────────────────────────────────────┤
│  AXE 2 : SAISIE (nouveau)                                            │
│  html[data-saisie="doigt" | "souris"]                                │
│  = f(réglage auto/toujours/jamais, type du DERNIER pointeur)         │
│  Source unique : public/js/saisie.js (script de tête, sans defer)     │
│  Lecteurs : CSS (sélecteurs d'attribut), useSaisie() côté React,      │
│             lecture directe de l'attribut côté pages JS               │
├──────────────────────────────────────────────────────────────────────┤
│  PRIMITIVES DE GESTE (existantes, partagées par les deux rendus)      │
│  useAppuiLong · issueAppui · useGlisser · CarteOuverte · retour       │
│  + nouvelles : fermeture au toucher ailleurs, infobulle à l'appui long│
├──────────────────────────────────────────────────────────────────────┤
│  ÉTAT DE PARTIE (board.tsx, AU-DESSUS de l'aiguillage l. 4213)        │
│  usePartieEnCours, useInteraction : survit à la rotation              │
├──────────────────────────────────────────────────────────────────────┤
│  get_world (moteur) · public/js/marvel/ : intouchables               │
└──────────────────────────────────────────────────────────────────────┘
```

La tablette n'est pas une troisième disposition : c'est **`Board` + `data-saisie="doigt"`**. Le téléphone couché de 768 px et plus est la même chose à plus petite échelle : tout ce que la tablette gagne (aperçu refermable, 44 px, infobulles), le téléphone couché le gagne gratuitement. C'est l'argument principal pour faire la tablette AVANT de trancher l'orientation.

### Responsabilités des composants

| Composant | Statut | Responsabilité | Fichier |
|---|---|---|---|
| `saisie.js` | **NOUVEAU** | Seul propriétaire de `html[data-saisie]`. Lit le réglage, écoute `pointerdown` et `pointermove` en capture sur `document`, pose l'attribut, émet `marvel:saisie`. Aucune dépendance. | `Fusion/marvel-lcg-src/public/js/saisie.js` |
| `saisie.ts` | **NOUVEAU** | Côté React : `useSaisie()` (lit l'attribut, s'abonne à l'événement), `lireReglageSaisie` / `ecrireReglageSaisie` (même clé, puis `dispatchEvent`). Fonction pure `saisieEffective(reglage, dernierType, indiceInitial)` testée en vitest. | `ui-app/src/board/saisie.ts` |
| `useModeMobile.ts` | inchangé | Axe disposition. Ne pas y mêler la saisie. | `ui-app/src/board/mobile/useModeMobile.ts` |
| `Board.tsx` | **MODIFIÉ** | `survol` (l. 1133) se tait si `data-saisie="doigt"` ; `cliquerCarte` (l. 1153) pose aussi l'aperçu au doigt ; toucher hors carte le referme ; croix passée à `CarteApercu` (l. 655). | `ui-app/src/board/Board.tsx` |
| `CarteApercu` | **MODIFIÉ** | Prop optionnelle `onFermer` : croix de 44 px, rendue seulement au doigt. | `Board.tsx` l. 655 |
| `CoucheInfobulles` | **NOUVEAU** | Un seul écouteur délégué au doigt : appui long sur un élément à `title` / `aria-label` montre une bulle, et mange le clic qui suit. Monté une fois. | `ui-app/src/board/CoucheInfobulles.tsx` |
| `board.css` | **MODIFIÉ** | Bloc `html[data-saisie='doigt']` : barre du haut à 44 px, compteurs, croix, `touch-action: manipulation`, `-webkit-touch-callout: none`. | `ui-app/src/board/board.css` |
| `FenetreReglages.tsx` | **MODIFIÉ** | Ligne « Écran tactile : automatique / toujours / jamais », montrée partout (contrairement à `montrerDisposition` l. 661). | `ui-app/src/board/FenetreReglages.tsx` |
| `board.html` + pages JS | **MODIFIÉ** (une ligne chacune) | `<script src="/public/js/saisie.js"></script>` à côté de `ui-version.js`. | `ui-app/board.html`, `public/prepare.html`, etc. |
| `app.js` (assistant) | inchangé en T1/T2 | `SANS_SURVOL` (l. 76) reste ; bascule possible plus tard vers l'attribut (voir plus bas). | `public/js/prepare/app.js` |
| `PlateauMobile` / `PlateauPortrait` / `MainPortrait` / `CarteOuverte` | modifiés seulement pour la refonte téléphone | Axe disposition < 768 px. Le doigt y est implicite : ils n'ont pas besoin de lire `data-saisie`. | `ui-app/src/board/mobile/` |

## Structure de fichiers recommandée

```
Fusion/marvel-lcg-src/public/js/
├── ui-version.js        # existant : modèle à suivre
└── saisie.js            # NOUVEAU : attribut data-saisie, avant le premier style

ui-app/src/board/
├── saisie.ts            # NOUVEAU : useSaisie, réglage, saisieEffective (pure)
├── saisie.test.ts       # NOUVEAU
├── CoucheInfobulles.tsx # NOUVEAU (T2)
├── Board.tsx            # MODIFIÉ : survol, cliquerCarte, CarteApercu
├── board.css            # MODIFIÉ : bloc [data-saisie='doigt']
├── FenetreReglages.tsx  # MODIFIÉ : réglage Écran tactile
└── mobile/              # inchangé dans son rôle (disposition < 768 px)
    ├── useAppuiLong.ts  # reste ici : déjà importé hors de mobile/, ne pas déplacer
    └── ...

ui-check/
├── playwright.config.ts # MODIFIÉ : projet « tablette-doigt » (1180x820, hasTouch, isMobile)
└── tests/tablette.spec.ts # NOUVEAU
```

### Justification

- **`saisie.js` dans `public/js/`, pas dans `ui-app/`** : c'est le seul endroit chargeable à la fois par le plateau React (`board.html` charge déjà `/public/js/ui-version.js` par chemin absolu, relayé par le proxy de Vite en dev) et par les pages JS. Une seule implémentation de la bascule, donc une seule règle à tester et pas deux comportements divergents.
- **`saisie.ts` à la racine de `board/`, pas dans `mobile/`** : la saisie concerne d'abord le plateau PC. Le ranger sous `mobile/` refait l'erreur de `useAppuiLong`, rangé là puis importé par `manuel/`.
- **Ne pas déplacer `useAppuiLong`** ni créer un dossier `gestes/` : déplacement pur sans gain fonctionnel, contraire à « pas de refacto opportuniste ».

## Patterns architecturaux

### Pattern 1 : un attribut sur la racine, propriétaire unique

**Quoi :** `saisie.js` est le seul code qui écrit `document.documentElement.dataset.saisie`. Tout le reste le lit : le CSS par sélecteur d'attribut, React par `useSaisie()`, les pages JS par lecture directe.
**Quand :** toute préférence qui doit valoir avant le premier rendu (sinon la barre du haut saute de 30 à 44 px au premier toucher) et qui traverse React et le JS non compilé.
**Compromis :** la logique de bascule n'est pas en TS strict ; elle tient en une trentaine de lignes et se teste en Playwright (tap puis souris). La décision pure est dupliquée dans `saisie.ts` pour vitest, avec un test qui compare les deux sur la même table de cas si on veut verrouiller l'accord (le précédent `affichage.ts` / `affichage-choix.js` vit déjà avec cette duplication).

**Exemple :**
```js
// public/js/saisie.js (esquisse, à écrire en phase T1)
(function () {
  "use strict";
  var CLE = "mc_ecran_tactile_v1";           // "auto" | "toujours" | "jamais"
  var racine = document.documentElement;
  function reglage() { try { return localStorage.getItem(CLE) || "auto"; } catch (e) { return "auto"; } }
  // Avant tout geste : iPad se déclare Mac, maxTouchPoints le trahit.
  var dernier = (navigator.maxTouchPoints > 1 || matchMedia("(pointer: coarse)").matches) ? "doigt" : "souris";
  function poser() {
    var r = reglage();
    var s = r === "toujours" ? "doigt" : r === "jamais" ? "souris" : dernier;
    if (racine.dataset.saisie !== s) { racine.dataset.saisie = s; window.dispatchEvent(new CustomEvent("marvel:saisie")); }
  }
  function noter(e) {
    var s = e.pointerType === "mouse" ? "souris" : "doigt";   // touch et pen = doigt
    if (s !== dernier) { dernier = s; poser(); }
  }
  document.addEventListener("pointerdown", noter, true);
  document.addEventListener("pointermove", function (e) { if (e.pointerType === "mouse") noter(e); }, true);
  window.addEventListener("marvel:saisie-reglage", poser);
  window.addEventListener("storage", function (e) { if (e.key === CLE) poser(); });
  poser();
})();
```

Points vérifiés qui justifient ce choix : sur iPad avec Magic Keyboard, les media queries répondent `(hover: none)` et `(pointer: coarse)` alors que le trackpad envoie bien des `pointerType: "mouse"` (source ci-dessous, confiance MOYENNE). Une media query ne peut donc PAS faire la décision 4 ; seul le type du dernier événement pointeur le peut. Les événements souris de compatibilité émis après un toucher ne sont pas des `PointerEvent` : ils ne font pas rebasculer vers « souris ».

### Pattern 2 : la saisie se lit au moment du geste, la disposition au moment du montage

**Quoi :** l'aiguillage `Board` / `PlateauMobile` reste une décision de montage (`useModeMobile`). La saisie, elle, ne remonte jamais de composant : elle change des gardes dans les gestionnaires et des règles CSS.
**Quand :** toujours. Un `RenduPartie` qui dépendrait de la saisie démonterait le plateau à chaque passage doigt / trackpad sur iPad.
**Compromis :** `Board` doit gérer les deux saisies dans le même composant. C'est voulu : c'est la définition du « mode tablette simple ».

**Exemple :**
```tsx
// Board.tsx l. 1133 : une garde de plus, rien d'autre ne bouge.
const survol = useCallback((evenement: ReactMouseEvent) => {
  if (enGlisserRef.current) return
  if (document.documentElement.dataset.saisie === 'doigt') return  // souris de compatibilité
  ...
}, [])
// cliquerCarte (l. 1153) : au doigt, le même toucher pose l'aperçu ET le menu (décision 1).
```

Lire l'attribut directement dans le gestionnaire (plutôt que via l'état React) évite un rendu de retard au premier toucher : `saisie.js` écoute en capture sur `document`, il a donc déjà basculé quand le `pointerup` du plateau arrive.

### Pattern 3 : un écouteur délégué plutôt que cinquante enveloppes

**Quoi :** l'infobulle à l'appui long (décision 7) passe par un seul écouteur posé au niveau du plateau, qui lit `title` ou `aria-label` de l'élément tenu, au lieu d'envelopper chaque bouton.
**Quand :** les 55 `title={...}` et 14 `onMouseEnter` / `onMouseOver` recensés dans `ui-app/src/board/*.tsx` (hors tests).
**Compromis :** il faut manger le `click` qui suit un appui long ayant montré la bulle (même idée que `vientDeDeclencher` de `useAppuiLong`), via un écouteur `click` en capture. Même logique que `apercu-survol.ts` : un écouteur sur le conteneur, l'état dérivé de ce qui est sous le doigt.

### Pattern 4 : ce qui doit survivre à la rotation vit au-dessus de l'aiguillage

**Quoi :** l'état d'interaction (`useInteraction`, `usePartieEnCours`) est déjà dans `board.tsx`, au-dessus de `RenduPartie` (l. 4213). Tout état local de `Board` ou de `PlateauPortrait` (aperçu, feuille ouverte, carte agrandie) meurt quand on franchit 768 px en tournant le téléphone.
**Quand :** si l'orientation retenue est « les deux ». Le retour 6 de Raven (Fin du tour posée sur la main après plusieurs rotations) est un symptôme de ce passage.
**Compromis :** remonter un état coûte des props ; ne remonter que ce qui gêne vraiment (une question en cours, jamais un aperçu).

## Flux de données

### Réglage « Écran tactile »

```
FenetreReglages (React)              burger des pages JS (plus tard, facultatif)
        │ ecrireReglageSaisie()               │ localStorage.setItem(CLE)
        ▼                                     ▼
localStorage["mc_ecran_tactile_v1"] ── "marvel:saisie-reglage" / "storage"
        │
        ▼
public/js/saisie.js : poser()  ──►  html[data-saisie]  ──►  "marvel:saisie"
                                         │                        │
                              CSS [data-saisie='doigt']     useSaisie() (React)
```

Par appareil, comme `mode-plateau` et les réglages du téléphone (`reglages-telephone.ts`) : pas d'envoi à `/save_preferences`. Un compte joue sur PC et sur iPad, l'écran tactile est une propriété de l'appareil.

### Détection (dernier geste)

```
pointerdown / pointermove (capture, document)
   pointerType touch|pen -> "doigt"     pointerType mouse -> "souris"
        │
        ▼
réglage "toujours" | "jamais" l'emporte ; "auto" suit le dernier geste
        │
        ▼
html[data-saisie]   (lu au geste suivant par Board.tsx, au rendu par CSS)
```

### Gestes sur le plateau PC au doigt

```
toucher une carte ─► pointerup sur .plateau-cadre
                       ├─ glisser terminé ? (gestes.onPointerUp) -> rien d'autre
                       ├─ cliquerCarte -> onCardClick -> menu (inchangé)
                       └─ NOUVEAU : setApercuId(id) si saisie = doigt
toucher hors carte  ─► pointerup sans .scan-card -> setApercuId(null)
toucher hors cadre  ─► pointerdown capture sur document, aperçu ouvert -> fermer
                       (sauf dans .menu-actions-carte : le menu reste utilisable)
croix de l'aperçu   ─► onFermer -> setApercuId(null)
```

L'aperçu est publié au spectateur (`publierVu(playerId, 'loupe', ...)`, `Board.tsx` l. 1327) : un aperçu ouvert au doigt y apparaîtra comme au survol. Comportement voulu, rien à changer.

## Paliers d'écran (à la place de la « montée en charge »)

| Appareil | Disposition | Saisie | Ce qui change en v1.1 |
|---|---|---|---|
| PC souris | Board | souris | Rien. Cible de non-régression. |
| PC tactile (Windows) | Board | bascule auto | Gagne le mode tablette au premier toucher ; « jamais » pour le couper. |
| iPad seul | Board | doigt | Lots T1, T2. |
| iPad + trackpad | Board | bascule auto | Survol rendu au trackpad. Le menu en feuille basse reste (`(pointer: coarse)` dans `board.css` l. 2163 continue de répondre vrai). |
| Téléphone couché >= 768 px | Board réduit | doigt | Profite de T1/T2 sans travail dédié. |
| Téléphone couché < 768 px | PlateauPortrait (règles paysage) | doigt implicite | Refonte téléphone. |
| Téléphone debout | PlateauPortrait | doigt implicite | Refonte téléphone. |

## Orientation du téléphone : structure selon la décision

- **« Portrait seul »** : rien de structurel. `useVerrouPortrait` et `EcranTourne` existent (`telephone.ts` l. 200 et suivantes, `board.tsx` l. 4710) ; on passe le verrou à « oui » par défaut et on retire du filet les cas couchés. Limite connue : iOS Safari refuse `screen.orientation.lock` hors application installée, il faut donc garder l'écran « Tourne ton téléphone ».
- **« Paysage seul »** : contraire à toute la refonte d'octobre (zones 1 à 3 en portrait) et à la recherche du jalon précédent. Non recommandé.
- **« Les deux »** (le plus probable vu l'existant) : garder exactement les deux rendus actuels, **ne pas recréer de `PlateauPaysage`**. Debout = `PlateauPortrait` ; couché = `Board` au doigt (donc la tablette). Trois points structurels :
  1. le critère de bascule reste la largeur à 768 px (cohérent avec `tel.js` et les pages). Le cas 667 x 375 (petit téléphone couché, bandes) est le seul à trancher : soit il garde les bandes, soit `REQUETE_MOBILE` devient `(max-width: 767px) and (orientation: portrait)` et il passe au plateau PC à l'échelle minimale. À décider avec captures, c'est un changement d'une ligne mais au comportement large ;
  2. tout état qui doit survivre au tour d'écran remonte au-dessus de `RenduPartie` (Pattern 4) ;
  3. `REQUETE_TELEPHONE` (fonctions du téléphone) et `REQUETE_PAYSAGE_TEL` (échelle) restent des détections d'APPAREIL, distinctes de la saisie : ne pas les remplacer par `data-saisie`, sinon un iPad recevrait les vibrations et l'échelle minimale du téléphone.

## Assistant JS et plateau React : ce qu'ils partagent

| Élément | Partagé ? | Comment |
|---|---|---|
| Seuil de disposition 768 px | oui, par convention | Deux constantes (`useModeMobile.ts`, `tel.js`). Ne pas fusionner : un module commun TS / JS non compilé coûterait plus qu'il ne rapporte. |
| Réglage « Écran tactile » | oui | Même clé localStorage, même attribut posé par le même `saisie.js`. |
| Attribut `data-saisie` | oui | Disponible sur toutes les pages qui chargent `saisie.js`. |
| Primitives de geste | **non** | `useAppuiLong` est un hook React ; l'assistant a ses propres gestes en JS (`tel.js` : poignée de feuille basse, glisser latéral de `app.js` l. 3700). Les réécrire en module commun = refacto non demandée. Partager les SEUILS (450 ms, 44 px, 90 px de fermeture) par une note dans le code suffit. |
| Survol de l'assistant | à reprendre plus tard | `SANS_SURVOL` (l. 76) est figé au chargement et vaut « sans survol » sur iPad même avec un trackpad. Remplacer `auSurvol` par une lecture de `data-saisie` au rendu corrigerait le cas, mais le jalon ne le demande pas : à classer en T3 ou en backlog. |

## Anti-patterns

### Anti-pattern 1 : une troisième disposition « tablette »
**Quoi :** un `PlateauTablette` ou une valeur `'tablette'` dans `ModeRendu`.
**Pourquoi c'est mauvais :** refusé explicitement (fiche du 12/10, « pas une troisième mise en page »), triple la surface de test, et le paysage téléphone en a déjà payé le prix (`PlateauPaysage` supprimé faute d'usage).
**À la place :** `Board` + `data-saisie`.

### Anti-pattern 2 : mettre la saisie dans `useModeMobile`
**Quoi :** ajouter « doigt » au réglage `mode-plateau` ou au calcul de `mode`.
**Pourquoi c'est mauvais :** chaque passage doigt / trackpad démonterait le plateau ; l'historique du fichier (l. 20 à 30) montre déjà deux allers-retours sur `(pointer: coarse)` dans cette requête.
**À la place :** deux axes séparés.

### Anti-pattern 3 : remplacer les `(pointer: coarse)` existants d'un coup
**Quoi :** réécrire `board.css` l. 2163, 5602, 6017 en `[data-saisie='doigt']`.
**Pourquoi c'est mauvais :** ces règles servent aujourd'hui le téléphone couché et l'iPad ; les changer modifie le PC tactile et l'iPad + trackpad sans qu'on l'ait décidé.
**À la place :** AJOUTER un bloc `[data-saisie='doigt']` pour ce qui est neuf (44 px, croix, callout) ; ne toucher aux anciennes requêtes que sur un défaut constaté.

### Anti-pattern 4 : se fier à `(hover: hover)` ou `(pointer: fine)` pour l'iPad
**Pourquoi c'est mauvais :** faux sur iPad avec trackpad (source ci-dessous), et c'est exactement la décision 4.
**À la place :** le type du dernier `PointerEvent`.

### Anti-pattern 5 : envelopper chaque bouton pour l'infobulle
**Pourquoi c'est mauvais :** 55 sites, autant de diffs dans des fichiers que la phase du méchant vient de remanier.
**À la place :** `CoucheInfobulles`, écouteur délégué.

## Points d'intégration

### Frontières internes

| Frontière | Communication | Risque PC |
|---|---|---|
| `saisie.js` -> React | attribut + `CustomEvent('marvel:saisie')` | Nul si l'attribut vaut « souris » par défaut sur PC : `maxTouchPoints` vaut 0 sur un PC sans écran tactile. À vérifier sur un portable Windows tactile (il passera en doigt au premier toucher, c'est voulu). |
| `FenetreReglages` -> `saisie.js` | localStorage + `marvel:saisie-reglage` | Faible : une ligne de réglage en plus. |
| `Board.tsx` `survol` / `cliquerCarte` | garde sur l'attribut | **Le plus sensible** : chemin du clic de toute partie PC. Exiger que `Board.test.tsx` et `apercu-refus.test.tsx` restent verts sans attribut posé (jsdom = souris). |
| `board.css` bloc doigt | sélecteur d'attribut | Nul sans l'attribut. La barre de 44 px change la hauteur de `.plateau-cadre` : `useEchelle` (l. 156, `ResizeObserver`) recalcule seul, mais l'échelle de la table baisse de quelques pour cent sur iPad. |
| `usePlacement` (panneaux) | mesures DOM | La croix et la barre plus haute déplacent des boîtes : `boites.test.ts` / `placer.test.ts` sont purs et ne bougent pas ; contrôle visuel en Playwright. |
| `board.tsx` `RenduPartie` | aiguillage par largeur | Inchangé, sauf décision « les deux » sur le cas 667 px. |
| Pages JS (`prepare.html`, `cards.html`, `deck.html`, `replay.html`, `galerie.html`, `campagne.html`) | une balise `<script>` | Nul tant qu'aucun CSS de ces pages ne lit `data-saisie`. Attention au mémo : `launcher.py` copie `public/` dans `.game/`, un fichier ajouté après démarrage est en 404 silencieux. |

### Filets de test

- **Vitest** : `saisie.test.ts` (table de cas de `saisieEffective`), `Board.test.tsx` complété (doigt : toucher = aperçu + menu ; toucher ailleurs ferme ; croix ferme ; souris inchangée).
- **Playwright** : nouveau projet `tablette-doigt` (1180 x 820, `hasTouch: true`, `isMobile: true`), à côté du gabarit `tablette` souris qui reste la référence de non-régression. Un test « bascule » : `page.touchscreen.tap` puis `page.mouse.move`, attendre l'attribut. Un test « 44 px » réutilisant le contrôle de `pages-telephone.spec.ts`.
- **Non-régression PC** : captures de référence `pc` et `tablette` existantes, qui doivent rester identiques au pixel (même méthode que la zone 2 le 10/10 : « PC comparé avant/après au pixel, identique »).

## Ordre de construction conseillé

1. **`saisie.js` + `saisie.ts` + projet Playwright `tablette-doigt`** (rien de visible). Tout le reste en dépend, et le projet de test doit exister avant la première modification de `Board.tsx`. Préalable : `boutons-bd.test.ts` est déjà rouge (fiche du 12/10) ; le constater et le noter avant, pour ne pas l'attribuer au jalon.
2. **T1 : aperçu refermable dans `Board.tsx`** (garde de `survol`, aperçu au toucher, fermeture hors carte, croix) + bloc CSS minimal (`touch-action: manipulation`, `-webkit-touch-callout: none`) + réglage dans `FenetreReglages`. C'est le seul point bloquant ; il bénéficie aussi au téléphone couché.
3. **T2 : 44 px** (barre, compteurs, croix) puis **`CoucheInfobulles`** puis raison « injouable » au toucher (`raisons` déjà passées à `CarteApercu`, l. 1541 : il suffit que l'aperçu s'ouvre au doigt, ce que fait l'étape 2).
4. **Décision d'orientation du téléphone** (recherche + captures), AVANT de toucher `PlateauPortrait`. Elle profite de l'étape 2 : le plateau couché sera alors jouable, donc comparable.
5. **Refonte téléphone, menus** (assistant, galerie, éditeur, campagne, salon) : surtout `app.js`, `tel.js`, `tel-pages.js`, CSS. Indépendante du plateau, peut avancer en parallèle de 2 et 3 (fichiers disjoints), sauf la balise `saisie.js` posée à l'étape 1.
6. **Refonte téléphone, plateau** (`PlateauPortrait`, `MainPortrait`, `Bande`, `CarteOuverte`), dans la structure dictée par l'étape 4.
7. **(Plus tard, T3)** mode manuel au doigt, `SANS_SURVOL` de l'assistant branché sur `data-saisie`, vérification sur un vrai iPad.

Contrainte d'ordonnancement externe : la fiche du 12/10 demande de lancer T1 « après la passe de finition de la refonte de la phase du méchant (mêmes fichiers du plateau) ». `Board.tsx`, `board.css` et `board.tsx` sont aussi ceux de cette refonte : vérifier qu'elle est close (et `git stash list`, deux sessions sur le même arbre) avant l'étape 2.

## Ce qui reste incertain

- Le comportement exact de Safari iPad (événements de compatibilité, délai du double-toucher, `pointermove` du trackpad au repos) n'est vérifié que par la documentation et une issue GitHub : rien n'a été essayé sur un iPad. À valider en T3.
- La valeur initiale avant tout geste sur un portable Windows tactile avec souris : `maxTouchPoints > 1` le classerait « doigt » jusqu'au premier mouvement de souris. Le `pointermove` souris rebascule tout de suite, mais la barre aura brièvement 44 px. Acceptable ou à affiner (`(any-hover: hover)` en indice) : à trancher en phase.
- Le sort du cas 667 x 375 si l'orientation est « les deux ».

## Sources

- Code lu : `ui-app/src/board/mobile/useModeMobile.ts`, `telephone.ts`, `reglages-telephone.ts`, `useAppuiLong.ts`, `PlateauMobile.tsx`, `CarteOuverte.tsx` ; `ui-app/src/board/Board.tsx` (l. 143 à 200, 1100 à 1560) ; `ui-app/src/board.tsx` (l. 1470 à 1550, 1835 à 2010, 4205 à 4220) ; `ui-app/src/board/affichage.ts`, `apercu-survol.ts`, `manuel/appui-tactile.ts`, `placement/` ; `ui-app/board.html`, `vite.config.ts` ; `public/js/ui-version.js`, `public/js/prepare/tel.js`, `public/js/tel-pages.js`, `public/js/prepare/app.js` (l. 60 à 80, 712 à 740, 5475 à 5500), `public/js/prepare/affichage.js` ; `ui-check/playwright.config.ts`. Confiance HAUTE.
- `git log -- '*PlateauPaysage*'` : suppression par `9f0b6fac`. Confiance HAUTE.
- [Issue t3code #14868 : iPad Safari + Magic Keyboard, `(hover: none)` et `(pointer: coarse)` malgré des `pointerType: "mouse"`](https://github.com/pingdotgg/t3code/issues/14868) et [WebKit bug 214609](https://bugs.webkit.org/show_bug.cgi?id=214609). Confiance MOYENNE (pas de test sur appareil).
- [Apple : utiliser une souris ou un trackpad avec l'iPad](https://support.apple.com/en-us/105004). Confiance MOYENNE.
