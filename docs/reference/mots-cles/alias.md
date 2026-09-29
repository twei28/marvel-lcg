# Alias (mot-clé maison, aspect Determination)

**Texte imprimé / définition** : « Alias. *(If you control a card with a
matching subtitle, discard it and play this card for free.)* » (rappel
imprimé sur `dt100` ; `dt105`, `dt106`, `dt107` portent le mot nu).

Définition MC4DB (règle `fanmade`, 29/09/2026) : « If you control a card
with a matching subtitle, discard it and play this card for free. Ignore
Unique Rule when deckbuilding. » Première phrase identique. La seconde n'a
pas d'équivalent chez nous, voir « Pièges connus ».

**Mécanisme moteur** : aucun crochet natif. Deux aptitudes écrites UNE fois,
`Alias()` dans `src/cards/pack/determination/__init__.py`, posées par
`*Alias()` dans chaque carte qui le porte :

- `AbilityFactory.ReduceCostToPlayThis(lambda effect: effect.this.printed_cost,
  conditions=[controle_un_homonyme])` : le coût tombe à zéro tant que le
  joueur contrôle une AUTRE carte dont `paper.subtitle` est égal au sien ;
- `AbilityFactory.AfterCardEnterPlay(AbilityType.ForcedResponse, "This",
  defausser_l_homonyme)` : à l'entrée en jeu, le premier homonyme contrôlé
  est défaussé (`Faces.DiscardAll(homonymes[:1], effect)`).

Les deux sont liées par le texte (« on joue gratuitement PARCE QU'on
défausse ») mais indépendantes dans le code : si l'homonyme quitte le jeu
entre le paiement et l'entrée en jeu, la carte est quand même gratuite.

**Carte exemple** : `dt100` * Archangel : `return [Reckless(), *Alias(),
...]`. Autres porteurs : `dt105` * Venompool, `dt106` * Captain Universe,
`dt107` * Zenpool.

**Pièges connus** :
- ⚠ **DEUX DÉFAUTS L'ONT RENDU INERTE JUSQU'AU 29/09/2026**, corrigés le
  même jour (gabarit
  `.planning/todos/2026-09-29-fleeting-alias-gabarits-processus-carte.md`) :
  1. les quatre porteurs avaient un `subtitle` VIDE dans `cards.json`, et les
     deux aptitudes rendent la main dès que le sous-titre est vide. Les
     sous-titres imprimés, lus sur les scans : Archangel = « Warren
     Worthington III » (homonymes `33019`, `41003` Angel) ; Venompool,
     Captain Universe (version Deadpool) et Zenpool = « Wade Wilson »
     (homonymes `40024`, `dt016` Deadpool) ;
  2. `ReduceCostToPlayThis(lambda effect: effect.this.printed_cost)` rendait
     l'objet `Cost` : la fabrique multiplie (`base_val * fn(effect)`), d'où
     un `TypeError` avalé par le moteur, visible seulement dans
     `/tmp/capacites_*.log`. Il faut `.val`. Une réduction de coût qui « ne
     part jamais » sans message : lire ce journal avant de chercher ailleurs.
  Preuve : cinq cas `[dt]` de `tools/test_capacites.py` (quatre sujets + un
  témoin sans homonyme), rouges avant, verts après.
- « Ignore Unique Rule when deckbuilding » (MC4DB) : la règle d'unicité
  officielle ne s'applique qu'EN JEU (deux cartes uniques de même nom), pas
  au deckbuilding, et Archangel/Angel, Zenpool/Deadpool n'ont pas le même
  nom. L'éditeur (`public/js/deckbuilder/regles.js`) ne connaît d'ailleurs
  aucune règle d'unicité : il ne plafonne que le nombre d'exemplaires par
  titre (`maxParDeck`). Rien à respecter, rien à corriger.
- Le mot-clé n'est pas lu dans `desc` : une carte qui l'imprime sans
  `*Alias()` est inerte, et `verifier_desc_mots_cles` ne le voit pas.

**Variantes maison** : aucune. « Alias » est aussi un mot du jeu officiel
(l'ALIAS d'une identité, en règle) : ne pas confondre, ce mot-clé-ci ne
parle que du sous-titre imprimé sous le nom d'un allié.
