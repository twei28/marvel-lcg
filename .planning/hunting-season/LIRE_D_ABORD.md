# Hunting Season / Saison de Chasse

Dossier à transmettre à Claude pour Narwhal Champions. Auteur : Nugget.
Préfixe demandé et retenu : `hs`. Pack : `hunting_season`.
Code de la fiche MC4DB d'origine : `hunting_season_by_nugget`.

## État réel du dossier

Les 226 cartes physiques sont représentées par 239 entrées JSON : les dix
complots principaux ont deux faces et les trois cartes de vilain Lizard aussi.
Chaque entrée possède une image de référence et un identifiant stable.
Les textes de gameplay sont transcrits manuellement. Les textes d'ambiance
ne sont pas transcrits dans le JSON ; ils restent lisibles sur les images.
L'OCR brut sert uniquement d'aide et ne constitue pas une transcription fiable.

Les dix configurations de scénario (standard et expert), les quatre modules,
le fragment d'index et la définition de campagne sont fournis.
Les scripts sont des **brouillons d'intégration partiels** : certains effets
simples emploient les API documentées, les autres portent un commentaire
`A_FAIRE_CLAUDE` avec le texte imprimé et les contraintes utiles. Un script
qui renvoie une liste vide ne signifie pas que la carte n'a aucun effet.
Ce pack ne doit pas être déclaré jouable tant que ces points sont ouverts.

`reference/campaign_rules.py` calcule les gains d'expérience, la progression,
les achats au Lodge, les soins et les changements du scénario final, sans
inventer une API du jeu. Il faut raccorder ses entrées à l'état réel du moteur
et ses résultats au carnet existant. Son dictionnaire est un modèle de travail,
pas une extension autorisée du schéma natif de campagne.

## Fichiers

- `integration/data/` : fragments de données à fusionner, sans écraser les fichiers existants.
- `integration/src/cards/pack/hunting_season/` : scripts par carte et adaptateur de campagne.
- `reference/cards/` : les 239 faces de référence en JPEG lisible.
- `reference/card_manifest.json` : correspondance entre ID, source et état du script.
- `reference/HuntingSeason_Campaign_Booklet.pdf` : livret original faisant autorité.
- `reference/campaign_rules.py` : calculs et transactions de campagne à raccorder.
- `reference/campaign_log_contract.json` : clés de carnet et besoins d'interface.
- `reference/mc4db_campaign.json` : fiche MC4DB exacte de cette campagne.
- `SPECIFICATIONS.md` : règles spéciales, expérience et points d'intégration.
- `POINTS_OUVERTS.md` : décisions et incompatibilités à traiter explicitement.
- `PROMPT_POUR_CLAUDE.md` : instruction prête à lui transmettre.
- `VERIFICATION.json` : contrôles statiques effectués, sans simulation du jeu.

Aucun accès au dépôt du moteur n'était disponible lors de la préparation.
Les fichiers Python ont été analysés syntaxiquement, pas importés dans le jeu.
Les API, les routes de chargement et les effets doivent être vérifiés par Claude
avec le dépôt réel et les documents moteur inclus.
