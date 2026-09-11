# Des cartes de contre jouées ne retirent pas la menace (rapport joueur)

**Rapport de StupidInhuman, 11/09/2026 08:45** (formulaire du site, aucune
capture, aucun journal) : « Il y a plusieurs cas où je joue des cartes qui
retirent de la malignace mais ça ne marche pas. Je ne sais pas si c'est lié au
fait que parfois je undo ou pas mais c'est souvent vers la fin de la game. »
L'utilisateur a vu la même chose sur *Pour la Justice* (`01060`) dans une
partie Spider-Man Justice contre Risky Business (défaite, 5 rounds).

⚠ **08:45 est AVANT le premier déploiement du jour** (cinquième couleur,
vers 09:30) : le défaut préexiste, il n'est pas lié à l'éclair.

## La piste, tirée du harnais le même jour

En écrivant les cas du pack Zeus, Precognition (`ze004`, un contre) était
**jouée, ses ressources dépensées, puis défaussée sans effet**, avec pour
seule trace « `WhenPlayerInTurn failed` », sans motif. Cause dans ce cas-là :
les identifiants des EFFETS de paiement envoyés au moteur ne correspondaient
pas (le pilote du harnais en interdisait un par erreur), le moteur n'a pas
trouvé de quoi payer et a fait échouer l'effet en silence, carte perdue.

Un **undo** peut produire la même situation en vraie partie : le plateau
garde des identifiants de moyens de paiement qui ne sont plus ceux du moteur
après l'annulation, `FindPayEffect` (effect_target_cost.py:71) rend `None`,
et l'effet échoue sans un mot. « Souvent vers la fin de la game » colle : plus
de cartes en jeu, plus d'undo, plus d'identifiants recyclés.

## Ce qui a été fait le 11/09/2026

`game/player/action/player_action.py` : les deux lignes « `{effect} failed` »
du journal écrivent désormais le motif (`effect.failures`). Au prochain
déploiement, le journal serveur dira pourquoi.

## Par où continuer

1. Journal serveur : `journalctl -u narwhal --since "2026-09-11 08:00"
   --until "2026-09-11 09:00" | grep -i failed` (accès SSH depuis PowerShell,
   clé `deploiement/cle_narwhal`).
2. Reproduire sur le plateau : jouer un contre, faire un undo, rejouer un
   contre en payant avec des cartes déjà proposées avant l'undo. Regarder
   `refus_json` et le nouveau motif.
3. Si c'est bien l'undo : côté plateau, invalider la liste des moyens de
   paiement (`target_payment`) à chaque nouvelle demande du moteur, ne
   jamais réutiliser celle d'avant.

## ✅ RÉSOLU LE 11/09/2026 : ce n'est pas un défaut, c'est le mot-clé Crise

Journal moteur rapatrié du serveur (`.site/moteur-5.log`, partie Spider-Man
Justice contre Risky Business). Chaque fois que *Pour la Justice* (`01060`)
est jouée :

```
414: Spider-Man would play For Justice! with (RR)
415: For Justice! activates, targets [(48,02004b) Hostile Takeover]
416: Spider-Man va contrer Hostile Takeover (+3)
417: [(59,02009) Collapsing Bridge]'s Crisis activates
418: For Justice! were discarded
```

**Collapsing Bridge (`02009`) porte Crise** : tant qu'elle est en jeu, la
menace ne peut pas être retirée du complot principal. Le joueur cible le
complot principal, le moteur applique la règle, la carte part en défausse
sans effet. C'est conforme aux règles. La même séquence apparaît trois fois,
séparée par des « Game Restart » : le joueur a annulé et rejoué le même coup,
ce qui explique le « c'est lié à l'undo » du rapport (l'undo est la
conséquence, pas la cause).

**Ce qui manque, c'est une explication au joueur.** La carte est jouable, donc
le canal des refus ne dit rien ; et le plateau laisse choisir un complot dont
la menace est verrouillée. Pistes, à décider avec l'utilisateur :

1. Sur le plateau, un bandeau « Crise » sur le complot principal tant qu'une
   manigance à Crise est en jeu, et un mot dans l'aperçu au survol.
2. Exclure le complot principal des cibles d'un contre tant qu'une Crise est
   en jeu (la règle rend le choix inutile, pas illégal : c'est un choix de
   confort, à annoncer).

Au passage : les journaux moteur existent bien en prod (`.site/moteur-N.log`,
un par table, ÉCRASÉ à chaque lancement de la table). Le rapport de 08:45
correspondait à une table relancée depuis : son journal était perdu. Une
rotation (`moteur-N-<date>.log`) éviterait ça.
