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
