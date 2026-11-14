# Shadowland : la mini-campagne (livret FR, 23/10/2026)

Source : `livret-fr.md` (transcription du livret officiel français). Trois scénarios, dans l'ordre, victoire obligatoire à chacun ; une défaite se rejoue sans pénalité.

## Fichiers
| Quoi | Où |
|---|---|
| Mise en place par scénario, carnet sortant | `src/cards/pack/shadowland/campaign.py` (`CampaignSetup(niveau)`, `CollectShadowland`) |
| Branchement (face 1A du complot principal) | `shadows_in_the_night/sl001a.py` (niveau 1), `shadow_labyrinth/sl038a.py` (2), `heart_of_shadow/sl060a.py` (3) |
| Vilains Sombres Protégés retirés du tirage | `shadowland/__init__.py` (`VilainsTirables`, `VilainsRetiresDeLaCampagne`, `VilainsDeLIdentite`), appelé par sl001a et sl038a |
| Description (écran, panneau de récompenses) | `data/campagnes/shadowland.json` (`cle_extension` « 209. Shadowland ») |
| Pages du livret (planches simples découpées du PDF FR) | `public/stories/shadowland/` : ignoré par git, part avec le déploiement (comme les autres campagnes) |
| Cas de test | `tools/cas/campagne_shadowland.py` (filtre `[slcamp]`, 62 cas) |

## Le carnet
| Clé | Sens | Écrite par |
|---|---|---|
| `Dark Protege Removed` | liste `sl013a;sl014a` : Sombres Protégés retirés | collecteur, victoires 1 et 2 (+ Daredevil / Elektra si un héros porte ce nom) |
| `Player N Overpowering Scenario 1` / `2` | `1` si la Corruption Insidieuse du joueur est INSOUTENABLE (face `sl072b`, trait OVERPOWERING) à la victoire ; absente sinon, jamais `0` | collecteur, victoires 1 et 2 |
| `Player N Recorded Card 1` / `2` | numéro de la carte (soutien ou amélioration de coût 2 ou moins) inscrite par le joueur | **le joueur**, dans le panneau (champ `choix`, `deck: requis`) |
| `Player N Remaining hit points` | PV persistants de la campagne experte | panneau (`victoire_commune_expert`, détecteur `pv_restants`) |
| `Campaign Completed` | campagne gagnée | collecteur, victoire 3 |

## Mise en place (ce que fait `CampaignSetup`)
- **Scénarios 1 et 2** : chaque joueur reçoit une Corruption Insidieuse (face A, attachée à son identité) ; les cartes du set Black Flower (`sl073`-`sl078`, les mêmes que `data/encounter_sets/black_flower.json`) sont mélangées au deck de rencontre ; menaces supplémentaires sur le complot principal (**1** par joueur au scénario 1, **3** au scénario 2). Le scénario 3 a déjà Black Flower et sa Corruption dans son contenu imprimé.
- **Scénarios 2 et 3** : 1 jeton Corruption par scénario précédent où la Corruption était INSOUTENABLE ; puis, pour chaque carte inscrite que le joueur a dans son deck, il peut la mettre en jeu sous son contrôle contre 1 jeton (le scénario 2 lit la carte n°1, le scénario 3 les cartes n°1 et n°2).
- **Scénario 3** : les quatre sbires Sombres Protégés (`sl020`-`sl023`, Grande Prêtresse, Gorgone, Lady Bullseye, Tigre Blanc) : un par joueur au hasard, face cachée (`dealt_encounter_cards`), les autres dans le deck de rencontre.
- **Experte, scénarios 2 et 3** : PV restants du carnet, puis chaque joueur peut se soigner en s'attribuant une carte Rencontre face cachée.
- **Tirage du vilain** (scénarios 1 et 2) : un Sombre Protégé retiré, ou qui partage le nom d'un héros de la table, n'est jamais tiré **en campagne** ; hors campagne le tirage reste libre.

## Décisions que le livret ne tranche pas
- **Cartes inscrites** : le livret dit « choisir un soutien ou une amélioration de coût 2 ou moins » ; le moteur ne vérifie ni le coût ni le contrôle (le joueur saisit le numéro, comme les autres campagnes saisissent un choix) ; seul `deck: requis` garde la carte dans le deck.
- **Six Sombres Protégés retirés** : impossible avec trois scénarios, mais par sécurité le tirage retombe alors sur la liste complète.
- **« Aucune partie jouée par un humain »** : la campagne n'a pas été jouée de bout en bout dans le navigateur ; l'écran des campagnes lit la description comme pour les autres boîtes, sans code d'interface propre.
- **Écran du joueur pour la carte inscrite** : champ texte (numéro de carte). Un sélecteur de cartes dans le panneau serait un chantier d'interface générique, non fait.

## Preuves
`tools/cas/campagne_shadowland.py` : 62 cas, tous verts ; deux mutations montrent qu'ils sont de vrais témoins (sans `MiseEnPlaceDeCampagne` : 15 cas rouges ; sans exclusion des vilains retirés : 6 cas rouges sur 24). `tools/verifier_campagnes.py` : les 7 clés déclarées existent dans le moteur.
