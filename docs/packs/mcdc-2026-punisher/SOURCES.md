# Sources MC/DC 2026 (Punisher) : fichiers reçus de l'équipe MC/DC

Reçus le 20/10/2026. Les fichiers eux-mêmes sont dans `docs/packs/mcdc-2026-punisher/sources/` (dossier ignoré par git : ce sont des fichiers de l'équipe
MC/DC, `team@mcdc.fun`, non redistribués dans ce dépôt). Pour les retrouver : liens Drive ci-dessous (partagés avec l'utilisateur).

## 1. Event Guide 2026, en anglais (8 pages, images sans couche de texte)
- Fichier : `sources/2026_Campaign_Guide_EN.pdf` (4,5 Mo). Drive : https://drive.google.com/file/d/1Upo_edvuivWtuVGXkWX9OdAdEFVPKuc3/view (titre Drive « 2026_Campaign_Guide (full pages).pdf », créé le 15/10/2026).
- Contenu (relevé le 20/10/2026) : programme de l'événement ; contenu des cartes (scénarios 85 cartes dont Big Apple 55 ; sous-fifres 30 : Hobgoblin 15 et Jigsaw 15 ; sets modulaires 22 : Punisher's Hit List 8, SWAT Team 6, The Syndicate 7, Capo of the Past 1 ; divers 25 : booster « Full-art » 20, cartes défi 2, cartes de campagne 2, héros Hawkeye alternatif 1 ; 31 cartes dont l'intitulé est masqué : additional campaign cards 2, epic multiplayer 3, etc.) ;
  scénario 1 Big Apple (mise en place 3×3, Uptown Expansion optionnelle, 8 vilains CAPO, instructions de campagne, FAQ des lieux) ; scénario 2 Hobgoblin / Jigsaw ; scénario 3 Punisher (Target Lock, résumé de la phase du méchant, FAQ) ; scénario 4 Kingsfall (multijoueur épique à 2 à 4 groupes, Long Live the King, FAQ) ; crédits ; teasing « See you in 2027! ».
- À comparer au livret français déjà rédigé (`regles-fr.md`) et à `README.md` : le texte anglais est la référence ; l'extraction exige une lecture des images (pas de texte copiable).

## 2. « 2026 Full Art Reprints » : dossier d'arts alternatifs
- Drive : https://drive.google.com/drive/folders/1qCDqiOTbvYG9vG2p5Ebn9p71dPt6rRso (créé le 11/10/2026).
- Un seul fichier visible par l'accès actuel : `P - dr sinclair - RP.jpg` (1500 × 2150 px, 450 Ko), une version « pleine illustration » de **Dr. Sinclair** (MC/DC 6176, Protection, Soutien, Persona. Thérapeute, coût 2 ; illustration de Tana Ford) :
  `sources/full-art-reprint-dr-sinclair-6176.jpg`. Le guide annonce un booster « Full-art » de 20 cartes : les 19 autres ne sont pas dans le dossier partagé (ou pas visibles).
- **Correction du 20/10/2026** : la carte Dr. Sinclair EXISTE dans le jeu : `52017` (pack fan-made `silk`, Protection, Support, Persona. Therapist, coût 2, texte identique à l'image). Elle est branchée comme art alternatif `mcdc26` (`data/arts_alternatifs.json`).

## 3. Galerie des cartes MC/DC 2026 (20/10/2026)
- Page : https://www.mcdc.fun/2026-card-gallery. Les 215 images uniques sont téléchargées dans `sources/galerie/<section>/` par `telecharger-galerie.py` (relançable) ; inventaire dans `GALERIE.md`.
- Les 41 reprints (RP) de cette galerie sont le booster « Full-art » : 38 sont branchés comme arts alternatifs (`importer-full-art.py`, code `mcdc26`, images 615×882 dans `assets/pics/<id>_mcdc26.jpg`), 3 ne le sont pas : Heli-Quincarrier et Wiccan (décision utilisateur), Punisher 6138 (voir plus bas). Décisions dans `.planning/todos/2026-10-20-mcdc-full-art-questions.md`.
- **Punisher 6138** (`A - punisher - RP.jpg`) : carte NOUVELLE, Aggression, Ally coût 3, THW 1, ATK 2*, Soldier / Vigilante, « ★ Punisher's attacks gain piercing and ranged. Response: After Punisher attacks and defeats a minion, deal 2 damage to an enemy. » À créer avec le chantier de la campagne Punisher (PROCESSUS-CARTE.md) ; son illustration est cette image de la galerie. Aucun branchement.
- Les autres sections (scénarios, lieux, méchants, sous-fifres, sets modulaires, cartes de campagne et de défi) sont de la matière pour la future campagne Punisher : téléchargées seulement, non intégrées.
- Crédit : « Full Art Reprints : MC/DC 2026 (Jonah, Marvin, Scott, Tim) » dans `public/credits.html` et dans les nouveautés.
