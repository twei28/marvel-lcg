Intègre la campagne Hunting Season / Saison de Chasse de Nugget dans Narwhal
Champions à partir de ce dossier et du dépôt réel auquel tu as accès.

Lis d'abord LIRE_D_ABORD.md, SPECIFICATIONS.md et POINTS_OUVERTS.md, puis les
instructions applicables du dépôt et le kit de création fourni en référence.

Le préfixe `hs` est choisi par l'utilisateur. Conserve les IDs hs001 à hs226
avec les suffixes recto/verso. Vérifie sa disponibilité réelle avant fusion.
Le nom de pack est hunting_season ; le code MC4DB d'origine est
hunting_season_by_nugget. Ne réutilise pas aveuglément les anciens IDs MC4DB.

Les données et scripts fournis sont un brouillon, pas un pack jouable validé.
Termine chaque A_FAIRE_CLAUDE en réutilisant les API et exemples existants.
Ne laisse jamais une carte à liste vide passer pour une carte sans effet.
N'invente aucune méthode ni chaîne de ciblage. Les mots-clés de desc sont
natifs ; ne recode pas leurs effets ni les dégâts consécutifs des alliés.
Complète les textes d'ambiance si le projet exige une transcription intégrale.
Les statistiques X et * restent volontairement explicites : remplace-les par
la représentation native correcte et des capacités dynamiques après inspection.

Fusionne les fragments dans la structure réelle de cards.json et sets_info.json.
Attribue toi-même la clé numérique d'index. Vérifie les clones et les variantes
artistiques. L'image d'un clone conserve son numéro physique et son ID propre.

Implémente le paquet Trap indépendant, le vilain recto-verso Curtis Connors /
Lizard et son changement de stade, la queue de Scorpion et les blessures de
Jameson, les restrictions AERIAL de Vulture, le Lodge à stock partagé et les
cartes de rencontre dans les decks des joueurs. Les spécifications détaillent
l'ordre et les cas limites. Les calculs purs de campaign_rules.py peuvent être
réutilisés après adaptation ; leur stockage ne doit pas devenir un nouveau
schéma moteur improvisé.

Le carnet doit fonctionner aussi après une défaite aux scénarios 1 à 4.
Raccorde les achats, choix de récompense, suppressions et dépenses de mise en
place à l'interface existante. Respecte les exemplaires physiques, les choix du
Master Hunter et l'attribution des quatre sets experts numérotés.

La capacité Swarmed by Rats est en attente d'une décision de l'utilisateur :
la carte imprime Interrupt mais décrit un déclencheur After. Ne corrige pas
silencieusement en Response. Voir POINTS_OUVERTS.md et reference/cards/hs018.jpg.

Quand l'intégration est achevée, indique les fichiers modifiés, les points
restants et les validations réellement exécutées. Ne revendique pas de tests
en jeu à partir de la seule vérification statique jointe. Garde les blocs de
code présentés à l'utilisateur sous 500 à 600 lignes.
