# Mode campagne — modifications du moteur et des fichiers partages

Rien dans `Fusion/marvel-lcg-src/src/game/**` n'a ete touche. Tout le mode campagne vit dans le pack
(`src/cards/pack/skrull_menace/campaign.py`), dans une donnee (`data/campagnes/skrull_menace.json`) et dans
des outils de test.

## Fichiers du pack (hors `src/game`)

| Fichier | Quoi | Pourquoi | Cas qui le prouve |
|---|---|---|---|
| `src/cards/pack/skrull_menace/campaign.py` (nouveau) | `CampaignSetup(1..5)` : mise en place, regle de cooperation, releve du carnet ; tableau « Cooperation Progress » et son assignation | modele `gmw/campaign.py` | les 32 chaines `[campagne_mode]` |
| `skrull_empire/sk082a.py`, `super_skrull/sk120a.py`, `paibok/sk144a.py`, `secret_invasion/sk192a.py` | une ligne `*CampaignSetup(n)` en tete de `GetAbilities()` + l'import | les capacites de campagne (type `Campaign`, hors jeu) doivent etre portees par la manigance principale 1A du scenario, comme `gmw/.../16061a` | `zone de cooperation — scenario 2`, `Elites — scenario 3`, `CAMPAGNE ENTIERE` (retirer la ligne de sk120a fait rougir le cas : preuve par mutation) |
| `skrull_pantheon/sk173a.py` (nouveau) | le module de la face A de « Protect the Pantheon », qui n'existait pas (la face A n'a aucune capacite imprimee) ; il ne contient que `*CampaignSetup(4)` | meme raison | `Shaper « Cube Removed » (scenario 4)`, `Elites — scenario 4`, `CAMPAGNE ENTIERE` |
| `shaper_of_worlds/sk229.py` | `mise_de_cote` (WhenGameWouldBegin) ne fait plus rien en mode campagne (`Worlds.IsCampaign`) | en campagne, le carnet DIT ou est chaque carte du set (en jeu, de cote, remelangee) et `campaign.py` les place une a une ; remettre tout le set de cote a la fin de la mise en place defairait un Shaper « In another game area » | `Shaper « In another game area »` ; les 4 cas `[modulaires] sk229` restent verts (hors campagne le comportement est inchange) |

Hors campagne, rien ne change : chaque capacite de `CampaignSetup` est gardee par `Worlds.IsCampaign`
(`AbilityFactoryCampaign.WhenCampaignSetup`, `Worlds.IsCampaign` dans les conditions des deux regles de
cooperation, et `WriteCampaignLogAtGameOver`). Les 117 cas `[modulaires]`, 67 `[sk-e]`, 73 `[super_skrull]`, 113 `[paibok]`,
98 `[pantheon]` et 225 `[secret_invasion]` sont verts apres les modifications des cinq 1A et de sk229.

## Outils et donnees

| Fichier | Quoi |
|---|---|
| `data/campagnes/skrull_menace.json` (nouveau) | la definition de la campagne ; ses cles sont verifiees par `tools/verifier_campagnes.py` |
| `tools/test_campagne_chaine.py` (nouveau) | harnais de chaines : N parties a la suite, carnet reporte comme le fait le panneau de recompenses (cles declarees seulement) |
| `tools/cas/campagne_mode.py` (nouveau) | les chaines (`CHAINES`) ; `CAS = []` : aucun cas pour `test_capacites.py` |
| `tools/autoplay.py` (partage, ADDITIF) | deux variables d'environnement, `AUTOPLAY_REGLES` (ex. `mode_campaign`) et `AUTOPLAY_CARNET` (JSON du carnet entrant), passees a `SceneLoader.NewFromJson` ; absentes : comportement identique (regles et carnet vides) |
| `ui-check/tests/campagne-skrull-menace.spec.ts` (nouveau) | la boite dans l'interface (creation, ecran de campagne, livret) et un scenario joue en vrai jusqu'au panneau de recompenses |
| scans `public/stories/skrull_menace/*.jpg` | NON versionnes (regle des images) : ecrits dans le depot principal, `/home/oem/Desktop/Marvel LCG/Fusion/marvel-lcg-src/public/stories/skrull_menace/` (15 pages du livret rendues a 975 px) |

## Pieges payes (a ne pas repayer)

- **Un joueur elimine sort de `world.players` ET de `const_players`** ; seul `const_seat_order_players` garde tous les sieges.
  Le releve boucle donc sur `world.const_seat_order_players`.
- **`Puzzle.Damage('<id>', n, source)` frappe la PREMIERE copie trouvee** (souvent celle qui dort dans le deck, quand le scenario en
  contient plusieurs) : viser `Puzzle.Damage(Puzzle.FindFaceInPlay('<id>'), ...)`. Le cas « sbire vaincu » etait vert pour la
  mauvaise raison avant ce correctif de la mesure.
- **Une cle absente du releve laisse l'ANCIENNE valeur au carnet** (le panneau ne distingue pas « effacee » de « jamais ecrite ») :
  les cles que le releve peut vider (`Eliminated Players`, `Cooperation Progress`, `Cooperation Area`) sont ecrites en chaine VIDE, jamais
  `None`.
- **Les noms d'options rendus par `/get_ask` ont des `_` a la place des espaces** (`Cloning_Faux_Pas`) : le harnais les normalise.
- **Le scratchpad de l'agent est PARTAGE avec les autres agents** (un `q3.py` d'un autre a ecrase le mien) : prefixer ses scripts.
- **Les ports** : le harnais de chaines prend `port_base + index de chaine` ; rester dans 31000-31999 (une chaine = un port).
