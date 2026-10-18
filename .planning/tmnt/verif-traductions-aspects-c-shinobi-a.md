# Vérification des traductions : lot aspects_c + shinobi_a (18/10/2026)

Lot : 72 cartes (`aspects_c.json` : 32 = Protection `up` 26 + Dual-Aspect `ud` 6 ; `shinobi_a.json` : 40 = Bushido `sb` 20 + Kuji-Kiri `sj` 20). Fichier corrigé :
`ui-app/src/board/textes-fr-fanmade.ts`. Branche `verif-trad-aspects-c-shinobi-a`.

Cartes relues : 72. Corrigées sur le fond : 10. Ponctuation (espaces insécables) : 70 cartes. Laissées telles quelles : 62 (pour le fond).

## Corrections de fond

| id | nom | AVANT | APRÈS | raison |
|---|---|---|---|---|
| sj009 | Armageddon | « après qu'Armageddon entre en jeu, distribuez à chaque joueur 1 carte de rencontre face cachée » | « après qu'Armageddon est entré en jeu, attribuez à chaque joueur 1 carte Rencontre face cachée » | l'officiel dit « attribuez … carte Rencontre face cachée » ; « après que » veut l'indicatif passé |
| sj009 | Armageddon | « chaque identité a +1 taille de main » | « chaque identité a +1 en taille de main » | tournure du reste du fichier (« gagne +1 en taille de main ») |
| sj006 | Enthrall | « Son CTR est égal à sa MNG imprimée » | « Sa CTR est égale à sa MNG imprimée » | CTR est féminin (« la CTR » partout) |
| sj012 | A Thin Place | « retirez-en 3 compteurs mystiques » | « retirez-lui 3 compteurs mystiques » | « en » fait double emploi avec le complément ; reste cohérent avec « retirez-lui » des autres cartes |
| sj013 | Kirby's Pencil | « sans payer son coût en ressources » | « en ignorant son coût en ressources » | anglais « ignoring » ; l'officiel (27023 et similaires) dit « en ignorant son coût en ressources » |
| sj013 | Kirby's Pencil | « autant de cartes que le coût en ressources imprimé de cette carte » | « … imprimé de la carte jouée » | « cette carte » pouvait désigner le Crayon lui-même ; l'anglais « that card » vise la carte jouée |
| sj013 | Kirby's Pencil | « deck de rencontre » | « deck Rencontre » | forme officielle |
| sj017 | Yi | « après que Yi utilise un pouvoir de base » | « après que Yi a utilisé un pouvoir de base » | « After … uses » rendu comme les autres Réponses (sb017 Uno) |
| sj001 / sj010 / sj011 | Foresight / Flash Ward / Unravel | « deck de rencontre » | « deck Rencontre » | forme officielle (409 occurrences contre 0 de « deck de rencontre ») |
| sj010 | Flash Ward | « dans la zone de boost de chacune des cartes défaussées » | « dans le champ de boost de chacune … » | l'officiel dit « champ de boost » |
| sj007 | Ring of Protection | « dans la zone de boost de la carte défaussée » | « dans le champ de boost de la carte défaussée » | idem |
| sb015 | Oathbreaker | « une carte rencontre … le deck rencontre … cette carte rencontre » | « une carte Rencontre … le deck Rencontre … cette carte Rencontre » | forme officielle (majuscule) |

## Ponctuation

Espaces avant `:` `;` `?` `!` et `»`, et après `«`, remplacés par des espaces insécables (U+00A0) sur les 72 cartes (70 lignes modifiées),
comme le fait `textes-fr-complets.ts` (1254 occurrences) ; `textes-fr-fanmade.ts` n'en avait aucune. Le « → » n'est pas touché.
Aucune autre ponctuation fautive (apostrophes, doubles espaces) trouvée dans le lot.

## À trancher (laissés tels quels)

1. **up024 Nobody** : la citation reste en anglais (« Can they swing from a thread? Take a look overhead. Hey there, there goes Nobody. »,
   parodie du générique de Spider-Man). Options : (a) laisser en VO ; (b) « Peut-il se balancer à un fil ? Levez les yeux. Tiens, voilà
   Personne qui passe. ». De plus l'anglais dit « them » (Angel Bridge) : le français écrit « lui ».
2. **up030 Redirection Mastery** : EN « After you exactly defend an attack », FR « avez « exactement » défendu une attaque ». Sens retenu par
   l'utilisateur : défense exacte (ATQ de l'attaque = DEF). Les guillemets sont un calque ; une reformulation (« avez défendu une attaque
   dont l'ATQ était exactement égale à votre DEF ») est possible mais interprétative.
3. **« K.O. » ou « vaincu »** pour un ennemi défait : sb006 Mercy (« devrait être mis K.O. ») et sb010 Tsujigiri (« met cet ennemi K.O. »)
   emploient « K.O. » alors que l'officiel dit « vaincu / vainquez » (0 « K.O. » dans `textes-fr-complets.ts`). Le fichier fanmade mélange
   les deux (≈ 30 « K.O. » contre ≈ 15 « vainquez »), et d'autres cartes TMNT (Raphael tr012…) disent « met K.O. » : choix à faire pour tout
   le fichier, pas pour ce lot seul.
4. **Jeton / compteur** : l'officiel dit « jetons » ; le lot mélange « jetons » (Brute, Guérison, Carburant, Réverbération), « compteurs ampli »
   (ud003), « compteurs mystiques » (sj012) et « compteurs de samouraï » (fiche `samurai-counter.md`, laissé). Une harmonisation vers
   « jetons » toucherait aussi le samouraï.
5. **Balises de traits `[[…]]`** : mélange de formes anglaises (`[[WEAPON]]`, `[[OATH]]`, `[[SPELL]]`, `[[TRAINING]]`) et françaises
   (`[[ENTRAÎNEMENT]]`, `[[ÉLITE]]`) dans le fichier. Sans effet à l'affichage (`traduction-posee.ts` traduit via `TRAITS_FR`), donc laissé.
6. **sj007 Ring of Protection** : « Défaussez des cartes du dessus de votre deck pour chaque icône » : le nombre par icône n'est pas dit
   en anglais ; lu comme 1 carte par icône, laissé tel quel.
7. **Citations traduites avec liberté** (jeux de mots) : up001 « coin-coin », sj017 « Choquant ! » (Shocking), sj016 « nous échappe des
   mains » : jugés acceptables, non modifiés.
8. Style « (3 au maximum) » (ud002) contre « (2 max) » (up016) : variation d'écriture sans erreur, laissée.

## Coquilles de l'anglais relevées (non corrigées)

- up034 Seymour Gutz : « Seymor Gutz » dans le texte (le nom de la carte est Seymour).
- up043 Wonder Turtle : citation « Suprise. ».
- up027 Protection Training : « gets a +3 hit points ».
- ud004 Stealth Fighter : « **Interrupt**: After … is defeated » (une Interruption s'écrit « When » ; FR reproduit « après que »).
- sb016 Wakizashi « dashido », sj015 « wierdest », sj006 « textbox » (déjà notées dans `shinobi-reponses.md`).

## Traits FR

Contrôle des traits des 72 cartes contre `traits-fr.ts` : tous présents ou volontairement laissés en anglais (DIMENSION X, MUTANIMAL, NINJA,
NOVA POSSE, NYC, RONIN). Aucune erreur trouvée. Non vérifié : l'exactitude du mot officiel de PERSONA (« INDIVIDU ») et de CONDITION
(« CONDITION »), repris de la table sans source indépendante.

## Limites

- Les scans n'ont pas été rouverts : l'anglais est celui du JSON ; aucune incohérence ne m'a poussé à vérifier un scan.
- Tests : `src/board/traduction*`, `textes-fr-fanmade`, `noms-cartes-fr` passent (après régénération du public, dont les fichiers générés
  ne sont pas commités).
- Les noms de cartes (`noms-cartes-fr.ts`) n'ont pas été relus.
