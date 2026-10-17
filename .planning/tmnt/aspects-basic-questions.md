# Aspect TMNT Basic (`ub`, pack `tmnt_aspect_basic`) : questions ouvertes

16/10/2026. Scans : `scratchpad/zip-aspect/TMNT Aspect/Basic/<fichier>.png` (zip « TMNT Aspect », Inkwire).
Une question par carte, multichoix, option recommandée en premier. Les cartes concernées sont codées selon
la recommandation (pour ne pas bloquer), mais restent « Carte terminée : NON » dans
`.planning/tmnt/aspects-basic-gabarits.md` tant que la réponse n'est pas rendue — sauf Q-ub03, non intégrée.

---

## Q-ub01 — ub002 Assess the Situation : trait TACTIC absent ?

Scan : `Basic/Assess the Situation.png`. Le scan ne porte AUCUN trait ; l'officielle 12033 a « TACTIC. ».
Le texte est identique, la capacité est branchée par `ability_link` sur 12033.

1. **(recommandé)** Suivre le scan : aucun trait. En jeu : la carte n'est pas trouvée par les effets qui
   cherchent une carte TACTIC (ex. Team-Building Exercise n'est pas concerné ; Ares ar007 cherche une
   amélioration TACTIC, pas un événement). Différence minime.
2. Considérer l'oubli : ajouter TACTIC. En jeu : comme l'officielle.
3. Autre (précise).

## Q-ub02 — ub047 Sky Wagon : traits NYC. VEHICLE. au lieu de LOCATION. S.H.I.E.L.D.

Scan : `Basic/Sky Wagon.png`. Bandeau « Helicarrier » (sans ✦ : carte non unique). Texte identique à 01092.

1. **(recommandé)** Suivre le scan (NYC, VEHICLE) : un van volant n'est pas un lieu, le choix paraît
   voulu. En jeu : compte comme soutien NYC (ex. Demolish ua015 gagne Déferlement/Perçant), ne compte pas
   comme LOCATION.
2. Ajouter LOCATION (NYC, VEHICLE, LOCATION). En jeu : en plus, compte pour les effets LOCATION.
3. Autre (précise).

## Q-ub03 — ub019 Honorable Blades : Usagi Yōjimbō n'existe pas dans la base

Scan : `Basic/Honorable Blades.png`. « Team-Up (Leonardo and Usagi Yōjimbō). Max 1 per deck.
Hero Action: Ready Leonardo and Usagi Yōjimbō. Cloak Leonardo. Place a tough status card on Usagi Yōjimō. »
Aucun personnage « Usagi Yōjimbō » (ni héros ni allié) dans `cards.json` : la carte serait injouable.
Coquille probable aussi : « Yōjimō » à la dernière ligne.

1. **(recommandé)** Ne pas intégrer la carte tant qu'Usagi n'existe pas (scan d'Usagi à fournir). En jeu :
   la carte n'apparaît pas.
2. L'intégrer quand même, injouable (Team-Up jamais rempli). En jeu : visible au deck-builder, jamais
   jouable.
3. Autre (précise).

→ Carte NON intégrée (absente de `cards.json`), aucun script.

## Q-ub04 — ub025 Leonardo (allié, sous-titre « Leo ») et le héros Leonardo (tl001, alter ego « Leo »)

Scan : `Basic/Leonardo.png`. Le moteur juge l'unicité sur titre + sous-titre (`CanCoexistWith`) : titre
« Leonardo » ET sous-titre « Leo » = alter ego du héros → les deux NE COEXISTENT PAS.

1. **(recommandé)** Garder ce comportement : un joueur Leonardo ne peut pas mettre l'allié Leonardo en jeu
   (même personnage). En jeu : l'allié est injouable dans un deck Leonardo et à côté d'un joueur Leonardo.
2. Les autoriser à coexister (allié et héros distincts). En jeu : deux Leonardo sur la table.
3. Autre (précise).

## Q-ub05 — ub008 Donatello (allié, « Donnie ») et le héros Donatello (td001, alter ego « Donnie »)

Scan : `Basic/Donatello.png`. Même situation que Q-ub04 : le moteur interdit la coexistence.
1. **(recommandé)** Garder (même personnage). 2. Autoriser la coexistence. 3. Autre (précise).

## Q-ub06 — ub029 Michelangelo (allié, « Mikey ») et le héros Michelangelo (tm001, alter ego « Mikey »)

Scan : `Basic/Michelangelo.png`. Même situation que Q-ub04.
1. **(recommandé)** Garder. 2. Autoriser la coexistence. 3. Autre (précise).

## Q-ub07 — ub041 Raphael (allié, « Raph ») et le héros Raphael (tr001, alter ego « Raph »)

Scan : `Basic/Raphael.png`. Même situation que Q-ub04.
1. **(recommandé)** Garder. 2. Autoriser la coexistence. 3. Autre (précise).

## Q-ub08 — ub022 Jennika (allié, « Jenny ») et l'héroïne Jennika (tj001, alter ego « Jenny »)

Scan : `Basic/Jennika.png`. Même situation que Q-ub04. NB : sa Réponse remonte une carte Shinobi, cartes
réservées au deck Jennika : sans l'héroïne, la Réponse n'a de cible que dans un deck qui en contiendrait.
1. **(recommandé)** Garder (non-coexistence). 2. Autoriser la coexistence. 3. Autre (précise).

## Q-ub09 — ub005 Casey Jones (allié, SANS sous-titre) : l'allié tr002 et le héros tc001 portent le même titre

Scan : `Basic/Casey Jones.png`. Titre « Casey Jones », pas de sous-titre : ne coexiste ni avec l'allié
Casey Jones de Raphael (tr002, sans sous-titre) ni avec le héros Casey Jones (tc001). Les deux alliés ont
des stats et textes différents.

1. **(recommandé)** Garder : un seul « Casey Jones » en jeu. En jeu : injouable dans un deck Casey Jones, et
   une seule des deux versions d'allié à la fois.
2. Distinguer les deux alliés (sous-titre maison) mais pas le héros. 3. Autre (précise).

## Q-ub10 — ub048 Slash (bandeau « ✦ Hulk ») et l'allié Slash de Michelangelo (tm002)

Scan : `Basic/Slash (Hulk).png`. Titre « Slash », pas de sous-titre ; tm002 « Slash », pas de sous-titre :
ne coexistent pas. Par la décision Q-R1 (bandeau), il ne coexiste pas non plus avec un héros/allié « Hulk ».
1. **(recommandé)** Garder les deux règles. 2. Autoriser Slash TMNT et Slash de Michelangelo ensemble.
3. Autre (précise).

## Q-ub11 — ub053 Splinter (soutien, bandeau « ✦ Stick ») et l'allié Splinter de Leonardo (tl002)

Scan : `Basic/Splinter.png`. Même titre unique « Splinter », sans sous-titre : un soutien et un allié du même
nom ne coexistent pas (règle d'unicité par titre, quel que soit le type).
1. **(recommandé)** Garder. 2. Autoriser la coexistence (types différents). 3. Autre (précise).
