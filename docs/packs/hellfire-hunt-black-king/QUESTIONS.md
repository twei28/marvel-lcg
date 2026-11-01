# Hellfire Hunt, scénario 2 « Black King » : vrais doutes de règle (01/11/2026)

Aucune question n'a pu être posée à l'utilisateur (brief commun) : chaque point ci-dessous a un CHOIX PROVISOIRE, documenté dans le code, et attend d'être posé UNE FOIS, image à l'appui, par le chef. Tranchés par les règles / le livret / la FAQ p. 22 avant d'arriver ici : l'ordre Absorb / Tactique du Roi, la face A sans limite, la limite qui ne compte que la face B, les compteurs qui s'empilent au-delà de la limite, le « once per round per player » de 2B, la Permanence de Captured by Hellfire! (le moteur la laisse en jeu, « add this card to the victory display » l'en fait sortir).

## 1. « Max 1[par joueur] fois par round » de la Tactique du Roi (face B)

- Carte : `hf207b` (`Scenario/Black King/7b.png`, texte « (Max 1[person] times per round.) » ; FAQ du livret p. 22 : « only the first instance of the 1[person] effect will trigger »).
- Lectures possibles :
  1. **N conversions par round, N = nombre de joueurs, tous joueurs confondus** (RETENUE, `TactiqueDuRoi`, compteur de round `king_tactic`).
  2. **1 conversion par round ET par joueur** (chaque joueur a la sienne, attribuée au joueur dont l'attaque a causé les dégâts).
  3. **1 conversion par round, point** (le FAQ ne donne que l'exemple à 1 joueur).
- Ce que chacune change EN JEU : à 1 joueur, rien (les trois disent 1). À 2 joueurs, (1) = deux conversions par round, quel que soit le joueur qui frappe ; (2) = pareil sauf si le même joueur frappe deux fois (la 2e frappe du même joueur s'empile) ; (3) = une seule : Shaw stocke beaucoup plus d'énergie, donc le stade 2 est plus dur.
- Recommandation : (1), la plus simple à lire ; (2) demanderait de savoir QUEL joueur a causé les dégâts (allié, événement, effet de carte : pas toujours un joueur).

## 2. « If there is no CAPTIVE ally is confused in this way » (`hf222` / `hf223` Hellfire Indoctrination)

- Carte : `Scenario/Black King/22.png`, `23.png`.
- Lectures : (a) un captif DÉJÀ désorienté n'est pas « désorienté de cette façon » : la carte gagne surge (RETENUE) ; (b) tout captif présent compte, même déjà désorienté : pas de surge.
- Ce que ça change : seulement quand le captif est déjà désorienté (second Hellfire Indoctrination dans le round, ou Hellfire Indoctrination après l'effet d'une autre carte) : (a) le joueur subit une carte de rencontre de plus ; (b) non.
- Recommandation : (a), c'est la lecture littérale de « in this way » (même formule que « If you cannot » : on regarde ce que CETTE carte a fait).

## 3. Dust attaque plusieurs cibles : les dégâts consécutifs (`hf208`)

- Carte : `Scenario/Black King/8.png` (ATQ 2★, deux icônes de dégâts consécutifs).
- Lectures : (a) Dust subit les dégâts consécutifs UNE fois par attaque (RETENUE : c'est ce que fait le moteur pour `33012` Dust officielle, qui frappe tous les sbires) ; (b) une fois par cible touchée (vilain + chaque sbire).
- Ce que ça change : (a) Dust (PV 3) survit à une attaque contre 3 cibles ; (b) elle meurt dès la 2e cible.
- Recommandation : (a), règle officielle des attaques multiples (« consequential damage is dealt once per attack »).

## 4. L'énergie de Shaw survit-elle au changement de stade ?

- Cartes : `hf201`/`hf202`/`hf203` (`Scenario/Black King/1.png`-`3.png`), `hf207a`.
- Le livret ne le dit pas. Lectures : (a) les compteurs restent sur la carte du stade vaincu et disparaissent avec elle, comme les dégâts et les statuts (RETENUE, comportement natif du moteur) ; (b) les compteurs passent au stade suivant.
- Ce que ça change : après la défaite du stade I, Shaw (II) arrive sans énergie en (a), ce qui rend le début du stade II plus facile ; le Black King (Permanent) reste attaché dans les deux cas.
- Recommandation : (a) (règle générale : le stade suivant est une nouvelle carte).

## Limites du moteur, à dire tel quel (pas des questions)

- **FAQ p. 22 (2B)** : « you can exhaust a captive ally you control, and you can do this on another player's turn ». Le moteur ne propose une Action de héros que pendant le tour du joueur qui la déclenche : la Limite « une fois par round et par joueur » est bien codée, mais l'usage pendant le tour d'un autre joueur ne l'est pas. À vérifier en partie réelle à deux joueurs.
- **`hf318` Hellfire Hunt (scénario 1, autre agent)** porte `"Acceleration": "1"` alors que son icône, comparée à celle de `hf338` (vraie icône Acceleration : pointe + barre) et à celle de `hf226`, est l'icône HAZARD (carte penchée sans barre). Non corrigé ici (hors périmètre) : à signaler au porteur du scénario 1.

## RÉPONSES DE L'UTILISATEUR (01/11/2026)
1 : autant de conversions que de joueurs (choix codé). 2 : un captif déjà désorienté ne compte pas, la carte gagne surge (choix codé) ; l'utilisateur a fait remarquer que c'était une règle de base, qu'il ne fallait pas la lui poser. 3 et 4 : NON posées, tranchées par les règles de base (dégâts consécutifs une fois par attaque ; un stade suivant est une nouvelle carte, compteurs perdus) = choix codés.
