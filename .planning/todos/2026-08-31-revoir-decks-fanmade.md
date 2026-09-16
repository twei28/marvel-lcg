# ✅ CLOS LE 12/09/2026 : les decks générés sont RETIRÉS, pas revus

**Décision utilisateur du 12/09/2026**, à la question « jusqu'où va la revue ? » :
« On vire tous les decks générés pour les fan-made ». Application de la consigne
du 06/09/2026 (PROCESSUS-HEROS étape 3) à tout l'existant : 33 decks de départ
vidés de leur moitié d'aspect (les 12 de ce TODO, plus les 16 arbitrés entre le
29/08 et le 05/09, plus 5 copies d'un deck officiel ou sans note : spider_man_rainy,
venom_rainy, thor_jane_foster, albert, gwenpool). Chaque fichier garde une
`metadata.deck_note`. Les 7 decks illégaux ci-dessous disparaissent avec eux,
sauf `jubilee` (officiel, Unlikely Duo ×2, laissé tel quel) et le paquet
« Commanding Leadership » de `data/decks_aspect.json` (Hawkeye ×2, liste publiée,
laissée telle quelle). Conservés : les decks d'auteur, `wolverine_x23` (deck
officiel de X-23, dont il est le re-skin) et les substitutions de Human Torch,
Mister Fantastic, The Thing et Invisible Woman (cartes d'auteur absentes du moteur,
remplacées une pour une dans une liste d'auteur).

---

# (Ancien texte) À FAIRE : revoir les decks de départ que Claude a construits

**Demandé par l'utilisateur le 31/08/2026.** À traiter **quand tous les
personnages fan-made auront été portés**, pas avant.

---

## Pourquoi

Quand l'auteur d'un pack fournit sa decklist, elle est recopiée telle quelle :
aucun jugement, aucun risque. C'est le cas de `venompool`, `lockjaw`,
`moon_knight`, `totally_awesome_hulk`.

Quand il n'en fournit pas, le deck a été **construit par Claude**, sur cette
méthode :

1. lire tout le kit et identifier ce qu'il récompense (son « moteur ») ;
2. proposer à l'utilisateur l'aspect qui nourrit ce moteur — la décision lui
   revient, elle est de conception, pas technique ;
3. filtrer `data/cards.json` par classe d'aspect et par texte, en privilégiant
   ce qui alimente le moteur ;
4. appliquer les contraintes dures (15 signature + 25, aucune carte signature
   d'un autre héros, aucun allié au nom du héros, bonne classe) ;
5. consigner le raisonnement dans `metadata.aspect_note`.

**Les limites, dites franchement :**

- **aucun deck n'a jamais été testé en jeu.** `autoplay.py` prouve qu'il ne
  plante pas, pas qu'il est bon : son pilote est une heuristique, et son taux
  de victoire ne veut rien dire (Deadpool officiel fait 0 % lui aussi) ;
- **aucune notion validée de courbe ni d'équilibrage** — un coût moyen se
  calcule, il ne dit pas si le deck se joue bien ;
- les choix viennent de la **lecture du texte** des cartes, pas de parties
  jouées ;
- **aucune règle écrite n'existe dans le projet** pour ce cas : la méthode
  ci-dessus est un usage, pas une norme.

C'est donc, dans chaque portage, la partie la plus susceptible d'être fausse.

---

## Les 12 decks à revoir

| Deck | Aspect retenu | Choisi par |
|---|---|---|
| `agent_anti_venom` | (à relire dans son `aspect_note`) | session antérieure |
| `angela` | Agressivité | utilisateur, 31/08/2026 |
| `brawn` | (à relire) | session antérieure |
| `howard_the_duck` | Justice | session antérieure |
| `iron_lad` | (à relire) | session antérieure |
| `kate_bishop` | (à relire) | session antérieure |
| `ms_america` | Justice | utilisateur, 30/08/2026 |
| `okoye` | (à relire) | session antérieure |
| `patriot` | Leadership | utilisateur, 30/08/2026 |
| `scarlet_spider` | (à relire) | session antérieure |
| `speed` | Agressivité | session antérieure |
| `wiccan` | Justice | session antérieure |

**Ne PAS revoir** : `venompool`, `lockjaw`, `moon_knight`,
`totally_awesome_hulk` — decklists d'auteur, recopiées.

À noter : `human_torch` et `mister_fantastic` avaient une decklist d'auteur,
mais 3 et 4 cartes n'existaient pas dans le moteur et ont été **remplacées**
(voir §9 du GUIDE). Ces substitutions-là méritent aussi un coup d'œil.

---

## Comment revoir, le jour venu

La seule mesure qui vaut est **une partie jouée à la main**. Aucun outil du
projet ne juge un deck. Piste concrète, deck par deck :

1. lancer une partie solo avec le deck tel quel ;
2. noter ce qui reste bloqué en main faute de ressources, et ce qui ne sert
   jamais ;
3. corriger, et mettre à jour `metadata.aspect_note` avec la raison du
   changement — le fichier doit rester la trace du POURQUOI, pas seulement du
   QUOI.

---

## MESURE FAITE LE 31/08/2026 : 7 decks de départ sont ILLÉGAUX

Constaté en vrai, dans le wizard : l'écran de préparation affiche déjà un
badge « ⚠ Hors règles » avec le détail au survol. Scan des limites
d'exemplaires (`desc.MaxPerDeck`, « Max N per deck » imprimé, et unicité `*`)
sur **tous** les decks du projet :

| Deck de départ | Infraction | Origine |
|---|---|---|
| `gwenpool` | Blackout ×2, Git Gud ×2, Rock Paper Scissors ×3, Tic-Tac-Toe ×3 — **max 1** chacune (uniques) | fan-made, session antérieure |
| `howard_the_duck` | The Power of Justice ×3 — max 2 | fan-made, session antérieure |
| `iron_lad` | The Power of Justice ×3 — max 2 | fan-made, session antérieure |
| `scarlet_spider` | The Power of Aggression ×3 — max 2 | fan-made, session antérieure |
| `speed` | Energy ×2 — max 1 | fan-made, session antérieure |
| `wiccan` | The Power of Justice ×3 — max 2 | fan-made, session antérieure |
| `jubilee` | Unlikely Duo ×2 — max 1 | **deck OFFICIEL du moteur** : ne pas y toucher sans vérifier la liste publiée par FFG |

Le deck officiel de Deadpool met bien ces cartes 'Pool en **1** exemplaire :
les ×2/×3 de `gwenpool` sont donc des erreurs, pas une convention de pack.

Deux autres endroits, hors périmètre de ce TODO mais notés au passage :
- **`Commanding Leadership`**, un des « paquets d'aspect conseillés » assemblés
  à la volée par le wizard : Hawkeye ×2 (max 1) ;
- `deck/custom/Wolverine_custom.json` (The Power of Determination ×3,
  Twice the Determination ×3) et quatre `prebuilt_*.json` : fichiers importés
  ou personnels, à laisser à leur propriétaire.

> ⚠ **Relevé le 16/09/2026 : ces 144 decks n'existent plus.** Ils ont été
> supprimés les 05/09 et 12/09/2026 sur décision de l'utilisateur, et
> `deck/custom/` n'en porte plus un seul. Le paragraphe ci-dessous ne vaut
> que comme historique. Le reste de la fiche, lui, tient toujours :
> « Commanding Leadership » est encore assemblé à la volée par
> `public/js/prepare/catalog.js`.

**Ce qui est SAIN :** les 144 decks d'aspect de
`deck/custom/<héros>_<aspect>.json` (commit `0b41fc5`) — zéro infraction, la
règle est vérifiée par leur validateur de construction.

Correction non faite : retirer un exemplaire en trop change l'équilibre d'un
deck, c'est exactement la revue que ce TODO décrit. À traiter deck par deck,
en remplaçant la carte retirée plutôt qu'en descendant à 24 cartes.
