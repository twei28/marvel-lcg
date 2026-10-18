# Vérification des traductions FR : lot shinobi_b (18/10/2026)

Lot : Ninjutsu `sa001-sa020`, Taijutsu `sh001-sh020`, Dual `sc001-sc012`, Paths `se001-se011` (63 cartes).
Fichier corrigé : `ui-app/src/board/textes-fr-fanmade.ts` uniquement. Branche `verif-trad-shinobi-b`.

Bilan : 63 cartes relues, 7 corrigées, 56 laissées telles quelles.

## Corrections

| id | nom | AVANT | APRÈS | raison |
|---|---|---|---|---|
| sa001 | Assassinate | « Cette attaque gagne perçant. » | « Cette attaque gagne Perçant. » | mot-clé en majuscule dans les cartes officielles FR |
| sa003 | Reconnaissance | « …du deck rencontre. » | « …du deck Rencontre. » | « deck Rencontre » partout ailleurs (officiel et sc008/sc009) |
| sh001 | Raising Block | « quand vous devriez subir des dégâts d'une attaque, prévenez 3… » | « quand vous êtes censé subir n'importe quelle quantité de dégâts d'une attaque, prévenez 3… » | « any amount of damage » omis ; tournure officielle (01003, 05005) et déjà utilisée par sa009 |
| sh009 | Toss | idem (prévenez 3 de ces dégâts et retirez 1 menace) | « …êtes censé subir n'importe quelle quantité de dégâts d'une attaque, prévenez 3… » | même omission |
| sh018 | Countercross | idem (prévenez 1 de ces dégâts) | « …êtes censé subir n'importe quelle quantité de dégâts d'une attaque, prévenez 1… » | même omission |
| sh010 | Martial Skill | « retirez-lui 1 compteur chi » | « retirez-en 1 compteur chi » | alignement sur « retirez-en » (sa007, sa008, sc002, sc004, tournure officielle) |
| sc007 | Mizuki | « choisissez :\n• camouflez un personnage ami ;\n• remettez dans votre main un événement… défausse. » | « choisissez :\n• Camouflez un personnage ami.\n• Remettez dans votre main un événement… défausse. » | puces de l'anglais (majuscule, point) et des officielles (« choisissez :\n• Retirez… ») ; sa019 et sh005 les suivaient déjà |

## À trancher (laissés tels quels)

- **sa012 Black Ops** : l'anglais imprimé dit « Hero Action: After your hero defeats… » ; l'utilisateur a tranché que la carte se comporte en Hero Response (Q-N2). Le FR suit l'imprimé (« Action de héros »), comme Æthreal Shift. Option : « Réponse de héros » si l'on veut que le FR suive la décision de comportement. Je n'ai pas tranché.
- **sc012 Hitodama** : l'imprimé est « Hero Response (attack) », le comportement retenu est Hero Action (Q-D2) ; FR « Réponse de héros » = imprimé. Même question.
- **sh011 Elbow Strike, sh016 Jō** : « damages an enemy » rendu par « blessé un ennemi » (aussi dans ul045). Les cartes officielles disent plutôt « infligé des dégâts à / blessé » selon le cas (« attaqué et blessé »). Je garde « blessé ».
- **Compteurs** : « compteurs chi », « compteurs bâton », « compteurs de fumée / d'ombre / de samouraï » : formes mixtes (apposition ou « de »). Le texte officiel dit « jetons X » mais TMNT utilise « compteurs » (compteurs-fr.ts). Non modifié.
- **Noms de capacités** (Shadow Stride, Insight, Way of the Warrior, Recenter, Meditate, Dark Visions, Light of Foot, Gardener, Bodyguard, Kanpeki) laissés en anglais comme tous les noms de capacité des cartes maison (ex. « Of Heven and Hel »). Option : les traduire.
- **se005** : le rappel « (2 cartes glissées maximum.) » est en italique alors que l'anglais « (Max 2 tucked cards.) » ne l'est pas ; identique à td012 (1 carte glissée maximum). Gardé.
- **Traits** : NYC, NINJA, NINJUTSU, TAIJUTSU, BUSHIDO, KUJI-KIRI, SENPAI restent en anglais dans `TRAITS_FR` (absents de la table, donc inchangés) ; les autres (OBJET, ARME, COMPÉTENCE, POSTURE, SERMENT, TORTUE, MOINE, ÉQUIPE, ÉGOUTS, RUES, LIEU, SORT, TITRE, ENTRAÎNEMENT, PRÉPARATION, PSIONIQUE, MYSTIQUE…) sont cohérents. Je n'ai pas vérifié si l'officiel traduit « NYC ».
- **Espaces insécables** : le fichier entier utilise des espaces ordinaires avant « : ; ? ! » et dans « » (0 espace insécable sur tout le fichier). Non modifié, car convention globale du fichier.
- **« jusqu'à »** : « infligez 1 dégât à jusqu'à 3 ennemis » (sc011) est lourd mais déjà utilisé ailleurs (ul…) ; gardé.

## Coquilles de l'anglais relevées (non corrigées)

- sh014 : « Just do what I do Casey. » (virgule manquante avant Casey).
- sh009 Toss et sh018 Countercross : pas de citation (normal, aucune imprimée).
- sa012 : Hero Action au lieu de Response (voir ci-dessus) ; sc012 : inverse.
- sh012 : citation sans signature (imprimé tel quel).

## Non vérifié

- Je n'ai pas rouvert les scans (le texte anglais de `trad/shinobi_b.json` a été pris pour fidèle), donc une coquille de transcription anglaise éventuelle n'est pas détectée.
- Pas de relecture des traductions de noms de cartes (hors périmètre).

## Contrôles

- `cd ui-app && npx vitest run src/board/traduction src/board/textes-fr-fanmade` : 31/31 après `node ui-app/outils/generer-traduction-public.mjs` (fichiers générés non commités). Balises `<b>`/`<i>`, nombres et retours à la ligne comparés automatiquement EN/FR : seule différence, le rappel en italique de se005 (voulu).
