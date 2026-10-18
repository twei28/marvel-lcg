# Vérification des traductions TMNT : suite (18/10/2026)

Branche `verif-trad-suite`. Seul fichier de code touché : `ui-app/src/board/textes-fr-fanmade.ts` (cartes TMNT uniquement). `compteurs-fr.ts` n'a PAS été modifié (voir point 3). Tests : traduction, textes-fr-fanmade, noms-cartes-fr, vocabulaire, compteurs, tmnt (28 fichiers, 365 tests) et `verifier_traductions_fr.py` passent.

## 1. Les 8 cartes sans français : faites (8 cartes)

te021 Advance, te023 Assault, te025 Caught Off Guard, te026 Gang-Up, te027 Shadow of the Past, te121 Exhaustion, te122 Masterplan, te123 Under Fire. Anglais comparé à `cards.json` (identique à l'officielle 01186 à 01193, `ability_link`) ; scans non rouverts (texte strictement identique à l'officiel).
- te021 : `<b>Une fois révélée</b> : le méchant manigance.` + `« Le monde sera à moi. » —Krang`
- te025 : formulation de te001 (« Si aucune carte n'a été défaussée ainsi ») au lieu de la faute officielle « n'est défaussée par cette effet ».
- te027 : copie du te005 déjà corrigé (« Mélangez le reste de votre set de rencontre Némésis… »), l'officielle 01190 disant « les cartes restantes ».
- Citations (ma traduction, à valider) : « Je me vengerai ! » (Shredder), « Pourquoi tant de colère, petite tortue ? » (Bebop), « Nous devons tous jouer notre rôle. » (Rat King), « On les tient maintenant ! Impossible de s'échapper ! » (Granitor). J'ai évité deux calques de la proposition du rapport « mechants » (« Pourquoi si en colère », « Ils ne peuvent pas s'échapper »).

## 2. Espaces insécables : 419 cartes sur 507 (plus les 8 nouvelles)

U+00A0 ajoutée avant « : ; ? ! » et à l'intérieur de « » (« ␣ et ␣ » deviennent « U+00A0 et U+00A0 »), sur toutes les cartes TMNT. Plus aucune espace simple avant ces signes dans les cartes TMNT. Les cartes non TMNT n'ont pas été touchées. Avant/après : `<b>Réponse forcée</b> : après` -> `<b>Réponse forcée</b> : après` (tk001a, ts010, td016…) ; `<i>« Je me vengerai ! »</i>` -> `« Je me vengerai ! »`.

## 3. Jeton ou compteur : 54 cartes

Convention officielle relevée dans `textes-fr-complets.ts` : « jeton(s) Nom » avec majuscule (« jeton Charge », « jetons Munition », « Utilisations (3 jetons Taille) »), « jeton générique » pour *all-purpose counter*, « compteur de points de vie » (seul emploi de « compteur », conservé : il n'est pas dans les cartes TMNT).
- tr001a Raphael : « 1 compteur de rage » -> « 1 jeton Rage ».
- sb001 : « Utilisations (3 compteurs de samouraï) » -> « Utilisations (3 jetons Samouraï) » (aussi sb002 à sb020, sc002/4/5, se003, tj006).
- tx006 : « 2 compteurs polyvalents » -> « 2 jetons génériques » (aussi tx004b).
Autres mots traités : dragage (tv), chasseur (ta008), minuteur (tr014), essaim (td016/17, tx007/12), mutagène, câble, bouclier (tx), pistolet, munitions->Munition, dague (ua), ampli (ud003), chi, bâton (sh), ombre, fumée (sa), mystique (sj012). Aucun « compteur » ne reste dans les cartes TMNT.
Laissé : `compteurs-fr.ts` inchangé. Ses libellés sont de simples noms (« acier », « essaim », « rage »…) affichés sur le plateau sans le mot « compteur » ni « jeton », en minuscules comme pour les officiels (« acier ») ; les tests (`compteurs-fr`, plateaux TMNT) les figent. Seule entrée contenant le mot : la clé générique `counter: 'compteur'` (non utilisée par les cartes TMNT), laissée. À toi de dire si tu veux « Rage » en majuscule sur le plateau, ou `counter` -> « générique ».
Laissé aussi : ub041 « jeton de dégât » (déjà « jeton »).

## 4. K.O. / vaincu : 2 cartes

- sb006 Mercy : « quand un ennemi devrait être mis K.O. par votre héros » -> « quand un ennemi est censé être vaincu par votre héros » (anglais : *would be defeated*).
- sb010 Tsujigiri : « Si cette attaque met cet ennemi K.O. » -> « Si cette attaque vainc cet ennemi ».
Gardé : `[[K.O.]]` (nom de la face de Bebop et Rocksteady) sur tk007b, tk008b, tk009 à tk012.

## 5. « Exigence » en texte brut : 4 cartes

tr003, tr004, tr005, tc005 : `<b><i>Exigence</i></b> ([physical])` -> `Exigence ([physical])`. Vérifié : l'anglais de `cards.json` est « Requirement » sans balise, et l'officiel (`27006`, `28013`…) l'écrit en texte brut ; ul009 et up042 l'avaient déjà ainsi.

## 6. Listes à puces : 2 cartes

- ua002 : `• infligez 4 dégâts à un ennemi ;` -> `• Infligez 4 dégâts à un ennemi.` ; `• sonnez un ennemi.` -> `• Sonnez un ennemi.`
- ua025 : `• camouflez Kitsune ;` -> `• Camouflez Kitsune.` ; `• hébétez un ennemi.` -> `• Hébétez un ennemi.`
Les autres listes à puces (tk022, tk024, tk102, tk104, tk203, td005, tr010, ta015, tj012, tx008, tx014, ub053, uj016, sj003, sj004, sa019, sh005, sc007) étaient déjà « Majuscule… . ».

## 7. Black Ops, Hitodama, Æthreal Shift : 3 cartes

Le français affiché suit la décision de l'utilisateur ; `cards.json` (anglais imprimé) intact. Aucun test ne lisait ces textes.
- sa012 Black Ops : `<b>Action de héros</b> : après que votre héros a vaincu…` -> `<b>Réponse de héros</b> : après que…`
- sc012 Hitodama : `<b>Réponse de héros</b> <i>(attaque)</i> : infligez 3 dégâts…` -> `<b>Action de héros</b> <i>(attaque)</i> : …`
- sj020 Æthreal Shift : `<b>Action de héros</b> <i>(défense/contre)</i> : quand votre héros est censé subir…` -> `<b>Interruption de héros</b> <i>(défense/contre)</i> : …`

## 8. Karai : 2 cartes

ts101 et tl015 (même Karai, même texte) : `<b>Une fois vaincu</b>` -> `<b>Une fois vaincue</b>` (« révélée » l'était déjà). Je n'ai pas touché au sous-titre « (Sbire némésis de Leonardo.) ».

## 9. Redirection Mastery (up030) : 1 carte

Avant : `après que vous avez « exactement » défendu une attaque, infligez à l'attaquant des dégâts égaux à votre DEF pour cette attaque.`
Après : `après que vous avez défendu contre une attaque dont la valeur était exactement égale à votre DEF, infligez à l'attaquant des dégâts égaux à votre DEF pour cette attaque.`
Sens décidé conservé (l'attaque, boosts compris, vaut exactement votre DEF ; cas de test `tmnt_aspect_protection.py`). À valider par l'utilisateur.

## Correction hors liste (1 carte)

ta015 : « sur le manigance principale » -> « sur la manigance principale » (faute de genre évidente).

## 10. Laissé tel quel, comme demandé

Citation de Nobody (up024), « Double Peine » (tk006a), « rebondissements » (te201), « attribuez » (Mutanimal Van), noms de capacités en anglais, traits (liste « à trancher » des rapports : RHINO / RHINOCÉROS, HUMEUR, COPAINS…), coquilles de l'anglais (« Shugun », « Musroom », « TIme », « dashido »…), articles devant les titres anglais.

## Non vérifié

Scans non rouverts pour les 8 cartes reskin (texte anglais identique à l'officiel). Les fichiers générés `Fusion/marvel-lcg-src/public/js/traduction/*` ne sont pas commités (régénérés pour les tests puis remis à l'état du dépôt).
