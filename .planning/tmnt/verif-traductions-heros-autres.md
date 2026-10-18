# Vérification des traductions : lot `heros_autres` (Venus, Casey Jones, Alopex, Jennika)

70 cartes relues (tv, tc, ta, tj, avec traits FR), 7 cartes corrigées (8 corrections), 63 laissées telles quelles (dont tv008 Evanescence, sans texte). Fichier modifié : `ui-app/src/board/textes-fr-fanmade.ts`.

## Corrections

| id | nom | AVANT | APRÈS | raison |
|---|---|---|---|---|
| tv007 | Resistance | « quand vous devriez subir des dégâts d'une attaque » | « quand vous êtes censé subir n'importe quelle quantité de dégâts d'une attaque » | « any amount of damage » omis ; formule de l'officiel (01003). |
| tv009 | Arcane Emitting Diode | « les 2 premières cartes de votre deck » | « les 2 cartes du dessus de votre deck » | « top 2 cards » : formule officielle, alignée sur tv010 et tv012. |
| tv014 | Turtle Shell | « les 2 premières cartes de votre deck » | « les 2 cartes du dessus de votre deck » | idem. |
| tc001a | Casey Jones (héros) | « le mot-clé restreint » | « le mot-clé Restreint » | nom de mot-clé : majuscule, comme l'officiel. |
| tc012 | Persuader | « Cette attaque gagne perçant. » | « Cette attaque gagne Perçant. » | officiel « gagne Perçant » ; cohérence avec tj010. |
| tj010 | Jennika's Other Tekko-Kagi | « quand vous faites une attaque de base » | « quand vous effectuez une attaque de base » | officiel « effectuez une attaque de base » ; cohérence avec tc012. |
| ta015 | Curse of Nine Tales | « choisissez l'un ou l'autre » | « choisissez une option » | « Choose one » : formule officielle. |
| ta015 | Curse of Nine Tales | « sur le complot principal » | « sur la manigance principale » | terme officiel (« main scheme »), 68 occurrences contre 1 ailleurs. |

## À trancher (laissé tel quel)

- tc005 Grand Slam : « Requirement » rendu `<b><i>Exigence</i></b>` alors que l'anglais n'a aucune balise sur ce mot. À confirmer sur le scan (gras italique ou non) ; je n'ai pas pu le voir.
- tc001b : « After you change to this form » rendu « après que vous avez changé pour cette forme ». Correct mais calqué ; l'officiel dit « après avoir changé de forme ». Alternative : « après être passé sous cette forme ». Sens laissé tel quel.
- Traits restés non traduits dans la table (identiques à l'anglais) : SKYLINE (tj007), SENPAI (tj011), PHANTOMS (tj014/tj015), KAMA, TEKKO-KAGI, NYC, PURPLE DRAGONS. Probablement voulu (noms propres ou termes japonais) ; SKYLINE pourrait devenir « HORIZON URBAIN », PHANTOMS « FANTÔMES ». Non tranché.
- Mots-clés de style : « (Limite d'une fois par phase.) » est en italique côté FR alors que l'anglais de tc001a n'a pas de balise (rendu officiel habituel, laissé).

## Coquilles de l'anglais (non corrigées)

- tj010 : « gains:"<b>Hero Interrupt</b> » : espace manquant avant le guillemet.
- tc006 / tc013 : « tucked under Casey's Bag » : aucune faute, rien à signaler.
- ta011 Prey : « Alopex' » (au lieu de « Alopex's »), alors que ta014 écrit « Alopex's » : incohérence anglaise.

## Non vérifié

- Aucun scan n'a été ouvert : relecture faite sur le texte anglais fourni par le lot.
- `npx vitest` impossible dans ce worktree (vitest et jsdom absents de `node_modules`) ; seul un contrôle de syntaxe du fichier TS a été fait (il se charge, tv007 lu correctement). `generer-traduction-public.mjs` non lancé ; fichiers générés non commités.
