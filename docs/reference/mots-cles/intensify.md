# Intensify (mot-cle maison NON DEFINI, ensemble TMNT Intense)

**Texte imprime** : te201 « Intense Combatants » (zip `TMNT Standard-Expert (Status Card Standard-Expert) /
Optional Intense Version / X1 Intense Combatants.png`) : « **Forced Interrupt**: When a status card would be
placed on a character, if that character already has 1 copy of that status card on them, intensify them
instead. »

**Definition** : AUCUNE. Ni la carte, ni les encarts des vilains Shredder, Baxter Stockman, Bebop & Rocksteady ne
definissent « intensify ». La carte est creee dans `cards.json` (pack `tmnt_standard_expert`) sans script.

**Mecanisme moteur** : aucun. Piste a trancher avec l'utilisateur (question Q2 de
`.planning/tmnt/shredder-questions.md`) : « intensifier » une carte d'etat pourrait vouloir dire en poser un
doublon au-dela du plafond, ou doubler son effet.

**Carte exemple** : `te201` Intense Combatants (non scriptee).

**Pieges connus** : le plafond « une carte Cloaked par personnage » (`CanStatus.cloaked_max`) interagit avec
cette regle : le plafond est teste dans `CanStatus.GainStatus` AVANT l'envoi de `WhenStatusWouldCardPlaceOn`
(meme ordre que le plafond de Tough) ; si l'utilisateur definit « intensify », l'ordre est a revoir.

**Variantes maison** : aucune.
