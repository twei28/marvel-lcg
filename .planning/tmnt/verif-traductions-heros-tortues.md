# Vérification des traductions : lot heros_tortues (Leonardo, Donatello, Michelangelo, Raphael)

70 cartes relues une à une contre l'anglais (fichier `trad/heros_tortues.json`), 17 corrigées, 52 laissées telles quelles, 1 sans texte (td007 Inspired Brilliance, carte Ressource vierge, `fr` null normal).
Terminologie vérifiée contre `textes-fr-complets.ts` (officiel) : « pile de défausse » (20 occurrences contre 1 « dans votre défausse »), « vainc / vaincu » (281 occurrences, aucun « K.O. » dans l'officiel), « après le début de votre tour » (4 occurrences), « Exigence », « Restreint », « Perçant », « Déferlement », « À Distance », « dégâts consécutifs », « prévenez », « contre de base », « sonnez », « initie une attaque ».

## Corrections (tout dans `ui-app/src/board/textes-fr-fanmade.ts`)

Motif A : officiel = « pile de défausse » (et « pile de défausse Rencontre »), jamais « défausse » seul.
Motif B : officiel = « vaincre », pas « mettre K.O. ».
Motif C : officiel = « après le début de votre tour ».
Motif D : citations de capacité gagnée harmonisées en « … » comme tl008 et tl011 (le fichier emploie « » 308 fois ; les 5 cartes du lot avaient des guillemets droits).

| id | nom | AVANT | APRÈS | raison |
|---|---|---|---|---|
| tl001b | Leo | « cherchez dans votre deck et votre défausse » | « … votre deck et votre pile de défausse » | A |
| tl002 | Splinter | « dans votre défausse » | « dans votre pile de défausse » | A |
| tl008 | Iaijutsu | « Si cette attaque met K.O. un ennemi » | « Si cette attaque vainc un ennemi » | B |
| tl013 | Brainwashed Betrayal | « après que votre tour commence » | « après le début de votre tour » | C |
| tl014 | Foot Patrol | « le deck Rencontre et la défausse Rencontre » | « … et la pile de défausse Rencontre » | A |
| td001b | Donnie | « votre deck et votre défausse » | « votre deck et votre pile de défausse » | A |
| td008 | Donnie's Lab | « de votre défausse » | « de votre pile de défausse » | A |
| td014 | Extermination! | « et la défausse Rencontre » | « et la pile de défausse Rencontre » | A |
| tm001b | Mikey | « dans votre deck et votre défausse » | « … votre pile de défausse » | A |
| tm003 | Call for Help | « dans votre deck et votre défausse » | « … votre pile de défausse » | A |
| tm008 | Mikey's Couch | « dans votre défausse » | « dans votre pile de défausse » | A |
| tm011 | Michelangelo's Nunchuck | gagne : "<b>Réponse de héros</b> … round." | gagne : « <b>Réponse de héros</b> … round. » | D |
| tm012 | Michelangelo's Other Nunchuck | idem, guillemets droits | « … » | D |
| tr001b | Raph | « votre deck et votre défausse » | « … votre pile de défausse » | A |
| tr003 | Disarm | le texte "<b>Action de héros</b>" ou "<b>Réponse de héros</b>" | le texte « <b>Action de héros</b> » ou « <b>Réponse de héros</b> » | D |
| tr011 | Raphael's Sai | gagne : "<b>Action de héros</b> … ennemi." | « … » | D |
| tr012 | Raphael's Other Sai | « après que Raphael met K.O. un ennemi » + guillemets droits | « après que Raphael vainc un ennemi » + « … » | B + D |

## À trancher (laissés tels quels)

1. **Exigence** (tr003, tr004, tr005) : écrit `<b><i>Exigence</i></b> ([physical]).` L'officiel (27006, 28013…) l'écrit en texte brut `Exigence ([physical]).`, mais le fichier maison utilise `<b><i>Exigence</i></b>` sur 8 autres cartes (dd003, vv002, sf003, tc005…) ; ul009 et up042 sont en brut. Option 1 : tout en brut comme l'officiel. Option 2 : garder gras italique. À décider avec le scan sous les yeux ; aucun changement fait.
2. **Espaces insécables** : la consigne demande une espace insécable dans « » et avant « : ; ? ! ». Tout le fichier (1179 apostrophes droites, 308 paires « ») n'utilise que des espaces ordinaires, aucune insécable. Je n'ai pas introduit d'insécables sur 17 cartes seulement (incohérent avec le reste, risque de rupture de ligne mal gérée côté affichage). Question de fond pour toutes les cartes.
3. **Keywords en tête de phrase** : « Coup Rapide », « À Distance », « Perçant », « Déferlement » en majuscules, alignés sur l'officiel ; rien à changer, signalé pour mémoire.
4. **td005 Improvised Tactics** : le rappel « (vous ne pouvez pas choisir deux fois la même option) » est en italique dans le FR ; l'anglais du JSON n'a pas de balise. Italique probable sur le scan, non vérifié.
5. **tl015 Karai** : « Une fois révélée » (carte) et « Une fois vaincu » (sbire) : conforme à l'officiel pour un sbire, laissé.

## Coquilles de l'anglais relevées (non corrigées)

- **td001b Donnie** : « Donatello's Bo » alors que la carte td011 s'appelle « Donatello's Bō » (macron). Le FR recopie « Bo ».
- **tr014 Mutagen Bomb** : « Old Hobb » (deux b) alors que la carte tr015 s'appelle « Old Hob ». Le FR recopie « Old Hobb ».
- **tl001b / td012 / tm011** : rien d'autre. (« Brainwashed » et autres noms cohérents.)

## Traits

Contrôle rapide de `ui-app/src/board/traits-fr.ts` : les traits traduits du lot (AÉRIEN, ARMURE, CHAT, DÉFENSE, OBJET, LIEU, COMPÉTENCE, TACTIQUE, TECHNOLOGIE, ADOLESCENT, CONTRE, TITRE, ARME, VERS, ANDROÏDE, GÉNIE, ÉGOUTS, POSTURE, ESSAIM, TORTUE, JUSTICIER) sont corrects. Les autres (NINJA, KATANA, SAI, NUNCHUCK, BO, FOOT CLAN, MOUSERS, FLYBORGS, MUTANT, MUTANIMAL, SENSEI, RAT, NYC, SKYLINE, CONDITION, VEHICLE traduit) n'ont pas d'entrée ou restent en anglais : cohérent avec les noms propres laissés en anglais. Je n'ai pas relu la sortie complète du générateur. Aucun changement.

## Ce que je n'ai pas pu vérifier

- Aucun scan consulté : tout est fait contre le texte anglais du JSON (aucun doute sur le sens n'a nécessité le scan, hormis les points 1 et 4).
- Noms de compteurs cohérents avec `compteurs-fr.ts` : non ouvert (les textes disent « compteur de rage », « compteur de minuteur », « compteur d'essaim »).
- Tests : `npx vitest run src/board/traduction src/board/textes-fr-fanmade` : 30 passés, 1 échec attendu (`.js est à jour` : fichiers générés `Fusion/marvel-lcg-src/public/js/traduction/*` à régénérer par l'orchestrateur après fusion, non commités).
