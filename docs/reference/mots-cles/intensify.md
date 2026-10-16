# Intensify (mot-clé maison, ensemble TMNT Intense)

**Texte imprimé** : te201 « Intense Combatants » (zip `TMNT Standard-Expert (Status Card Standard-Expert) /
Optional Intense Version / X1 Intense Combatants.png`) : « **Forced Interrupt**: When a status card would be
placed on a character, if that character already has 1 copy of that status card on them, intensify them
instead. »

**Définition** (fournie par l'utilisateur le 16/10/2026, réponse Q2 de `.planning/tmnt/shredder-questions.md`) :
« intensify X » = donner une carte d'état **Intensified** à X (7e carte d'état, fiche `intensified.md`).

**Mécanisme moteur** : helper `Intensify(effect, face)` du pack `tmnt_standard_expert`
(`Faces.GiveStatus([face], "Intensified", effect)`, rend False si X n'a aucune carte d'état). te201 écoute la
fenêtre `Message.WhenStatusWouldCardPlaceOnAgain` (fabrique `AbilityFactory.WhenUnitWouldBeStatusAgain`),
envoyée par `CanStatus.GainStatus` AVANT les plafonds.

**Carte exemple** : `te201` Intense Combatants, `src/cards/pack/tmnt_standard_expert/tmnt_intense/te201.py`.

**Pièges connus** : le plafond « un seul Sonné / Désorienté / Hébété / Cloaked » et `tough_max` sont testés
APRÈS la fenêtre te201 : sans cet ordre, le doublon serait refusé en silence et te201 ne verrait jamais rien.
Une Intensified n'ouvre pas la fenêtre (sinon boucle).

**Variantes maison** : aucune.
