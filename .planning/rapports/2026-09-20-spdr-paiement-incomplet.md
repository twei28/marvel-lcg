# Paiement incomplet : la carte partait à la défausse et la ressource restait dépensée

Signalement n°18 du 20/09/2026, par Yarro. Branche `mode-manuel`.

## Ce que Yarro décrit

> « Quand tu veux payer le coût pour jouer une carte, tu peux incliner une
> interface pour générer une ressource. Cela fonctionne mais il faut respecter
> un ordre précis si tu as un mix entre payer de ta main et payer avec la capa
> d'SP//dr. En gros si jamais tu fais un mix et tu choisis d'abord de payer par
> la capa d'SP//dr et que par exemple pour une carte qui coûte 2, tu n'inclines
> qu'une interface. Il va te l'incliner et mettre la carte que tu veux en
> défausse. Pour jouer la carte il faut d'abord payer une carte de ta main et
> ensuite déclencher la capa d'SP//dr. »

## La reproduction

Position montée avec `tools/test_capacites.py` (héros `sp_dr`, scénario
`rhino`) :

- forme héros, donc **deux interfaces** en jeu : `31002b` SP//dr (ressource
  imprimée mentale) et `31012` Speed-Metal Alloy (physique) ;
- main réduite à une seule carte, `31022` Spider-Man, **coût 2** ;
- le seul moyen de paiement offert est Sync Ratio, la capacité de ressource de
  `31001a` SP//dr Suit.

Trace du pilote, moteur d'origine :

```
JOUER   31022 | jouable = True
PAIEMENT Play | cout = 2 | payment = [{'2': 'RG'}] | choisies = ['2'] | couvert = 2
APRES   31022 | en main = False | zone = SP//dr's DiscardPile<5>
```

Sync Ratio **annonce** `RG`, soit 2 ressources : de quoi couvrir le coût, et
le moteur accepte le paiement sur cette annonce. Au moment de payer, son coût
`CostFunc.Exhaust(range=(1, "All"))` demande combien d'interfaces incliner ;
une seule est inclinée, donc **une seule ressource est générée**. Le coût de 2
n'est pas couvert.

Résultat constaté, exactement le signalement : `31002b` reste **incliné**, et
`31022` finit dans la **défausse** sans avoir été jouée. Perte sèche des deux
côtés, en un clic, sans message.

Le second témoin monte le « mix » de Yarro : `31010` Host Spider à coût 3,
payée par Sync Ratio (annonce 2) **plus** `31004` de la main (1). Une seule
interface inclinée : 1 + 1 = 2 < 3. Avant correctif, les **trois** cartes sont
perdues : `31010` et `31004` en défausse, l'interface inclinée.

## Où le paiement était abandonné

Deux endroits, l'un après l'autre.

1. `EffectChecker.check_pay` (`src/game/effect/effect_checker.py`) appelait
   `player.SpendResource(...)` — qui dépense TOUT — puis se contentait de
   **constater** le manque :
   `return effect.context.paid_this_resources.IsMatchCost(need_cost)`.
   À cet instant l'interface est inclinée, la carte de main dépensée est
   défaussée (`DiscardResourcesArea`), et rien ne les rend.

2. `PlayerAction.ResolveEffect` (`src/game/player/action/player_action.py`)
   traitait ce refus par `Faces.DiscardAll([this], effect)` : la carte, sortie
   de la main vers la zone de traitement au début de la méthode, partait à la
   défausse.

## Le correctif

**Le paiement devient atomique.** `check_pay` transmet désormais `need_cost` à
`SpendResource`, qui, une fois tous les moyens choisis passés, compare le
réservoir au coût AVANT le point de non-retour (`AfterCardsBeSpendAsResource`
puis `DiscardResourcesArea`). S'il est court, il rend tout :

- toute carte qui a **changé de zone** pour payer retourne d'où elle vient
  (comparaison avec la zone relevée avant le paiement : ça couvre la carte de
  main en transit dans `area_resources`, y compris celle d'un joueur qui aide
  à payer ; c'est la **première** origine relevée qui fait foi, sinon une carte
  portant deux effets payeurs verrait `area_resources` enregistrée comme son
  « origine » et y resterait bloquée) ;
- les coûts des payeurs se défont, via un nouveau `CostFunc.Base.RollbackCost`.
  `CostFunc.Exhaust` le redéfinit : il redresse exactement les cartes inclinées.
  Le cas par défaut rend « rien à rendre » quand le coût n'a pas de `call_fn` ;
  tout autre coût rend `False` et **est journalisé** — on ne fait pas croire à
  un rendu complet.

Deux pièges relevés en relecture, tous les deux corrigés :

- **Les deux porteurs de coût.** Un moyen de paiement porte son `CostFunc` sur
  `DoGenerateResources` (payé par `Effect.ProcessSelfCost`) **ou** sur
  `CanGenerateResources` (payé par `generate_resource` lui-même, via
  `message.cost_check_effect.cost_func`). Ne regarder que le premier ne couvrait
  **qu'une carte du jeu sur 107** : `31001a` Sync Ratio, celle sur laquelle le
  correctif a été mis au point. `50044` Fury's Watch — la carte officielle
  donnée en preuve de généricité — porte son `Exhaust` sur l'autre : elle
  serait restée inclinée, sans même une ligne au journal. `SpendResource`
  balaie désormais l'**union** des deux, dédoublonnée par identité d'objet
  (`_CoutsDuPayeur`).
- **L'état partagé entre copies.** `CardsDB.FindAbilities` sert le même objet
  `Ability` à toutes les copies d'un `card_id` et à tous les joueurs :
  `return_exhausted_cards` est donc commune. Deux copies dans le même paiement
  abandonné, et la première resterait inclinée pour toujours. Le rendu ne relit
  plus cet état : `SpendResource` prend un **relevé** (`CostFunc.SnapshotCost`)
  juste après chaque payeur, et `PayCost` remet le compteur à zéro à chaque
  appel, même celui qui échoue.

**La carte revient d'où elle vient.** `ResolveEffect` la déplace vers
`effect.context.play_from_area` au lieu de la défausser. Même correction sur
le chemin jumeau `CardPlayer.Play` (`src/game/card/face/base/card_player.py`),
où l'échec du coût PROPRE de la carte la défaussait de la même façon.

Fichiers touchés :

| fichier | rôle |
| --- | --- |
| `src/game/player/action/player_action.py` | paiement atomique + retour de la carte |
| `src/game/ability/cost_func.py` | `RollbackCost`, redressement exact pour `Exhaust` |
| `src/game/effect/effect_checker.py` | transmet `need_cost` |
| `src/game/card/face/base/card_player.py` | chemin jumeau |
| `tools/test_capacites.py` | 3 témoins ajoutés, 3 attendus corrigés |

## Générique, ou propre à SP//dr ?

**Générique**, et la batterie l'a prouvé toute seule.

1. **Le mécanisme est moteur, pas carte.** Les deux endroits ci-dessus ne
   savent rien de SP//dr : ils traitent n'importe quelle capacité `is_play`
   dont la vérification échoue après paiement.

2. **Une carte officielle a exactement la même forme.** `50044` Fury's Watch
   (pack `aos/nick_fury`) : `CanGenerateResources` annonce
   `Resources("B") * min(2, jetons)` pendant que son `DoGenerateResources`
   porte `CostFunc.RemoveTokens("YourSuitFormUpgrade", (1, 2), 'threat')`. Le
   joueur peut retirer 1 jeton quand 2 ont été annoncés : même sous-livraison,
   même abandon.

3. **Trois témoins d'autres packs gravaient le défaut comme si c'était la
   règle**, et sont devenus rouges dès que le moteur a été réparé :
   - `sd011` Top Speed (pack `speed`) — attendu : `defausse: ["sd015"]`, avec
     ce commentaire : « une carte dont le coût ne peut pas être payé n'est PAS
     rendue à la main » ;
   - `ar010` Ire of Athena (pack `ares`) — « la carte est injouable (le harnais
     la défausse) » ;
   - `bl002` Gear Up (pack `blade`) — attendu : `taille_main: 0`,
     `defausse: ["bl002"]`.

   Trois packs sans aucun rapport avec SP//dr, trois cartes simplement trop
   chères pour la main du moment : le moteur les mangeait toutes. Les trois
   attendus ont été corrigés et annotés — ils décrivaient un défaut, pas une
   règle.

## Le harnais choisi

`tools/test_capacites.py`. C'est le seul harnais qui monte une **position
réelle** et fait **jouer une carte en payant son coût** (clés `jouer`,
`payer_avec`, `main_exclusive`) ; `tools/test_cards.py`, lui, ne fait que
construire les capacités de toutes les cartes — il ne joue rien et n'aurait
rien vu. Les trois témoins ajoutés :

| témoin | ce qu'il prouve |
| --- | --- |
| `31001a` Sync Ratio — paiement INCOMPLET | la carte revient en main, les deux interfaces restent prêtes |
| `31001a` Sync Ratio — paiement INCOMPLET en MIXTE | la carte de main dépensée comme ressource revient aussi |
| `31001a` Sync Ratio — paiement COMPLET | contre-cas : une interface s'incline et la carte est bien jouée |
| `50044` Fury's Watch — paiement INCOMPLET | le coût porté par `CanGenerateResources` est rendu lui aussi (106 cartes sur 107) |

Rouge constaté d'abord, à chaque fois :

- correctif moteur retiré (`git apply -R`), les deux premiers témoins échouent
  avec « 31002b est incliné alors qu'il devrait être prêt ; 31022 n'est pas en
  main » et « 31010 / 31004 ne sont pas en main » ;
- `_CoutsDuPayeur` ramené au seul `paying_effect`, le témoin Fury's Watch
  échoue avec « 50044 est incliné alors qu'il devrait être prêt » ;
- le témoin COMPLET reste vert dans tous les états : c'est son rôle, il
  interdit un correctif qui refuserait tous les paiements.

Le journal du témoin Fury's Watch montre les deux moitiés du résultat :
`paiement abandonné : RemoveTokens ... ne sait pas se défaire, son coût reste
payé`, puis `APRES 50042 | en main = True`.

## Ce que le rendu ne rend PAS

Le point de non-retour est plus tôt que la frontière du rendu, et il faut le
dire précisément — sinon la prochaine correction partira d'une fausse base.
Quand `SpendResource` constate le manque, **chaque `WhenPlayerPayingResources`
a déjà été envoyé**. Ce qui en découle n'est pas défait :

1. **L'`ex_operation` du payeur**, qui a agi pendant le paiement. `kb013`
   Kate's Quiver a posé son compteur de flèche, `iw001b` a redressé Sue, et
   une dizaine d'autres cartes sont dans ce cas (`33003`, `ho013`, `mf001b`,
   `50170`, `50179`, `45030a`, `gp008`, `il020`, `39064`…).
2. **La fenêtre `WhenCardBeSpendAsResource`**, ouverte à chaque ressource
   générée : 44 fichiers de `src/cards/` y réagissent.
3. **Les coûts non réversibles** : `CostFunc.RemoveTokens` (Fury's Watch),
   `CostFunc.Counter`, les `CostFunc.Custom` arbitraires. Ceux-là, au moins,
   sont **journalisés** (`paiement abandonné : ... ne sait pas se défaire`) ;
   les deux premiers points ne le sont pas.

Un rendu partiel vaut mieux qu'une perte sèche — le joueur récupère sa carte,
qui est le matériel rare, et son inclinaison. Mais ce n'est pas une annulation.

## Ce qui reste, en plus

- **L'écran ne prévient toujours pas.** Le plateau laisse choisir « 1
  interface » pour un coût de 2 sans rien dire ; le paiement est simplement
  refusé proprement au lieu de coûter deux cartes. Dire au joueur combien il
  lui manque reste à faire, côté client.

## Verdict de la batterie

`tools/test_capacites.py` EN ENTIER, `PARALLELES=8`, sur un dossier de jeu
jetable (`.game-src-yarro`, supprimé après la passe ; ni `.game` ni
`.game-src` n'ont été touchés) :

**2342 / 2349 cas passés.** Sept rouges, aucun imputable à ce correctif :

| cas | verdict |
| --- | --- |
| `sg009`, `sg013`, `sg007`, `sg006` (Squirrel Girl) | **antérieurs**. Rejoués un à un avec le correctif RETIRÉ : rouges, avec le même message. |
| `ma015` Break Through | **artefact de la passe parallèle** (« aucun résultat, processus mort »). Rejoué seul : vert, trois fois, avec et sans le correctif. |
| `ze014` The Mother of Night (×2) | **une autre session, en cours**. Rejoués avec le moteur du commit `71433704`, c'est-à-dire AVANT les deux commits de ce correctif : rouges à l'identique. La cause est le « sas de recherche » (`search_transit`) en train d'être posé dans `selector_end.py` / `effect_invoke.py` pour le signalement Aghenatak ; `ze014` appelle `Search.PlayerCard` **deux fois** de suite. Signalé à cette session. |

⚠ Deux réserves de méthode, à lire ensemble :

1. **La passe est parallèle.** Le harnais rappelle qu'une validation de
   portage exige de la comparer **cas par cas** à une passe séquentielle. Ce
   n'a pas été fait (≈ 1 h 20 en parallèle, plusieurs heures en séquentiel) ;
   les sept rouges, eux, ont bien été rejoués un à un en séquentiel.
2. **L'arbre est partagé et vivant.** Cette passe a tourné pendant qu'une
   autre session modifiait `selector_end.py`, `effect_invoke.py`,
   `effect_context.py` et ajoutait ses propres cas. Le nombre brut ne mesure
   donc pas ce correctif seul. Ce qui le mesure, lui, ce sont les quatre
   témoins : verts avec, rouges sans, chacun vérifié dans les deux états.

### L'historique des passes, sans arrondi

Il n'y a **jamais eu** de passe complète du moteur d'origine : la première
passe complète a tourné le correctif déjà posé.

| passe | état | verdict |
| --- | --- | --- |
| 1 | correctif posé, les 3 attendus périmés pas encore corrigés | 2336 / 2344 (8 rouges) |
| 2 | attendus corrigés + jumeau `CardPlayer.Play` | 2339 / 2344 (5 rouges) |
| 3 | ronde de relecture : union des deux porteurs de coût, relevé par paiement, témoin `50044` | 2342 / 2349 (7 rouges) |

Le passage de 2344 à 2349 tient à un témoin ajouté par moi (`50044`) et à
quatre ajoutés par l'autre session.
