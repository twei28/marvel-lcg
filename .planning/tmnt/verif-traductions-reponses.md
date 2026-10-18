# Vérification des traductions TMNT : réponses de l'utilisateur appliquées (18/10/2026)

Branche `verif-trad-reponses`. Fichiers touchés : `ui-app/src/board/textes-fr-fanmade.ts` et `Fusion/marvel-lcg-src/data/cards.json` (champ `text` de ul025, ul031, ul041 seulement ; checksum recalculé : `6e0cce29…4d2d`, écriture `indent=1, ensure_ascii=False`). `compteurs-fr.ts` inchangé. Les fichiers générés `public/js/traduction/*` ne sont pas commités.

## 1. Shōgun, Mushroom, Time
- ul025 : « après que Shugun est entré en jeu » devient « après que Shōgun est entré en jeu » (FR et anglais `text`).
- ul041 : « Musroom ne compte pas… » devient « Mushroom ne compte pas… » (FR et anglais).
- ul031 : anglais `"TIme to get back at it."` devient `"Time to get back at it."` (le FR était déjà « Il est temps de s'y remettre. »).
- Aucun script ne dépend de ces textes : grep sur `src/`, `tools/`, `public/js` ne trouve « Shugun/Musroom » que dans des commentaires de ul025.py et ul041.py (non modifiés). Le `name` des cartes n'est pas touché.

## 2. Noms de capacités : table anglais vers français (appliquée partout)
Chaque nom n'apparaît que sur une carte (18 occurrences dans les cartes TMNT). « Foul Play » (The Hood) n'est pas une carte TMNT : hors périmètre. Déjà traduits avant : Double Trouble (tk006a, voir point 6) et Replicate (tx004b, « Réplication »).

| Anglais | Français | Carte |
|---|---|---|
| Shadow Stride | Pas de l'Ombre | se001 |
| Insight | Intuition | se002 |
| Way of the Warrior | Voie du Guerrier | se003 |
| Recenter | Recentrage | se004 |
| Kanpeki | Perfection | se005 |
| Magnificence | Magnificence | se006 |
| Meditate | Méditation | se007 |
| Dark Visions | Visions Sombres | se008 |
| Light of Foot | Pied Léger | se009 |
| Gardener | Jardinier | se010 |
| Bodyguard | Garde du Corps | se011 |
| Kenjutsu | Art du Sabre | tl001a |
| Kashikoi | Futé | td001a |
| Yaban Hito | Homme Sauvage | tr001a |
| Matagi | Chasseur Traditionnel | ta001a |
| Ninja Senpai | Ninja Aîné | tj001a |
| Overswing | Frappe Excessive | tc001a |
| Booyakasha | LAISSÉ tel quel (à trancher) | tm001a |

Booyakasha est une interjection de Michelangelo (comme « Cowabunga »), pas un nom descriptif : je ne l'ai pas traduit. Si tu veux quand même une traduction, dis laquelle. Les mots japonais (Kenjutsu, Kashikoi, Yaban Hito, Matagi, Kanpeki, Senpai) ont été traduits comme demandé (sens : art du sabre, malin, homme sauvage, chasseur traditionnel, parfait, aîné). Style : majuscules à chaque mot, comme les noms de capacités officiels (« Contrôle des Phases », « Beau Parleur », « Arme de Choix »).
Avant/après : se001 `<i>Shadow Stride</i> —` devient `<i>Pas de l'Ombre</i> —` ; tl001a `<i>Kenjutsu</i> —` devient `<i>Art du Sabre</i> —` ; se011 `<i>Bodyguard</i> —` devient `<i>Garde du Corps</i> —`.

## 3. Wingnut (uj038)
`dépensez les ressources suivantes [energy][energy]` devient `dépensez [energy][energy]`.

## 4. Casey Jones (tc001b)
`après que vous avez changé pour cette forme` devient `après avoir changé de forme`.

## 5. Bebop et Rocksteady (tk009, tk010, tk011, tk012)
`après que Bebop passe sur sa face [[K.O.]]` devient `après que Bebop est retourné sur sa face [[K.O.]]` (tk009, tk011) ; idem `après que Rocksteady est retourné sur sa face [[K.O.]]` (tk010, tk012).

## 6. tk006a
`<i>Double Peine</i>` devient `<i>Double Galère</i>`.

## 7. te201
`(Environnement optionnel pour ceux qui veulent plus de rebondissements.)` devient `(Environnement optionnel pour ceux qui veulent encore plus de grabuge.)`.

## 8. Parenthèses en italique : vérifié au scan
Méthode : comparaison du FR avec `cards.json` (parenthèses hors mots-clés attaque/contre/défense), puis relecture des scans pour chaque famille. Constat : `cards.json` met parfois en italique ce que le scan imprime en brut (td012, Limites des héros). Le scan fait foi pour le FR ; l'anglais de `cards.json` n'est pas modifié.
Italique RETIRÉ (parenthèse brute sur le scan), 12 cartes :
- td005 `(vous ne pouvez pas choisir deux fois la même option)`
- td012 `(1 carte glissée maximum.)`
- se005 `(2 cartes glissées maximum.)`
- tc001a `(Limite d'une fois par phase.)`
- tl001a, td001a, tv001a, tv001b `(Limite d'une fois par round.)`, tj001a `(Limite d'une fois par round pour chaque Shinobi.)`
- tm006 `(jusqu'à un maximum de 3)`, tm009 `(seul le joueur Michelangelo peut déclencher cette capacité)`
- uj022 `(y compris celle-ci)` (scan Move in Shadows : brut)

Scans vérifiés italiques, donc LAISSÉS en italique : Rampage (ua002, ua015…), « Coût additionnel… », « En payant cette carte… » / « Lorsque vous payez… », Mélangez., (attaque)/(contre)/(défense), tl008 et uj020 « (en payant son coût) », tj003 « (Cette carte est à la fois… ) », tx004a « (High Speed et Security Protocol) », tk013/tk020, ul034 (ATQ), tm001a (CTR, ATQ ou DEF), ub027.
Sens inverse (parenthèse brute en FR mais italique au scan) : aucun cas trouvé parmi les cartes vues.
Non vérifié : je n'ai pas rouvert les ~500 scans ; seules les familles de parenthèses ci-dessus (au moins une carte par famille, tous les cas isolés) ont été regardées. Les parenthèses de sous-titre « (Sbire némésis de X.) » n'ont pas été examinées.

## 9. Laissé tel quel
Citation de Nobody (up024), Redirection Mastery (up030), « attribuez » sur Mutanimal Van, noms de jetons du plateau (`compteurs-fr.ts`), traits.

## Preuves
`node outils/generer-traduction-public.mjs` ; vitest (traduction, textes-fr-fanmade, noms-cartes-fr, vocabulaire, compteurs, tmnt) : 28 fichiers, 365 tests OK ; `verifier_traductions_fr.py` OK ; `verifier_prefixes.py` OK ; cas de test moteur : voir résumé de la réponse.
