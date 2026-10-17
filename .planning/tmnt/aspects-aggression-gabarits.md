# Aspect TMNT Aggression (`ua`, pack `tmnt_aspect_aggression`) : gabarits PROCESSUS-CARTE

16/10/2026, agent Aggression, branche `aspects-ua`. 41 scans ; ua006 Bo-Wing, ua009 Clobber, ua015 Demolish faits
par le socle (`aspects-socle-gabarits.md`). Cas : `Fusion/marvel-lcg-src/tools/cas/tmnt_aspect_aggression.py`
(filtre `[ua]`, 111 cas, 111/111 verts au dernier passage). Questions : `aspects-aggression-questions.md` (Q-UA1 à Q-UA3).
Images : `tools/importer_images_tmnt_aspects.py <zip-aspect> assets/pics ua` (41 images, assets/ gitignoré).
Bandeaux « ✦ <titre d'origine> » (décision Q-R1) : ua017 Exeen ✦ Angela, ua022 He-Dude ✦ Two-Gun Kid,
ua035 Rave ✦ Bug, ua040 Ujigami ✦ Shang-Chi -> `unique_also`. Sous-titres ordinaires (Leo, Raph, Mikey, Splinter) :
pas de bandeau.

## Reskins IDENTIQUES (`ability_link`, aucun script)

Classement du TSV re-vérifié contre l'officielle, scan par scan : les 20 textes sont identiques au nom près.
Firepower : le scan dit « for each upgrade exhausted » au lieu de « for each weapon upgrade » : même effet (seules
des WEAPON peuvent être inclinées par le coût) — gardé IDENTIQUE.

### ua001 : Aggressive Conditioning (reskin IDENTIQUE de 56013)

> **Converti en art alternatif de 56013 le 17/10/2026** : seule l'image différait de l'officielle, la carte `ua001` n'existe plus dans `cards.json` (image `56013_tmnt.jpg`, `data/arts_alternatifs.json`). Les cas du reskin sont supprimés, le TÉMOIN sur `56013` est conservé. Ce qui suit est l'historique.

- [x] Étape 2 : carte de référence : `56013` par `ability_link` (recette RECETTES §11). Module de `56013` relu : aucun
      nom ni card_id en dur ; `grep -rn '"56013"' src/game src/engine` : rien.
- [x] Étape 5 : texte du scan relu mot à mot contre `56013` : identique (nom de carte remplacé, citation ajoutée).
      Traits : ceux du SCAN. « Play under any player's control » : non mesure a 2 joueurs (capacite de l'original, `CanPlayThisUpgradeCard("Players")`)
      Résultat : conforme.
- [x] Étape 6 : nombres : Upgrade 3, RES R (poing, comme ua009/18012), CONDITION, MaxPerUnit 1, +3 PV / +1 ATK — recopiés de `56013` et vérifiés sur le scan (icône de ressource comparée
      aux cartes du même pack : poing = R comme ua009/18012, éclair = Y comme ua038/54016, nœuds = B comme ua034/35018).
      Résultat : conforme.
- [x] Étape 7 : cas `[ua] ua001 ...` + TÉMOIN `[ua] ua001 TEMOIN 56013` (même montage, même chiffre) : +3 PV et +1 ATK (attributs health+3, attack+1).
      Substitution (retrait de TOUS les `ability_link` du pack sauf ua006/ua009, mesuré en une passe, 30/54) : les
      cas de capacité de ua001 ROUGES, témoins verts.
      Résultat : verts avec le lien.
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay ciblé : voir « Autoplay » en fin de fichier (PAS jouée par le pilote).
- [x] Étape 8 bis : change ce qu'on VOIT ? NON (capacité de l'officielle, déjà dessinée).

Carte terminée : OUI — Q-R2 (deck-builder, homonyme) en attente.

### ua005 : Blood Rage (reskin IDENTIQUE de 45043)

> **Converti en art alternatif de 45043 le 17/10/2026** : seule l'image différait de l'officielle, la carte `ua005` n'existe plus dans `cards.json` (image `45043_tmnt.jpg`, `data/arts_alternatifs.json`). Les cas du reskin sont supprimés, le TÉMOIN sur `45043` est conservé. Ce qui suit est l'historique.

- [x] Étape 2 : carte de référence : `45043` par `ability_link` (recette RECETTES §11). Module de `45043` relu : aucun
      nom ni card_id en dur ; `grep -rn '"45043"' src/game src/engine` : rien.
- [x] Étape 5 : texte du scan relu mot à mot contre `45043` : identique (nom de carte remplacé, citation ajoutée).
      Traits : ceux du SCAN. 
      Résultat : conforme.
- [x] Étape 6 : nombres : Upgrade 1, RES Y (eclair), CONDITION, MaxPerUnit 1, 1 degat, 1 carte — recopiés de `45043` et vérifiés sur le scan (icône de ressource comparée
      aux cartes du même pack : poing = R comme ua009/18012, éclair = Y comme ua038/54016, nœuds = B comme ua034/35018).
      Résultat : conforme.
- [x] Étape 7 : cas `[ua] ua005 ...` + TÉMOIN `[ua] ua005 TEMOIN 45043` (même montage, même chiffre) : sbire tue par attaque de base : 1 degat subi, main 1->2, incline.
      Substitution (retrait de TOUS les `ability_link` du pack sauf ua006/ua009, mesuré en une passe, 30/54) : les
      cas de capacité de ua005 ROUGES, témoins verts.
      Résultat : verts avec le lien.
- [x] Étape 7 bis : limite imprimée ? NON (Max 1 per player = donnee).
- [x] Étape 8 : autoplay ciblé : voir « Autoplay » en fin de fichier (jouée).
- [x] Étape 8 bis : change ce qu'on VOIT ? NON (capacité de l'officielle, déjà dessinée).

Carte terminée : OUI — Q-R2 (deck-builder, homonyme) en attente.

### ua007 : "Bring It!" (reskin IDENTIQUE de 19030)

> **Converti en art alternatif de 19030 le 17/10/2026** : seule l'image différait de l'officielle, la carte `ua007` n'existe plus dans `cards.json` (image `19030_tmnt.jpg`, `data/arts_alternatifs.json`). Les cas du reskin sont supprimés, le TÉMOIN sur `19030` est conservé. Ce qui suit est l'historique.

- [x] Étape 2 : carte de référence : `19030` par `ability_link` (recette RECETTES §11). Module de `19030` relu : aucun
      nom ni card_id en dur ; `grep -rn '"19030"' src/game src/engine` : rien.
- [x] Étape 5 : texte du scan relu mot à mot contre `19030` : identique (nom de carte remplacé, citation ajoutée).
      Traits : ceux du SCAN. 
      Résultat : conforme.
- [x] Étape 6 : nombres : Event 0, RES Y, Max 1 per phase — recopiés de `19030` et vérifiés sur le scan (icône de ressource comparée
      aux cartes du même pack : poing = R comme ua009/18012, éclair = Y comme ua038/54016, nœuds = B comme ua034/35018).
      Résultat : conforme.
- [x] Étape 7 : cas `[ua] ua007 ...` + TÉMOIN `[ua] ua007 TEMOIN 19030` (même montage, même chiffre) : 2 sbires -> 2 cartes ; 2e copie refusee dans la meme phase (main 3 et non 4).
      Substitution (retrait de TOUS les `ability_link` du pack sauf ua006/ua009, mesuré en une passe, 30/54) : les
      cas de capacité de ua007 ROUGES, témoins verts.
      Résultat : verts avec le lien.
- [x] Étape 7 bis : limite imprimée ? OUI : « Max 1 per phase » -> temoin d'epuisement `Bring It! : Max 1 per phase` (2 copies, main 3).
- [x] Étape 8 : autoplay ciblé : voir « Autoplay » en fin de fichier (jouée).
- [x] Étape 8 bis : change ce qu'on VOIT ? NON (capacité de l'officielle, déjà dessinée).

Carte terminée : OUI — Q-R2 (deck-builder, homonyme) en attente.

### ua010 : Combat Training (reskin IDENTIQUE de 01057)

> **Converti en art alternatif de 01057 le 17/10/2026** : seule l'image différait de l'officielle, la carte `ua010` n'existe plus dans `cards.json` (image `01057_tmnt.jpg`, `data/arts_alternatifs.json`). Les cas du reskin sont supprimés, le TÉMOIN sur `01057` est conservé. Ce qui suit est l'historique.

- [x] Étape 2 : carte de référence : `01057` par `ability_link` (recette RECETTES §11). Module de `01057` relu : aucun
      nom ni card_id en dur ; `grep -rn '"01057"' src/game src/engine` : rien.
- [x] Étape 5 : texte du scan relu mot à mot contre `01057` : identique (nom de carte remplacé, citation ajoutée).
      Traits : ceux du SCAN. 
      Résultat : conforme.
- [x] Étape 6 : nombres : Upgrade 2, RES R, SKILL, MaxPerUnit 1, +1 ATK — recopiés de `01057` et vérifiés sur le scan (icône de ressource comparée
      aux cartes du même pack : poing = R comme ua009/18012, éclair = Y comme ua038/54016, nœuds = B comme ua034/35018).
      Résultat : conforme.
- [x] Étape 7 : cas `[ua] ua010 ...` + TÉMOIN `[ua] ua010 TEMOIN 01057` (même montage, même chiffre) : +1 ATK.
      Substitution (retrait de TOUS les `ability_link` du pack sauf ua006/ua009, mesuré en une passe, 30/54) : les
      cas de capacité de ua010 ROUGES, témoins verts.
      Résultat : verts avec le lien.
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay ciblé : voir « Autoplay » en fin de fichier (jouée).
- [x] Étape 8 bis : change ce qu'on VOIT ? NON (capacité de l'officielle, déjà dessinée).

Carte terminée : OUI — Q-R2 (deck-builder, homonyme) en attente.

### ua016 : Drop Kick (reskin IDENTIQUE de 10014)

> **Converti en art alternatif de 10014 le 17/10/2026** : seule l'image différait de l'officielle, la carte `ua016` n'existe plus dans `cards.json` (image `10014_tmnt.jpg`, `data/arts_alternatifs.json`). Les cas du reskin sont supprimés, le TÉMOIN sur `10014` est conservé. Ce qui suit est l'historique.

- [x] Étape 2 : carte de référence : `10014` par `ability_link` (recette RECETTES §11). Module de `10014` relu : aucun
      nom ni card_id en dur ; `grep -rn '"10014"' src/game src/engine` : rien.
- [x] Étape 5 : texte du scan relu mot à mot contre `10014` : identique (nom de carte remplacé, citation ajoutée).
      Traits : ceux du SCAN. 
      Résultat : conforme.
- [x] Étape 6 : nombres : Event 3, RES R, 4 degats — recopiés de `10014` et vérifiés sur le scan (icône de ressource comparée
      aux cartes du même pack : poing = R comme ua009/18012, éclair = Y comme ua038/54016, nœuds = B comme ua034/35018).
      Résultat : conforme.
- [x] Étape 7 : cas `[ua] ua016 ...` + TÉMOIN `[ua] ua016 TEMOIN 10014` (même montage, même chiffre) : paye en [physical] seul : 4 degats + sonne + 1 carte ; contre-cas energie : 4 degats seuls.
      Substitution (retrait de TOUS les `ability_link` du pack sauf ua006/ua009, mesuré en une passe, 30/54) : les
      cas de capacité de ua016 ROUGES, témoins verts.
      Résultat : verts avec le lien.
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay ciblé : voir « Autoplay » en fin de fichier (jouée).
- [x] Étape 8 bis : change ce qu'on VOIT ? NON (capacité de l'officielle, déjà dessinée).

Carte terminée : OUI — Q-R2 (deck-builder, homonyme) en attente.

### ua017 : Exeen (bandeau ✦ Angela) (reskin IDENTIQUE de 18011)

- [x] Étape 2 : carte de référence : `18011` par `ability_link` (recette RECETTES §11). Module de `18011` relu : aucun
      nom ni card_id en dur ; `grep -rn '"18011"' src/game src/engine` : rien.
- [x] Étape 5 : texte du scan relu mot à mot contre `18011` : identique (nom de carte remplacé, citation ajoutée).
      Traits : ceux du SCAN. 
      Résultat : conforme.
- [x] Étape 6 : nombres : Ally 0, PV 3, ATK 2*, THW 0*, RES B, traits DIMENSION X / NOVA POSSE, unique_also Angela — recopiés de `18011` et vérifiés sur le scan (icône de ressource comparée
      aux cartes du même pack : poing = R comme ua009/18012, éclair = Y comme ua038/54016, nœuds = B comme ua034/35018).
      Résultat : conforme.
- [x] Étape 7 : cas `[ua] ua017 ...` + TÉMOIN `[ua] ua017 TEMOIN 18011` (même montage, même chiffre) : sbire trouve et mis en jeu ; aucun sbire -> Exeen defaussee ; bandeau : Angela/Exeen exclusifs dans les deux sens.
      Substitution (retrait de TOUS les `ability_link` du pack sauf ua006/ua009, mesuré en une passe, 30/54) : les
      cas de capacité de ua017 ROUGES, témoins verts.
      Résultat : verts avec le lien.
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay ciblé : voir « Autoplay » en fin de fichier (jouée).
- [x] Étape 8 bis : change ce qu'on VOIT ? NON (capacité de l'officielle, déjà dessinée).

Carte terminée : OUI — bandeau Q-R1 appliqué (unique_also).

### ua018 : Firepower (reskin IDENTIQUE de 54014)

- [x] Étape 2 : carte de référence : `54014` par `ability_link` (recette RECETTES §11). Module de `54014` relu : aucun
      nom ni card_id en dur ; `grep -rn '"54014"' src/game src/engine` : rien.
- [x] Étape 5 : texte du scan relu mot à mot contre `54014` : identique (nom de carte remplacé, citation ajoutée).
      Traits : ceux du SCAN. « for each upgrade » (scan) vs « for each weapon upgrade » (officielle) : meme sens (les ameliorations inclinees sont des WEAPON)
      Résultat : conforme.
- [x] Étape 6 : nombres : Event 1, RES R, 3 armes max, 3 degats chacune — recopiés de `54014` et vérifiés sur le scan (icône de ressource comparée
      aux cartes du même pack : poing = R comme ua009/18012, éclair = Y comme ua038/54016, nœuds = B comme ua034/35018).
      Résultat : conforme.
- [x] Étape 7 : cas `[ua] ua018 ...` + TÉMOIN `[ua] ua018 TEMOIN 54014` (même montage, même chiffre) : 2 armes inclinees -> 6 degats.
      Substitution (retrait de TOUS les `ability_link` du pack sauf ua006/ua009, mesuré en une passe, 30/54) : les
      cas de capacité de ua018 ROUGES, témoins verts.
      Résultat : verts avec le lien.
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay ciblé : voir « Autoplay » en fin de fichier (jouée).
- [x] Étape 8 bis : change ce qu'on VOIT ? NON (capacité de l'officielle, déjà dessinée).

Carte terminée : OUI — Q-R2 (deck-builder, homonyme) en attente.

### ua020 : Fusillade (reskin IDENTIQUE de 20026)

> **Converti en art alternatif de 20026 le 17/10/2026** : seule l'image différait de l'officielle, la carte `ua020` n'existe plus dans `cards.json` (image `20026_tmnt.jpg`, `data/arts_alternatifs.json`). Les cas du reskin sont supprimés, le TÉMOIN sur `20026` est conservé. Ce qui suit est l'historique.

- [x] Étape 2 : carte de référence : `20026` par `ability_link` (recette RECETTES §11). Module de `20026` relu : aucun
      nom ni card_id en dur ; `grep -rn '"20026"' src/game src/engine` : rien.
- [x] Étape 5 : texte du scan relu mot à mot contre `20026` : identique (nom de carte remplacé, citation ajoutée).
      Traits : ceux du SCAN. 
      Résultat : conforme.
- [x] Étape 6 : nombres : Event 2, RES B, 5 degats — recopiés de `20026` et vérifiés sur le scan (icône de ressource comparée
      aux cartes du même pack : poing = R comme ua009/18012, éclair = Y comme ua038/54016, nœuds = B comme ua034/35018).
      Résultat : conforme.
- [x] Étape 7 : cas `[ua] ua020 ...` + TÉMOIN `[ua] ua020 TEMOIN 20026` (même montage, même chiffre) : 1 arme inclinee -> 5 degats.
      Substitution (retrait de TOUS les `ability_link` du pack sauf ua006/ua009, mesuré en une passe, 30/54) : les
      cas de capacité de ua020 ROUGES, témoins verts.
      Résultat : verts avec le lien.
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay ciblé : voir « Autoplay » en fin de fichier (jouée).
- [x] Étape 8 bis : change ce qu'on VOIT ? NON (capacité de l'officielle, déjà dessinée).

Carte terminée : OUI — Q-R2 (deck-builder, homonyme) en attente.

### ua022 : He-Dude (Mikey, bandeau ✦ Two-Gun Kid) (reskin IDENTIQUE de 56010)

- [x] Étape 2 : carte de référence : `56010` par `ability_link` (recette RECETTES §11). Module de `56010` relu : aucun
      nom ni card_id en dur ; `grep -rn '"56010"' src/game src/engine` : rien.
- [x] Étape 5 : texte du scan relu mot à mot contre `56010` : identique (nom de carte remplacé, citation ajoutée).
      Traits : ceux du SCAN. DEFAUT DE L'ORIGINAL corrige : 56010 laissait choisir 2 fois le meme ennemi (Rhino 4 degats) ; `exclude="Targets"` (CORRECTIF commente dans cw/56010.py), vu ROUGE sans le correctif (4/4 rouges) et vert avec
      Résultat : conforme.
- [x] Étape 6 : nombres : Ally 3, PV 3, ATK 2*, THW 1*, RES B, TURTLE / WARRIOR, unique_also Two-Gun Kid — recopiés de `56010` et vérifiés sur le scan (icône de ressource comparée
      aux cartes du même pack : poing = R comme ua009/18012, éclair = Y comme ua038/54016, nœuds = B comme ua034/35018).
      Résultat : conforme.
- [x] Étape 7 : cas `[ua] ua022 ...` + TÉMOIN `[ua] ua022 TEMOIN 56010` (même montage, même chiffre) : 2 ennemis distincts touches (Rhino 2, Shocker 2) ; Rhino seul : 2 et non 4 ; bandeau exclusif.
      Substitution (retrait de TOUS les `ability_link` du pack sauf ua006/ua009, mesuré en une passe, 30/54) : les
      cas de capacité de ua022 ROUGES, témoins verts ; le contre-cas d ABSENCE reste vert (attendu).
      Résultat : verts avec le lien.
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay ciblé : voir « Autoplay » en fin de fichier (PAS jouée par le pilote).
- [x] Étape 8 bis : change ce qu'on VOIT ? NON (capacité de l'officielle, déjà dessinée).

Carte terminée : OUI — bandeau Q-R1 appliqué (unique_also).

### ua023 : Honed Technique (reskin IDENTIQUE de 28017)

> **Converti en art alternatif de 28017 le 17/10/2026** : seule l'image différait de l'officielle, la carte `ua023` n'existe plus dans `cards.json` (image `28017_tmnt.jpg`, `data/arts_alternatifs.json`). Les cas du reskin sont supprimés, le TÉMOIN sur `28017` est conservé. Ce qui suit est l'historique.

- [x] Étape 2 : carte de référence : `28017` par `ability_link` (recette RECETTES §11). Module de `28017` relu : aucun
      nom ni card_id en dur ; `grep -rn '"28017"' src/game src/engine` : rien.
- [x] Étape 5 : texte du scan relu mot à mot contre `28017` : identique (nom de carte remplacé, citation ajoutée).
      Traits : ceux du SCAN. 
      Résultat : conforme.
- [x] Étape 6 : nombres : Upgrade 3, RES B, Requirement BB, MaxPerUnit 1 — recopiés de `28017` et vérifiés sur le scan (icône de ressource comparée
      aux cartes du même pack : poing = R comme ua009/18012, éclair = Y comme ua038/54016, nœuds = B comme ua034/35018).
      Résultat : conforme.
- [x] Étape 7 : cas `[ua] ua023 ...` + TÉMOIN `[ua] ua023 TEMOIN 28017` (même montage, même chiffre) : Precision Strike payee en [mental] : 2+1 = 3 degats.
      Substitution (retrait de TOUS les `ability_link` du pack sauf ua006/ua009, mesuré en une passe, 30/54) : les
      cas de capacité de ua023 ROUGES, témoins verts.
      Résultat : verts avec le lien.
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay ciblé : voir « Autoplay » en fin de fichier (PAS jouée par le pilote).
- [x] Étape 8 bis : change ce qu'on VOIT ? NON (capacité de l'officielle, déjà dessinée).

Carte terminée : OUI — Q-R2 (deck-builder, homonyme) en attente.

### ua024 : Innate Aggression (reskin IDENTIQUE de 61034)

> **Converti en art alternatif de 61034 le 17/10/2026** : seule l'image différait de l'officielle, la carte `ua024` n'existe plus dans `cards.json` (image `61034_tmnt.jpg`, `data/arts_alternatifs.json`). Les cas du reskin sont supprimés, le TÉMOIN sur `61034` est conservé. Ce qui suit est l'historique.

- [x] Étape 2 : carte de référence : `61034` par `ability_link` (recette RECETTES §11). Module de `61034` relu : aucun
      nom ni card_id en dur ; `grep -rn '"61034"' src/game src/engine` : rien.
- [x] Étape 5 : texte du scan relu mot à mot contre `61034` : identique (nom de carte remplacé, citation ajoutée).
      Traits : ceux du SCAN. Starting en mise en place reelle : non mesure (le harnais ne place pas ua024 dans le deck de depart)
      Résultat : conforme.
- [x] Étape 6 : nombres : Upgrade 2, sans ressource, MaxPerDeck 1, +1 ATK, Starting — recopiés de `61034` et vérifiés sur le scan (icône de ressource comparée
      aux cartes du même pack : poing = R comme ua009/18012, éclair = Y comme ua038/54016, nœuds = B comme ua034/35018).
      Résultat : conforme.
- [x] Étape 7 : cas `[ua] ua024 ...` + TÉMOIN `[ua] ua024 TEMOIN 61034` (même montage, même chiffre) : +1 ATK ; la capacite Starting (`WhenGameBeginSetup`) est bien construite sur ua024.
      Substitution (retrait de TOUS les `ability_link` du pack sauf ua006/ua009, mesuré en une passe, 30/54) : les
      cas de capacité de ua024 ROUGES, témoins verts.
      Résultat : verts avec le lien.
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay ciblé : voir « Autoplay » en fin de fichier (jouée).
- [x] Étape 8 bis : change ce qu'on VOIT ? NON (capacité de l'officielle, déjà dessinée).

Carte terminée : OUI (Starting en mise en place réelle : vu en autoplay, 8 parties, « Add this card to your starting hand » accepté) — Q-R2 (deck-builder, homonyme) en attente.

### ua027 : Looking for Trouble (reskin IDENTIQUE de 16043)

> **Converti en art alternatif de 16043 le 17/10/2026** : seule l'image différait de l'officielle, la carte `ua027` n'existe plus dans `cards.json` (image `16043_tmnt.jpg`, `data/arts_alternatifs.json`). Les cas du reskin sont supprimés, le TÉMOIN sur `16043` est conservé. Ce qui suit est l'historique.

- [x] Étape 2 : carte de référence : `16043` par `ability_link` (recette RECETTES §11). Module de `16043` relu : aucun
      nom ni card_id en dur ; `grep -rn '"16043"' src/game src/engine` : rien.
- [x] Étape 5 : texte du scan relu mot à mot contre `16043` : identique (nom de carte remplacé, citation ajoutée).
      Traits : ceux du SCAN. 
      Résultat : conforme.
- [x] Étape 6 : nombres : Event 0, RES R, THWART, 3 menaces — recopiés de `16043` et vérifiés sur le scan (icône de ressource comparée
      aux cartes du même pack : poing = R comme ua009/18012, éclair = Y comme ua038/54016, nœuds = B comme ua034/35018).
      Résultat : conforme.
- [x] Étape 7 : cas `[ua] ua027 ...` + TÉMOIN `[ua] ua027 TEMOIN 16043` (même montage, même chiffre) : sbire mis en jeu, menace principale 5 -> 2.
      Substitution (retrait de TOUS les `ability_link` du pack sauf ua006/ua009, mesuré en une passe, 30/54) : les
      cas de capacité de ua027 ROUGES, témoins verts.
      Résultat : verts avec le lien.
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay ciblé : voir « Autoplay » en fin de fichier (jouée).
- [x] Étape 8 bis : change ce qu'on VOIT ? NON (capacité de l'officielle, déjà dessinée).

Carte terminée : OUI — Q-R2 (deck-builder, homonyme) en attente.

### ua028 : Magic Attack (reskin IDENTIQUE de 21043)

> **Converti en art alternatif de 21043 le 17/10/2026** : seule l'image différait de l'officielle, la carte `ua028` n'existe plus dans `cards.json` (image `21043_tmnt.jpg`, `data/arts_alternatifs.json`). Les cas du reskin sont supprimés, le TÉMOIN sur `21043` est conservé. Ce qui suit est l'historique.

- [x] Étape 2 : carte de référence : `21043` par `ability_link` (recette RECETTES §11). Module de `21043` relu : aucun
      nom ni card_id en dur ; `grep -rn '"21043"' src/game src/engine` : rien.
- [x] Étape 5 : texte du scan relu mot à mot contre `21043` : identique (nom de carte remplacé, citation ajoutée).
      Traits : ceux du SCAN. 
      Résultat : conforme.
- [x] Étape 6 : nombres : Event 1, RES R, SPELL, MaxPerDeck 1, jusqu'a 5 — recopiés de `21043` et vérifiés sur le scan (icône de ressource comparée
      aux cartes du même pack : poing = R comme ua009/18012, éclair = Y comme ua038/54016, nœuds = B comme ua034/35018).
      Résultat : conforme.
- [x] Étape 7 : cas `[ua] ua028 ...` + TÉMOIN `[ua] ua028 TEMOIN 21043` (même montage, même chiffre) : identite MYSTIC (Doctor Strange) : 3 cartes declarees -> 3 degats ; Spider-Man : injouable.
      Substitution (retrait de TOUS les `ability_link` du pack sauf ua006/ua009, mesuré en une passe, 30/54) : les
      cas de capacité de ua028 ROUGES, témoins verts ; le contre-cas d ABSENCE reste vert (attendu).
      Résultat : verts avec le lien.
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay ciblé : voir « Autoplay » en fin de fichier (PAS jouée par le pilote).
- [x] Étape 8 bis : change ce qu'on VOIT ? NON (capacité de l'officielle, déjà dessinée).

Carte terminée : OUI — Q-R2 (deck-builder, homonyme) en attente.

### ua029 : Martial Prowess (reskin IDENTIQUE de 10018)

> **Converti en art alternatif de 10018 le 17/10/2026** : seule l'image différait de l'officielle, la carte `ua029` n'existe plus dans `cards.json` (image `10018_tmnt.jpg`, `data/arts_alternatifs.json`). Les cas du reskin sont supprimés, le TÉMOIN sur `10018` est conservé. Ce qui suit est l'historique.

- [x] Étape 2 : carte de référence : `10018` par `ability_link` (recette RECETTES §11). Module de `10018` relu : aucun
      nom ni card_id en dur ; `grep -rn '"10018"' src/game src/engine` : rien.
- [x] Étape 5 : texte du scan relu mot à mot contre `10018` : identique (nom de carte remplacé, citation ajoutée).
      Traits : ceux du SCAN. 
      Résultat : conforme.
- [x] Étape 6 : nombres : Upgrade 2, RES R, MaxPerUnit 1 — recopiés de `10018` et vérifiés sur le scan (icône de ressource comparée
      aux cartes du même pack : poing = R comme ua009/18012, éclair = Y comme ua038/54016, nœuds = B comme ua034/35018).
      Résultat : conforme.
- [x] Étape 7 : cas `[ua] ua029 ...` + TÉMOIN `[ua] ua029 TEMOIN 10018` (même montage, même chiffre) : seule ressource disponible : paie Precision Strike, Martial Prowess inclinee.
      Substitution (retrait de TOUS les `ability_link` du pack sauf ua006/ua009, mesuré en une passe, 30/54) : les
      cas de capacité de ua029 ROUGES, témoins verts.
      Résultat : verts avec le lien.
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay ciblé : voir « Autoplay » en fin de fichier (jouée).
- [x] Étape 8 bis : change ce qu'on VOIT ? NON (capacité de l'officielle, déjà dessinée).

Carte terminée : OUI — Q-R2 (deck-builder, homonyme) en attente.

### ua031 : No Quarter (reskin IDENTIQUE de 28013)

> **Converti en art alternatif de 28013 le 17/10/2026** : seule l'image différait de l'officielle, la carte `ua031` n'existe plus dans `cards.json` (image `28013_tmnt.jpg`, `data/arts_alternatifs.json`). Les cas du reskin sont supprimés, le TÉMOIN sur `28013` est conservé. Ce qui suit est l'historique.

- [x] Étape 2 : carte de référence : `28013` par `ability_link` (recette RECETTES §11). Module de `28013` relu : aucun
      nom ni card_id en dur ; `grep -rn '"28013"' src/game src/engine` : rien.
- [x] Étape 5 : texte du scan relu mot à mot contre `28013` : identique (nom de carte remplacé, citation ajoutée).
      Traits : ceux du SCAN. 
      Résultat : conforme.
- [x] Étape 6 : nombres : Event 2, RES B, Requirement R, 4 degats — recopiés de `28013` et vérifiés sur le scan (icône de ressource comparée
      aux cartes du même pack : poing = R comme ua009/18012, éclair = Y comme ua038/54016, nœuds = B comme ua034/35018).
      Résultat : conforme.
- [x] Étape 7 : cas `[ua] ua031 ...` + TÉMOIN `[ua] ua031 TEMOIN 28013` (même montage, même chiffre) : 1 point d'exces -> 1 carte defaussee, l'Aggression en main.
      Substitution (retrait de TOUS les `ability_link` du pack sauf ua006/ua009, mesuré en une passe, 30/54) : les
      cas de capacité de ua031 ROUGES, témoins verts.
      Résultat : verts avec le lien.
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay ciblé : voir « Autoplay » en fin de fichier (jouée).
- [x] Étape 8 bis : change ce qu'on VOIT ? NON (capacité de l'officielle, déjà dessinée).

Carte terminée : OUI — Q-R2 (deck-builder, homonyme) en attente.

### ua032 : "Now I'm Mad" (reskin IDENTIQUE de 43019)

> **Converti en art alternatif de 43019 le 17/10/2026** : seule l'image différait de l'officielle, la carte `ua032` n'existe plus dans `cards.json` (image `43019_tmnt.jpg`, `data/arts_alternatifs.json`). Les cas du reskin sont supprimés, le TÉMOIN sur `43019` est conservé. Ce qui suit est l'historique.

- [x] Étape 2 : carte de référence : `43019` par `ability_link` (recette RECETTES §11). Module de `43019` relu : aucun
      nom ni card_id en dur ; `grep -rn '"43019"' src/game src/engine` : rien.
- [x] Étape 5 : texte du scan relu mot à mot contre `43019` : identique (nom de carte remplacé, citation ajoutée).
      Traits : ceux du SCAN. 
      Résultat : conforme.
- [x] Étape 6 : nombres : Upgrade 1, RES R, MaxPerUnit 1, +1 ATK / -1 THW sous la moitie — recopiés de `43019` et vérifiés sur le scan (icône de ressource comparée
      aux cartes du même pack : poing = R comme ua009/18012, éclair = Y comme ua038/54016, nœuds = B comme ua034/35018).
      Résultat : conforme.
- [x] Étape 7 : cas `[ua] ua032 ...` + TÉMOIN `[ua] ua032 TEMOIN 43019` (même montage, même chiffre) : 4 PV sur 10 : +1/-1 ; 5 PV sur 10 : rien (seuil strict).
      Substitution (retrait de TOUS les `ability_link` du pack sauf ua006/ua009, mesuré en une passe, 30/54) : les
      cas de capacité de ua032 ROUGES, témoins verts ; le contre-cas d ABSENCE reste vert (attendu).
      Résultat : verts avec le lien.
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay ciblé : voir « Autoplay » en fin de fichier (jouée).
- [x] Étape 8 bis : change ce qu'on VOIT ? NON (capacité de l'officielle, déjà dessinée).

Carte terminée : OUI — Q-R2 (deck-builder, homonyme) en attente.

### ua034 : Precision Strike (reskin IDENTIQUE de 35018)

> **Converti en art alternatif de 35018 le 17/10/2026** : seule l'image différait de l'officielle, la carte `ua034` n'existe plus dans `cards.json` (image `35018_tmnt.jpg`, `data/arts_alternatifs.json`). Les cas du reskin sont supprimés, le TÉMOIN sur `35018` est conservé. Ce qui suit est l'historique.

- [x] Étape 2 : carte de référence : `35018` par `ability_link` (recette RECETTES §11). Module de `35018` relu : aucun
      nom ni card_id en dur ; `grep -rn '"35018"' src/game src/engine` : rien.
- [x] Étape 5 : texte du scan relu mot à mot contre `35018` : identique (nom de carte remplacé, citation ajoutée).
      Traits : ceux du SCAN. 
      Résultat : conforme.
- [x] Étape 6 : nombres : Event 1, RES B, 2 degats, soin 2 — recopiés de `35018` et vérifiés sur le scan (icône de ressource comparée
      aux cartes du même pack : poing = R comme ua009/18012, éclair = Y comme ua038/54016, nœuds = B comme ua034/35018).
      Résultat : conforme.
- [x] Étape 7 : cas `[ua] ua034 ...` + TÉMOIN `[ua] ua034 TEMOIN 35018` (même montage, même chiffre) : Shocker tue -> heros soigne 2 (3 -> 1).
      Substitution (retrait de TOUS les `ability_link` du pack sauf ua006/ua009, mesuré en une passe, 30/54) : les
      cas de capacité de ua034 ROUGES, témoins verts.
      Résultat : verts avec le lien.
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay ciblé : voir « Autoplay » en fin de fichier (jouée).
- [x] Étape 8 bis : change ce qu'on VOIT ? NON (capacité de l'officielle, déjà dessinée).

Carte terminée : OUI — Q-R2 (deck-builder, homonyme) en attente.

### ua035 : Rave (bandeau ✦ Bug) (reskin IDENTIQUE de 16040)

- [x] Étape 2 : carte de référence : `16040` par `ability_link` (recette RECETTES §11). Module de `16040` relu : aucun
      nom ni card_id en dur ; `grep -rn '"16040"' src/game src/engine` : rien.
- [x] Étape 5 : texte du scan relu mot à mot contre `16040` : identique (nom de carte remplacé, citation ajoutée).
      Traits : ceux du SCAN. 
      Résultat : conforme.
- [x] Étape 6 : nombres : Ally 2, PV 2, ATK 1*, THW 1*, RES Y, DIMENSION X / NOVA POSSE, unique_also Bug — recopiés de `16040` et vérifiés sur le scan (icône de ressource comparée
      aux cartes du même pack : poing = R comme ua009/18012, éclair = Y comme ua038/54016, nœuds = B comme ua034/35018).
      Résultat : conforme.
- [x] Étape 7 : cas `[ua] ua035 ...` + TÉMOIN `[ua] ua035 TEMOIN 16040` (même montage, même chiffre) : attaque de base du heros -> Rave soigne 1 ; bandeau exclusif.
      Substitution (retrait de TOUS les `ability_link` du pack sauf ua006/ua009, mesuré en une passe, 30/54) : les
      cas de capacité de ua035 ROUGES, témoins verts.
      Résultat : verts avec le lien.
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay ciblé : voir « Autoplay » en fin de fichier (jouée).
- [x] Étape 8 bis : change ce qu'on VOIT ? NON (capacité de l'officielle, déjà dessinée).

Carte terminée : OUI — bandeau Q-R1 appliqué (unique_also).

### ua038 : Spoiling for a Fight (reskin IDENTIQUE de 54016)

> **Converti en art alternatif de 54016 le 17/10/2026** : seule l'image différait de l'officielle, la carte `ua038` n'existe plus dans `cards.json` (image `54016_tmnt.jpg`, `data/arts_alternatifs.json`). Les cas du reskin sont supprimés, le TÉMOIN sur `54016` est conservé. Ce qui suit est l'historique.

- [x] Étape 2 : carte de référence : `54016` par `ability_link` (recette RECETTES §11). Module de `54016` relu : aucun
      nom ni card_id en dur ; `grep -rn '"54016"' src/game src/engine` : rien.
- [x] Étape 5 : texte du scan relu mot à mot contre `54016` : identique (nom de carte remplacé, citation ajoutée).
      Traits : ceux du SCAN. 
      Résultat : conforme.
- [x] Étape 6 : nombres : Event 0, RES Y — recopiés de `54016` et vérifiés sur le scan (icône de ressource comparée
      aux cartes du même pack : poing = R comme ua009/18012, éclair = Y comme ua038/54016, nœuds = B comme ua034/35018).
      Résultat : conforme.
- [x] Étape 7 : cas `[ua] ua038 ...` + TÉMOIN `[ua] ua038 TEMOIN 54016` (même montage, même chiffre) : sbire mis en jeu -> heros redresse.
      Substitution (retrait de TOUS les `ability_link` du pack sauf ua006/ua009, mesuré en une passe, 30/54) : les
      cas de capacité de ua038 ROUGES, témoins verts.
      Résultat : verts avec le lien.
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay ciblé : voir « Autoplay » en fin de fichier (PAS jouée par le pilote).
- [x] Étape 8 bis : change ce qu'on VOIT ? NON (capacité de l'officielle, déjà dessinée).

Carte terminée : OUI — Q-R2 (deck-builder, homonyme) en attente.

### ua039 : Suppressing Fire (reskin IDENTIQUE de 46014)

> **Converti en art alternatif de 46014 le 17/10/2026** : seule l'image différait de l'officielle, la carte `ua039` n'existe plus dans `cards.json` (image `46014_tmnt.jpg`, `data/arts_alternatifs.json`). Les cas du reskin sont supprimés, le TÉMOIN sur `46014` est conservé. Ce qui suit est l'historique.

- [x] Étape 2 : carte de référence : `46014` par `ability_link` (recette RECETTES §11). Module de `46014` relu : aucun
      nom ni card_id en dur ; `grep -rn '"46014"' src/game src/engine` : rien (sauf le commentaire « Fix 46014 » de defeated.py, sans effet de nom).
- [x] Étape 5 : texte du scan relu mot à mot contre `46014` : identique (nom de carte remplacé, citation ajoutée).
      Traits : ceux du SCAN. 
      Résultat : conforme.
- [x] Étape 6 : nombres : Upgrade 0, RES B, TACTIC, MaxPerUnit 1 — recopiés de `46014` et vérifiés sur le scan (icône de ressource comparée
      aux cartes du même pack : poing = R comme ua009/18012, éclair = Y comme ua038/54016, nœuds = B comme ua034/35018).
      Résultat : conforme.
- [x] Étape 7 : cas `[ua] ua039 ...` + TÉMOIN `[ua] ua039 TEMOIN 46014` (même montage, même chiffre) : attachee a Shocker, attaque et defaite -> soin 2 (3 -> 1).
      Substitution (retrait de TOUS les `ability_link` du pack sauf ua006/ua009, mesuré en une passe, 30/54) : les
      cas de capacité de ua039 ROUGES, témoins verts.
      Résultat : verts avec le lien.
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay ciblé : voir « Autoplay » en fin de fichier (jouée).
- [x] Étape 8 bis : change ce qu'on VOIT ? NON (capacité de l'officielle, déjà dessinée).

Carte terminée : OUI — Q-R2 (deck-builder, homonyme) en attente.

## Cartes NOUVELLES et MODIFIÉE (scripts propres `src/cards/pack/tmnt_aspect_aggression/uaNNN.py`)

Commun : ressource vérifiée contre une carte du même pack (poing = R : ua009 Clobber / 18012 ; éclair = Y :
ua038 / 54016 ; nœuds = B : ua034 / 35018). Le texte imprimé, les cartes de référence et les mots-pièges sont
recopiés en tête de chaque module. Substitution : `tools/substituer_pack.py <game> 30200 ua0` (stub de chaque
module, cas filtrés sur le card_id) : 19/19 cartes avec au moins un cas rouge ; les cas restés verts sont TOUS
des contre-cas d'absence d'effet (listés carte par carte).

### ua002 : Apex Predator (NOUVELLE)

- [x] Étape 2 : Rampage : `ua015` Demolish (`CostFunc.Rampage`) ; « Choose: » : `sk041` / `20008` (`ChooseAbilities`).
- [x] Étape 5 : « additional cost » (coût, Tenace = impayé), « Choose » (une branche), « an enemy » ×2,
      [star] = rappel. Fiche rampage.md lue. Résultat : conforme.
- [x] Étape 6 : coût « 1* », RES Y, Rampage 2, 4 dégâts. Résultat : conforme.
- [x] Étape 7 : `[ua] ua002 ... branche Deal 4` (2 dégâts, deck 6→4, Rhino 4), `... branche Stun` ; contre-cas
      `... identite Tenace` (rien). Sans module : 2/3 rouges (le contre-cas Tenace reste vert, attendu).
      Résultat : 3/3 verts.
- [x] Étape 7 bis : limite ? NON.
- [x] Étape 8 : jouée 2 fois (lot A), 4 dégâts à Rhino ; 0 traceback.
- [x] Étape 8 bis : NON (dégâts, statut Sonné déjà dessiné, défausse).

Carte terminée : OUI.

### ua003 : Assassin (Leo) (NOUVELLE)

- [x] Étape 2 : `36016` Gentle (`AfterUnitAttackEnd` + `GainForThisActive(attack_consequential_damage)`).
- [x] Étape 5 : « the villain OR an ELITE minion », « -1 consequential », [star] capacité constante.
      Résultat : conforme.
- [x] Étape 6 : coût 3, PV 3, ATK « 3** » (2 consécutifs), THW « 1* », RES B ; -1. Résultat : conforme.
- [x] Étape 7 : `[ua] ua003 ... VILAIN` (1 dégât consécutif), `... ELITE (Sandman)` (1), contre-cas `... NON ELITE`
      (2). Sans module : 2/3 rouges (contre-cas vert, attendu). Résultat : 3/3 verts.
- [x] Étape 7 bis : NON.
- [x] Étape 8 : mis en jeu (lots A et C) ; 0 traceback.
- [x] Étape 8 bis : NON.

Carte terminée : OUI.

### ua004 : Attack Training (MODIFIÉE de 32043)

- [x] Étape 2 : `32043` Attack Training, copié puis adapté (PAS d'`ability_link` : « NINJA or MUTANIMAL » au lieu
      de « X-MEN »).
- [x] Étape 5 : « NINJA OR MUTANIMAL » (OU, `CardFinder(traits=[...])`), « Max 1 TRAINING per ally » (natif,
      trait TRAINING). Résultat : conforme.
- [x] Étape 6 : coût 1, RES R, +1 ATK, +2 PV. Résultat : conforme.
- [x] Étape 7 : `[ua] ua004 ... NINJA (Assassin)`, `... MUTANIMAL (Leatherhead)`, `... Mockingbird -> injouable`.
      Sans module : 3/3 rouges. Résultat : 3/3 verts.
- [x] Étape 7 bis : NON (« Max 1 TRAINING per ally » est la règle native du sélecteur, inchangée depuis 32043).
- [x] Étape 8 : dans le lot C (2 copies), PAS jouée par le pilote ; 0 traceback.
- [x] Étape 8 bis : attache une carte à un allié : chemin d'attachement standard (déjà dessiné, comme 32043).

Carte terminée : OUI (non vue jouée en autoplay).

### ua008 : Chain Reaction (NOUVELLE)

- [x] Étape 2 : `35018` (dégâts puis `IsDefeated`) ; `60023` (cible choisie à la résolution).
- [x] Étape 5 : « that enemy », « second / third enemy » choisis après la défaite, chaîne arrêtée sinon.
      Résultat : conforme.
- [x] Étape 6 : coût 2, RES R, 2 / 2 / 3. Résultat : conforme.
- [x] Étape 7 : `[ua] ua008 ... Shocker -> Hydra Bomber -> Rhino 3`, contre-cas `... 1re cible survit`.
      Sans module : 2/2 rouges. Résultat : 2/2 verts.
- [x] Étape 7 bis : NON.
- [x] Étape 8 : jouée 3 fois (lot A) ; 0 traceback.
- [x] Étape 8 bis : NON.

Carte terminée : OUI.

### ua011 : Combo Move (NOUVELLE)

- [x] Étape 2 : `sk041` (« X damage among enemies » = `range=(N,N)`, `repeat_rules="Any"`) ; `vp003` (deux capacités
      exclusives sur une condition).
- [x] Étape 5 : « among enemies » (réparti, même ennemi permis), « your IDENTITY has MARTIAL ARTIST ».
      Résultat : conforme.
- [x] Étape 6 : coût 1, RES Y, 2 / 3. Résultat : conforme.
- [x] Étape 7 : `[ua] ua011 ... 1 Rhino 1 Shocker`, `... 2 sur Rhino`, `... Daredevil 3`. Sans module : 3/3 rouges.
      Résultat : 3/3 verts.
- [x] Étape 7 bis : NON.
- [x] Étape 8 : jouée 2 fois (lot B, Daredevil) ; 0 traceback.
- [x] Étape 8 bis : NON.

Carte terminée : OUI.

### ua012 : Commando (Raph) (NOUVELLE)

- [x] Étape 2 : `01083` Mockingbird (Réponse d'entrée en jeu, stun) ; `60191` (défausser un événement en coût).
- [x] Étape 5 : flèche = coût, « an event » sans trait, « enters play ». Résultat : conforme.
- [x] Étape 6 : coût 2, PV 2, ATK 1*, THW 1*, RES Y. Résultat : conforme.
- [x] Étape 7 : `[ua] ua012 ... Rhino sonne, 35018 defausse` ; contre-cas `... aucun evenement`. Sans module : 1/2
      rouge (contre-cas vert, attendu). Résultat : 2/2 verts.
- [x] Étape 7 bis : NON.
- [x] Étape 8 : mis en jeu et Réponse partie (lots A et C, 5 fois) ; 0 traceback.
- [x] Étape 8 bis : NON.

Carte terminée : OUI.

### ua013 : Critical Wound (NOUVELLE)

- [x] Étape 2 : `43012` Puncture Wound (cible « attaquée ce tour » via `world.stat.this_turn_made_attack`) ;
      `33005` Exploit Weakness (+1 par attaque) ; `sk093` (`GiveKeywordToAttached(..., apply=)`) pour DONNER
      vulnerable (fiche vulnerable.md lue ; aucune carte ne le donnait encore).
- [x] Étape 5 : « a MINION », « YOUR HERO attacked THIS TURN », « non-ELITE » (vulnerable seul), « each attack ».
      Résultat : conforme.
- [x] Étape 6 : coût 1, RES Y, +1. Résultat : conforme.
- [x] Étape 7 : `[ua] ua013 ... Shocker ... sonne = defausse`, `... ELITE Radioactive Man : pas vulnerable, 2 puis 3`
      (5 dégâts), contre-cas `... PAS attaque -> injouable`. Sans module : 3/3 rouges. Résultat : 3/3 verts.
- [x] Étape 7 bis : NON.
- [x] Étape 8 : dans le lot C (2 copies), PAS jouée par le pilote ; 0 traceback.
- [x] Étape 8 bis : attache une carte à un sbire : chemin standard (Exploit Weakness).

Carte terminée : OUI (non vue jouée en autoplay).

### ua014 : Daitō (NOUVELLE)

- [x] Étape 2 : `54018` Bambino (restricted sur identité, Interruption d'attaque du porteur) ; `31029` / `34007`
      (`Friend`) ; `tc012` (`GainPiercing`). Fiches restricted.md, piercing.md lues.
- [x] Étape 5 : « ATTACKS an enemy » (toute attaque, pas seulement de base), « exhaust → », « 1 additional AND
      piercing ». Résultat : conforme.
- [x] Étape 6 : coût 1, RES R, +1. Résultat : conforme.
- [x] Étape 7 : `[ua] ua014 ... heros, Rhino Tenace -> 3 degats, Tenace defausse`, `... ALLIE Leatherhead -> 4`.
      Sans module : 2/2 rouges. Résultat : 2/2 verts.
- [x] Étape 7 bis : NON.
- [x] Étape 8 : mis en jeu et Interruption partie 5 fois (lots A et C : « Daredevil gagne 1 dégât supplémentaire …
      gagne (piercing) ») ; 0 traceback.
- [x] Étape 8 bis : attache (standard).

Carte terminée : OUI. Non mesuré : le « restricted » sur identité n'a pas de cas (copie exacte du montage Bambino).

### ua019 : Flow of Battle (NOUVELLE) — Q-UA1

- [x] Étape 2 : `61035` Shakedown (« attack and exactly defeat ») ; `13017` (coût de défausse). Fiche
      `prerequisite.md` CRÉÉE (mot-clé non défini).
- [x] Étape 5 : « exactly » (`has_excess_damage=False`), « an ENEMY », « Hero Response », Max 1 per player
      (`MaxPerUnit`). « Prerequisite » : lecture NON tranchée (Q-UA1), lecture codée = jouable si identité MARTIAL ARTIST.
- [x] Étape 6 : coût 1, RES B, 3 cartes, max 1. Résultat : conforme.
- [x] Étape 7 : `[ua] ua019 ... exactement Shocker -> pioche 3`, contre-cas `... exces`, `... Prerequisite Spider-Man`.
      Sans module : 2/3 rouges (contre-cas exces vert, attendu). Résultat : 3/3 verts.
- [x] Étape 7 bis : NON (Max 1 per player = donnée).
- [x] Étape 8 : mise en jeu 2 fois (lot C) ; 0 traceback.
- [x] Étape 8 bis : NON.

**Réponse du 17/10/2026** : « Prerequisite (MARTIAL ARTIST) » = jouable seulement si l'identité a le trait MARTIAL ARTIST (Spider-Man ne peut
pas la poser, Daredevil oui) : lecture codée confirmée, rien à changer.
Carte terminée : OUI.

### ua021 : Guerilla Trap (NOUVELLE)

- [x] Étape 2 : `13017` Lie in Wait ; `ua015` (soutien NYC) ; `ReduceCostToPlayThis` ; `ta002` (Dazed/Cloaked).
      Fiches daze.md, cloak.md lues.
- [x] Étape 5 : « that minion » (Trigger), « your HERO », « daze AND cloak », réduction seulement avec soutien NYC.
      Résultat : conforme.
- [x] Étape 6 : coût 2, -1, RES Y. Résultat : conforme.
- [x] Étape 7 : `[ua] ua021 ... sbire hebete, heros camoufle`, `... NYC -> cout 1`, contre-cas `... sans NYC`.
      Sans module : 2/3 rouges (contre-cas vert, attendu). Résultat : 3/3 verts.
- [x] Étape 7 bis : NON.
- [x] Étape 8 : mise en jeu 1 fois (lot C), Réponse non déclenchée dans ces parties ; 0 traceback.
- [x] Étape 8 bis : statuts Dazed / Cloaked : cartes d'état déjà dessinées (packs TMNT).

Carte terminée : OUI.

### ua025 : Kitsune (NOUVELLE)

- [x] Étape 2 : `04040` Spider-Girl (`AfterYouPlayThisFromHand`) ; `ta014` (Cloak soi-même).
- [x] Étape 5 : « play from your HAND », « choose » (une branche), « an enemy ». Résultat : conforme.
- [x] Étape 6 : coût 3, PV 3, ATK 1*, THW 1*, RES Y. Résultat : conforme.
- [x] Étape 7 : `[ua] ua025 ... Cloak Kitsune`, `... Daze an enemy`, contre-cas `... mise en jeu par un autre effet`.
      Sans module : 2/3 rouges (contre-cas vert, attendu). Résultat : 3/3 verts.
- [x] Étape 7 bis : NON.
- [x] Étape 8 : jouée 4 fois, Réponse partie 4 fois (lot A) ; 0 traceback.
- [x] Étape 8 bis : statuts déjà dessinés.

Carte terminée : OUI.

### ua026 : Leatherhead (NOUVELLE)

- [x] Étape 2 : `01051` Tigra (même Réponse, 1 → 2).
- [x] Étape 5 : « a MINION », « attacks AND defeats », « from HIM ». ⚠ Ordre moteur mesuré : les dégâts
      CONSÉCUTIFS se résolvent APRÈS les Réponses (TimingPriority) : Leatherhead soigne ce qu'il portait avant
      l'attaque, puis prend ses 2 consécutifs — exactement comme Tigra. Résultat : conforme au modèle officiel.
- [x] Étape 6 : coût 4, PV 4, ATK « 3** », THW 1*, RES R, soin 2. Résultat : conforme.
- [x] Étape 7 : `[ua] ua026 ... 2 prealables ... (2 au total)` ; contre-cas `... Rhino pas vaincu -> 4 (vaincu)`.
      Sans module : 1/2 rouge (contre-cas vert, attendu). Résultat : 2/2 verts.
- [x] Étape 7 bis : NON.
- [x] Étape 8 : mis en jeu 1 fois (lot C) ; 0 traceback.
- [x] Étape 8 bis : NON.

Carte terminée : OUI. À vérifier en partie réelle : l'ordre « Réponse puis dégâts consécutifs » est celui du
moteur (et de Tigra) ; s'il était jugé faux, c'est la TimingPriority du moteur qui serait à revoir, pas la carte.

### ua030 : Nerve Strike (NOUVELLE)

- [x] Étape 2 : `60023` Know Your Enemy (Discount 1 MARTIAL ARTIST, helper `fne.DiscountAbility`) ; `35018`.
      Fiche `discount.md` CRÉÉE avant le code.
- [x] Étape 5 : « THAT enemy », « Stun OR confuse » (une seule). Résultat : conforme.
- [x] Étape 6 : coût « 3* », Discount 1, RES Y, 2 dégâts. Résultat : conforme.
- [x] Étape 7 : `[ua] ua030 ... Stun`, `... Confuse`, `... Discount Daredevil (cout 2)`, contre-cas `... Spider-Man`.
      Sans module : 3/4 rouges (contre-cas vert, attendu). Résultat : 4/4 verts.
- [x] Étape 7 bis : NON.
- [x] Étape 8 : jouée 1 fois (lot B) ; 0 traceback.
- [x] Étape 8 bis : NON.

Carte terminée : OUI.

### ua033 : Pete (NOUVELLE) — Q-UA3

- [x] Étape 2 : `16032` Schadenfreude (`AfterYouDealDamage`) ; `62018` / `61033b` (deux coûts enchaînés). Compteur
      `pistol` ajouté à `CardFace.COUNTER`. Fiche uses.md lue.
- [x] Étape 5 : « exhaust AND remove 1 » (deux coûts), « that enemy » (`who_took_damage` est une LISTE : bogue vu
      et corrigé au 1er passage, AttributeError). « After YOU deal damage » : lecture NON tranchée (Q-UA3).
- [x] Étape 6 : coût 1, RES Y, Uses 3 pistol, 1 dégât. Résultat : conforme.
- [x] Étape 7 : `[ua] ua033 ... heros -> +1, pistolets 2, incline`, `... 2e attaque sans +1 (5)`, `... evenement ->
      declenche AUSSI (3)` (mesuré : le moteur compte l'événement comme « vous »), `... ALLIE -> pas de declenchement`.
      Sans module : les cas de déclenchement rouges, le cas « allié » (absence) vert. Résultat : 4/4 verts.
- [x] Étape 7 bis : pas de limite imprimée ; le coût « exhaust » borne l'usage : témoin `... 2e attaque` (5 et non 6).
- [x] Étape 8 : mis en jeu 2 fois, Réponse partie 2 fois (lot B) ; 0 traceback.
- [x] Étape 8 bis : compteur pistol : compteurs nommés déjà dessinés (Uses).

**Réponse du 17/10/2026** : « After you deal damage » = l'identité + les cartes que vous jouez (un allié qui attaque ne compte pas ; Precision
Strike déclenche Pete) : lecture codée confirmée, rien à changer.
Carte terminée : OUI.

### ua036 : Ray Fillet (NOUVELLE)

- [x] Étape 2 : `38003` Gambit (`ThisEnterPlayWithCounters`, coût compteur) ; `WhenUnitUseBasicPower`.
- [x] Étape 5 : « a basic power » (ATK et THW), « from him », étoiles des stats = rappel. Résultat : conforme.
- [x] Étape 6 : coût 3, PV 2, ATK 2*, THW 1*, RES B, 2 munitions, 2 dégâts. Résultat : conforme.
- [x] Étape 7 : `[ua] ua036 ... attaque (4, ammo 1)`, `... CONTRE (2, ammo 1, menace 5->4)`, `... 3e pouvoir sans
      bonus (10, ammo 0)`. Sans module : 3/3 rouges. Résultat : 3/3 verts.
- [x] Étape 7 bis : pas de limite ; témoin d'épuisement des munitions (3e usage sans dégât) : vert.
- [x] Étape 8 : mis en jeu 4 fois, Interruption 5 fois (lot B) ; 0 traceback.
- [x] Étape 8 bis : compteur ammo déjà dessiné.

Carte terminée : OUI.

### ua037 : Slash (NOUVELLE) — Q-UA2

- [x] Étape 2 : `01083` (entrée en jeu) ; `27166` (« take N damage » = identité).
- [x] Étape 5 : « Forced », « enters play », « take 3 damage » sans sujet : lecture NON tranchée (Q-UA2), codée =
      votre identité. Homonyme de `tm002` * Slash (unicité partagée par le titre).
- [x] Étape 6 : coût 2, PV 5, ATK 3*, THW 0*, RES Y, 3. Résultat : conforme.
- [x] Étape 7 : `[ua] ua037 ... identite 3 degats`. Sans module : 1/1 rouge. Résultat : vert.
- [x] Étape 7 bis : NON.
- [x] Étape 8 : mis en jeu 3 fois (lot B) : « Slash s'apprête à infliger 3 dégâts à Matt Murdock » ; 0 traceback.
- [x] Étape 8 bis : NON.

**Réponse du 17/10/2026** : « take 3 damage » = l'identité subit les 3 dégâts (Slash reste à 5 PV) : lecture codée confirmée. Homonyme de `tm002` :
même titre = même personnage, ils ne coexistent pas (décision G5).
Carte terminée : OUI.

### ua040 : Ujigami (Splinter) (NOUVELLE, bandeau ✦ Shang-Chi)

- [x] Étape 2 : `38003` (compteurs d'entrée) ; `hc001a` Hellcat (« Limit twice per round » = deux capacités
      `LimitOncePerRound`). Compteur `dagger` ajouté. `unique_also: ["Shang-Chi"]` (Q-R1).
- [x] Étape 5 : « Action » (pas Hero Action), « from here », « twice per round ». Résultat : conforme.
- [x] Étape 6 : coût 4, PV 3, ATK 2*, THW 2*, RES R, 10 dagues, 1 dégât, 2/round. Résultat : conforme.
- [x] Étape 7 : `[ua] ua040 ... Action (1, 9 dagues)`. Sans module : 2/2 rouges. Résultat : vert.
- [x] Étape 7 bis : OUI : témoin `[ua] ua040 ... la 3e Action du round est refusee` : trois tentatives, 2 dégâts et
      8 dagues mesurés. Résultat : vert.
- [x] Étape 8 : mis en jeu 3 fois, Action 6 fois (lot B) ; 0 traceback.
- [x] Étape 8 bis : compteur dagger, comme les autres compteurs nommés.

Carte terminée : OUI. Non mesuré : un cas d'unicité Ujigami / Shang-Chi (aucun allié « Shang-Chi » officiel dans
cards.json ; le héros 04098 porte ce titre — même mécanique `unique_also` que Bo-Wing, prouvée par `[reskin]`).

### ua041 : Yagi & Gorogoro (NOUVELLE)

- [x] Étape 2 : `tm002` (« attacks gain piercing ») ; `21019` Blade (Réponse forcée à choix) ; `ts007` (2 cartes).
- [x] Étape 5 : « BASIC attack », « discard 2 » (offert seulement avec 2 cartes), « REMOVE from the game ».
      Résultat : conforme.
- [x] Étape 6 : coût 2, PV 2, ATK 4 (aucun consécutif imprimé), THW —, RES B. Résultat : conforme.
- [x] Étape 7 : `[ua] ua041 ... percante, defausse 2 cartes`, `... une seule carte -> retire de la partie`.
      Sans module : 2/2 rouges. Résultat : 2/2 verts.
- [x] Étape 7 bis : NON.
- [x] Étape 8 : mis en jeu 1 fois, Réponse forcée 1 fois (lot B) ; 0 traceback.
- [x] Étape 8 bis : retrait de la partie (zone déjà gérée).

Carte terminée : OUI.

## Autoplay (étape 8), 16/10/2026, Rhino normal, profil équilibré, 8 parties par lot

| Lot | Deck | Blocages | Témoin | Blocages témoin |
|---|---|---|---|---|
| A | She-Hulk + 24 cartes ua (`scratchpad/deck-ua-A.json`) | 1/8 | She-Hulk TMNT du socle (`deck-she-hulk-tmnt.json`) | 1/8 |
| B | Daredevil + 22 cartes ua (`deck-ua-B.json`) | 1/8 | Daredevil de départ | 0/8 |
| C | Daredevil + 28 cartes ua restantes (`deck-ua-C.json`) | 0/8 | (témoin B) | 0/8 |

Grep NameError / AttributeError / TypeError / KeyError / AssertionError / Traceback : 0 sur les 40 journaux.
Jamais jouées par le pilote : ua001, ua004, ua013, ua022, ua023, ua028 (exige MYSTIC, absent des lots), ua038.

## Moteur touché

- `src/game/card/face/card_face.py` : compteurs `dagger`, `pistol` ajoutés à `COUNTER` (additif).
- `src/cards/pack/cw/56010.py` (Two-Gun Kid, officielle) : CORRECTIF `exclude="Targets"` — la 2e cible pouvait être
  la 1re (Rhino 4 dégâts). Témoin officiel `[ua] ua022 TEMOIN 56010` vert, ROUGE sans le correctif.
- `tools/test_cards.py` : 6599 OK, 0 erreur ; `verifier_prefixes.py` : OK. `[r` (reskin, rampage, règles…) : 120/120.
