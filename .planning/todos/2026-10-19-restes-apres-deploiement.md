# Restes après le déploiement du 19/10/2026 (18h02)

En ligne : corrections « Sur la table » (T1 à T17, jeton de dégâts retiré, flèches en arc, gel contre le Badoon corrigé, Draw Their Fire vérifiée) et les trois choix de la phase du méchant : « Guidée » (ancienne variante tris, défaut), « Plateau animé », « Accéléré ». Poussé sur GitHub (ede7f45e). Batterie complète : 6576/6581 (4 échecs connus du pack Squirrel Girl : sg006, sg007, sg009, sg013).

## À régler
- **Test ui-check qui échoue** : `phase-sur-table-lecture.spec.ts`, cas « klaw-ameliorations » (sélecteur de la source d'amélioration). Cause probable : l'éventail des améliorations (T14) a changé le DOM ; non vérifié.
- **Texte d'aide des réglages** : « Guidée : un « Suivant » par étape… » alors que le bouton du cartouche s'appelle « Étape suivante » ; à confirmer.
- ~~**Tutoiement**~~ : **CLOS le 21/10/2026.** Relecture complète (~65 occurrences de tu/ton/ta sur les deux sites, contre 2-3 « vous » isolés) : la note ci-dessus datait du 19/10 et allait dans le mauvais sens — le site est en réalité très majoritairement au TUTOIEMENT, confirmé comme convention voulue par l'utilisateur le 21/10. Les dernières poches de « vous » (défi Lone Wolf, écran de campagne, bandeau de version, fin de Bataille) sont passées en « tu ». Hors périmètre, volontairement non touché : `mots-cles.ts` (vocabulaire officiel vérifié sur le Guide de Référence FR FFG/Asmodee) et les dictionnaires de cartes.
- **Fenêtre « Choisis ta phase du méchant »** : posée une seule fois ; les joueurs actuels ne la reverront pas (ils sont migrés sur « Guidée » sans question). Décision en attente : la réafficher une fois à tous ?
- **Specs ui-check** qui posent encore `mc_phase_presentation: 'bis'` ou `'etape'` (`phase-detaille-defense.spec.ts`, `mise-en-place-pas-a-pas.spec.ts`, `phase-sur-table-lecture`, `phase-sur-table-multi`) : cette valeur se lit désormais « Guidée » ; à revoir.
- ~~**« −X PV » des effets de carte révélée**~~ : **CLOS le 21/10/2026, PAS corrigé.** Relu dans le code (`DeroulePhase.tsx` ~l.2914) : le texte « → Scott Lang subit 1 dégât (10 PV) » s'affiche déjà EN DIRECT sous la carte révélée pendant la phase, pas seulement dans le bilan de fin de phase comme le disait cette note. Il ne manque que le badge animé « −X PV » qui vole sur la carte (comme pour une attaque normale) ; pour l'avoir il faudrait synthétiser une sous-étape animée à partir de l'effet agrégé que publie le moteur (il ne détaille pas coup par coup), avec un risque réel de rouvrir les animations de dégâts stabilisées le 19/10 (`ea6e5a57`, `48df5c19`). Décision de l'utilisateur : le texte suffit, pas touché.
- **Cache téléphone/tablette** de la version en ligne (fichiers servis avec max-age 1 an) : pas de solution durable ; empreintes `?v=` comme sur Play à concevoir, sans toucher BUILD à l'aveugle.
- **Version en ligne et défaut d'Assaut** : code identique côté rangement, moteur juste ; non confirmé en navigateur.
- **Palettes** corrigées (75 vilains + TMNT) jamais envoyées en ligne (`data/palettes-heros-corrections.json` exclu des déploiements).
- ~~**Script de déploiement Linux** réutilisable~~ : fait le 20/10/2026, `deploiement/deployer-linux.sh` (simulation par défaut, `--oui`, `--retour-arriere`), tests `deploiement/tests/test-deployer-linux.sh`. Jamais lancé en réel : premier vrai déploiement à surveiller.

## Mis de côté (voir aussi 2026-10-19-table-telephone-tablette.md)
- Téléphone et tablette pour la phase du méchant (T13 abandonnée).
- T18 (« sur la table » devient « Étape par étape ») : ANNULÉE, remplacée par les trois choix.
- Draw Their Fire : pas de défaut ; le nom français « Attirer Leur Attention » ne contient pas « Draw Their Fire ».
