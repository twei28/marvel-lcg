# Jigsaw : doutes de l'échafaudage (21/10/2026)

Échafaudage fait par `.planning/mcdc-punisher/construire_jigsaw.py` (idempotent). Aucun script de capacité.

1. **Stades du vilain** : le scan imprime I (p111), II (p112), II (p113), III (p114). Les défs disaient 1/1/2/2 ;
   corrigé en **1/2/2/3** (pu056a/pu056b/pu057a/pu057b). Standard = pu056a→pu057a, expert = pu056b→pu057b
   (même décalage que Bullseye 60065/60066 → 60066/60067).
2. **Étoile ★ imprimée sur une stat** : codée `N**` (convention de gs226 « 2** »). ATK Bushwhacker (p117, ★ seule)
   → `0**` ; Boost de Cut to Pieces (p131) → `0**`, de A Made Man (p139) → `1**`. Convention à confirmer au
   premier script (le plateau affiche le scan, pas ce champ).
3. **Manigance annexe p129 (Putting the Pieces Together)** : scan couché, tourné de 90° à l'export (assets/pics/pu065.jpg).
4. **Jigsaw's Knife (p115)** : le titre vertical est normal pour une pièce jointe, scan non tourné.
5. **Scénarios** : 5 manigances `fne` × standard/expert = 10 fichiers `*_jigsaw(_expert).json`, copiés du modèle
   Hammerhead. Le groupement « sous-fifres interchangeables » de l'interface (`underlings.js`, lu sur le set `fne`)
   n'est PAS branché : les 5 scénarios Jigsaw sont dans le pack `pu`, tuiles séparées. À trancher.
6. **Scans en 532×740** (plus petits que les cartes officielles 615×892) : exportés tels quels.
7. Textes des défs : non revérifiés carte par carte ici (revue prévue carte par carte avant chaque script).
