# TODO / SPEC — Mode Découverte : apprendre le jeu en jouant

**Statut :** **IMPLÉMENTÉ** le 2026-08-03. Reste à jouer le tutoriel de bout en bout dans le navigateur, et à relire le texte des 11 leçons avec l'utilisateur.
**Plan d'implémentation :** `.planning/plans/2026-08-03-tutoriel-decouverte.md`
**Date de conception :** 2026-08-03
**Origine :** demande utilisateur (« j'aimerais faire un tutoriel pour le jeu Marvel Champions et pour l'utilisation du programme »)
**Rapport à la roadmap :** indépendant des 7 phases de la refonte UI. Ne dépend d'aucune d'elles et n'en bloque aucune.

---

## 1. Le problème

Quelqu'un qui ne connaît ni Marvel Champions ni ce programme ne peut pas commencer seul. Le livret d'apprentissage officiel fait une vingtaine de pages, et le plateau, même clair, suppose qu'on sait déjà ce qu'est une manigance, une forme alter-ego ou une carte de boost.

On veut l'amener **jusqu'à sa première partie terminée**, sans qu'il ait rien lu avant.

## 2. Décisions prises avec l'utilisateur

| Question | Décision |
|---|---|
| Public | Quelqu'un qui découvre **et** le jeu **et** le programme |
| Forme | Une **partie guidée dans le jeu**. Une page d'aide écrite a été envisagée puis écartée |
| Dirigisme | Le coach donne **une mission à la fois** et laisse jouer. Il ne bloque **jamais** rien |
| La partie | **Figée** : Spider-Man contre Rhino, seed 42 |
| Périmètre du « tour du programme » | Le **plateau** dans ce chantier. Les autres écrans (préparation, deck-builder, galerie, multi) feront l'objet d'un second chantier |

**Pourquoi « il ne bloque jamais rien ».** L'option dirigiste (seul le bon coup est cliquable) obligerait à filtrer ce que le moteur propose : on mentirait au joueur sur ce qui est légal, et le tutoriel se coincerait dès que la partie dévie du script. Un coach qui observe ne peut, lui, rien casser.

## 3. Ce qui existe déjà (vérifié le 3/8/2026)

- **Le plateau sait se superposer.** `SplashTour.tsx` (« à qui le tour »), `CoucheSucces.tsx` (bannière de succès) et `CoucheRevelation.tsx` sont des couches par-dessus la table. Le coach est une couche de plus, dans le même moule.
- **Le glossaire des mots-clés existe** : `ui-app/src/board/mots-cles.ts`, avec le vocabulaire OFFICIEL FR (Garde, Renfort, Déferlement, Robuste…), déjà affiché en infobulle. Le coach y renvoie, il ne le duplique pas.
- **Le wizard a déjà un mode à mise en place particulière** : `sandbox` (`MODES` dans `public/js/prepare/app.js`). Le mode Découverte s'ajoute à cette liste.
- **L'assistant d'action existe** : `AssistantAction.tsx` guide déjà « choisis une action → une cible → paie ». Le coach est au-dessus : il dit QUOI viser, l'assistant dit COMMENT.
- **La partie est déterministe.** Mesuré deux fois de suite, Spider-Man contre Rhino avec seed 42 : main de départ et ordre du deck **identiques**.

## 4. La main de départ, seed 42

C'est elle qui rend les leçons possibles. Relevé le 3/8/2026 :

| Carte | Type | Coût | Rôle dans le tutoriel |
|---|---|---|---|
| 01005 Swinging Web Kick | Événement | 3 | Leçon « jouer une carte » et « attaquer fort » |
| 01060 For Justice! | Événement | 2 | Leçon « contrer » |
| 01092 Helicarrier | Soutien | 3 | Montre qu'on ne peut pas tout se payer |
| 01065 Heroic Intuition | Amélioration | 2 | Idem |
| 01009 Webbed Up | Amélioration | 4 | Trop chère au tour 1 : sert l'idée de priorité |
| 01061 Great Responsibility | Événement | 0 | Notion avancée, non enseignée |

Les cartes suivantes du deck sont 01061, 01059 (Jessica Jones), 01058 (Daredevil), 01064, 01004 : **deux alliés arrivent vite**, ce qui rend la leçon « fais entrer un allié » atteignable au tour 2 ou 3.

⚠️ **Conséquence de conception.** Les leçons peuvent nommer une carte précise (« Coup de pied volant ») car la main est garantie. Elles ne doivent en revanche **jamais** désigner une carte par sa POSITION : l'ordre d'affichage dépend de ce que le joueur a déjà joué.

## 5. Architecture

```
Wizard : nouveau mode « Découverte »
        └─ lance directement Spider-Man / Rhino / seed 42, sans les 5 étapes
                    │
                    ▼
Plateau ── <CoucheCoach world={world} /> ── couche par-dessus la table
                    │
                    ├─ lit l'ÉTAT du monde (le même que la table affiche)
                    ├─ compare à la mission courante
                    └─ mission accomplie → félicite → mission suivante
```

Trois unités, chacune avec un seul rôle :

### 5.1 `ui-app/src/board/lecons.ts` — le contenu, et rien d'autre

Un tableau de leçons. Chacune : un identifiant, un titre, un texte, et une fonction qui dit si la mission est remplie. Aucun DOM, aucun React : **testable sous Node**, comme `libelles-cible.ts` et `salon-etat.js`.

Plusieurs missions se formulent par une VARIATION (« Rhino a encore perdu des PV », « la menace a baissé de 2 »), pas par un état absolu. L'état courant seul ne suffit donc pas : il faut le comparer à un **repère** pris au moment où la leçon a commencé.

```ts
/** Ce qu'on retient de l'état au début d'une leçon, pour mesurer une variation. */
export type Repere = {
  pvVilain: number
  menacePrincipale: number
  pvIdentite: number
  round: number
  cartesEnMain: string[]   // card_id
}

export type Lecon = {
  id: string
  titre: string
  texte: string
  /** Vrai quand la mission est remplie. Lit, ne modifie rien. */
  accomplie: (monde: World, repere: Repere) => boolean
  /** Vrai si la mission ne se détecte pas et s'enchaîne au clic. */
  manuelle?: boolean
}

/** Prend le repère. Appelée une fois, à l'entrée dans la leçon. */
export function prendreRepere(monde: World): Repere
```

`prendreRepere` est appelée par `CoucheCoach` à chaque changement de leçon, et son résultat conservé jusqu'à la suivante. C'est la seule chose que la couche mémorise ; tout le reste se déduit du monde.

### 5.2 `ui-app/src/board/CoucheCoach.tsx` — l'affichage

Un bandeau discret, repliable, jamais modal, `pointer-events: none` sauf sur ses boutons — même règle que `SplashTour`. Trois boutons : **Replier**, **Passer cette leçon**, **Quitter le tutoriel**.

### 5.3 `public/js/prepare/app.js` — le mode dans le wizard

Une entrée de plus dans `MODES`, et un raccourci de lancement : le mode Découverte saute les 5 étapes et appelle `launch()` avec un état pré-rempli.

## 6. Les leçons

### Track A — jouer (7 leçons)

| # | Mission affichée | Détection (`accomplie`) |
|---|---|---|
| 1 | « Tu es Peter Parker, en civil. Passe en Spider-Man. » | `area_hero[0].card_type === 'Hero'` |
| 2 | « Joue *Coup de pied volant* sur Rhino. » | 01005 était dans `repere.cartesEnMain` et n'est plus dans `hand_cards` |
| 3 | « Attaque Rhino avec ton héros. » | `info.health` de Rhino **<** `repere.pvVilain` |
| 4 | « Retire 2 menaces de la manigance principale. » | `area_schemes_main[0].info.k_threat` **≤** `repere.menacePrincipale - 2` |
| 5 | « Termine ton tour et regarde ce que fait Rhino. » | `round_id` **>** `repere.round` |
| 6 | « Fais entrer un allié en jeu. » | `players[0].allies.length > 0` |
| 7 | « Repasse en Peter Parker pour récupérer. » | `card_type === 'AlterEgo'` **et** PV de l'identité **>** `repere.pvIdentite` |

### Track B — le plateau (4 leçons)

| # | Mission affichée | Détection |
|---|---|---|
| 8 | « Survole une carte pour l'agrandir et lire ses mots-clés. » | `manuelle: true` — bouton **J'ai compris** |
| 9 | « Ouvre le panneau ⚙ : animations, sons, météo, succès. » | idem |
| 10 | « Tu as fait une erreur ? La touche U annule le dernier coup. » | idem |
| 11 | « L'historique en bas rejoue tout ce qui s'est passé. » | idem |

Les leçons 8 à 11 ne se détectent pas : observer un survol ou l'ouverture d'un panneau demanderait d'instrumenter l'interface pour un gain nul. Elles s'enchaînent au clic.

Après la leçon 11, le coach passe en **mode commentaire** : il ne demande plus rien et signale seulement les moments notables (le méchant attaque, une manigance annexe entre en jeu), jusqu'à la fin de la partie.

## 7. Comment la progression est mémorisée

`localStorage`, clé `marvel-board-tutoriel`, valeur = identifiant de la leçon courante. Le joueur peut fermer l'onglet et revenir. « Quitter le tutoriel » écrit `fini` : le coach ne réapparaît plus, sauf à relancer le mode Découverte.

Le coach ne s'affiche **que** si cette clé existe et vaut autre chose que `fini`. Une partie normale n'est jamais concernée.

## 8. Erreurs et cas limites

| Cas | Comportement |
|---|---|
| Le joueur fait la leçon 4 avant la 3 | La détection est évaluée à chaque rendu : la leçon passée en avance est validée dès qu'on l'atteint |
| Le joueur perd la partie pendant le tutoriel | Le coach affiche « on recommence quand tu veux » et propose de relancer le mode Découverte |
| Le joueur gagne avant la leçon 7 | Les leçons restantes sont sautées, le coach félicite |
| Une leçon devient impossible (la carte a été défaussée) | Le bouton **Passer cette leçon** est toujours là. C'est le filet |
| Le joueur ouvre le tutoriel en multi | Non prévu : le mode Découverte est solo. Le coach lit `players[0]` |
| Reprise d'une sauvegarde en cours de tutoriel | La progression suit le localStorage, pas la partie : elle est conservée |

## 9. Tests

1. **`lecons.ts` est pur** → un script Node vérifie chaque `accomplie()` sur des états de monde fabriqués à la main, dont les cas limites (aucun allié, menace inchangée, forme héros). Sur le modèle de `ui-app/outils/verifier-libelles-cible.mjs`.
2. **Le déterminisme du seed** → un script Python relance deux fois Spider-Man/Rhino seed 42 et compare main et deck. Si un jour le moteur change son tirage, ce test le dira **avant** que les leçons deviennent fausses. C'est le test le plus important de ce chantier.
3. **Bout en bout** → manuel : jouer le tutoriel du début à la fin.

## 10. Ce qui n'est PAS dans ce périmètre

- Les autres écrans : préparation, deck-builder, galerie, multi. Second chantier.
- Les règles avancées : némésis, campagnes, sets modulaires, défis, multi.
- Toute traduction du livret officiel : on enseigne **assez pour finir une partie**, pas l'intégralité du guide de référence.
- Le blocage des coups illégaux ou non désirés (voir §2).
