# Restes après le déploiement du 19/10/2026 (18h02)

En ligne : corrections « Sur la table » (T1 à T17, jeton de dégâts retiré, flèches en arc, gel contre le Badoon corrigé, Draw Their Fire vérifiée) et les trois choix de la phase du méchant : « Guidée » (ancienne variante tris, défaut), « Plateau animé », « Accéléré ». Poussé sur GitHub (ede7f45e). Batterie complète : 6576/6581 (4 échecs connus du pack Squirrel Girl : sg006, sg007, sg009, sg013).

## À régler
- **Test ui-check qui échoue** : `phase-sur-table-lecture.spec.ts`, cas « klaw-ameliorations » (sélecteur de la source d'amélioration). Cause probable : l'éventail des améliorations (T14) a changé le DOM ; non vérifié.
- **Texte d'aide des réglages** : « Guidée : un « Suivant » par étape… » alors que le bouton du cartouche s'appelle « Étape suivante » ; à confirmer.
- **Tutoiement** dans d'autres écrans (ex. « Tu pourras changer à tout moment… » dans la fenêtre de choix) : l'utilisateur n'aime pas le tutoiement dans les textes ; à passer en revue.
- **Fenêtre « Choisis ta phase du méchant »** : posée une seule fois ; les joueurs actuels ne la reverront pas (ils sont migrés sur « Guidée » sans question). Décision en attente : la réafficher une fois à tous ?
- **Specs ui-check** qui posent encore `mc_phase_presentation: 'bis'` ou `'etape'` (`phase-detaille-defense.spec.ts`, `mise-en-place-pas-a-pas.spec.ts`, `phase-sur-table-lecture`, `phase-sur-table-multi`) : cette valeur se lit désormais « Guidée » ; à revoir.
- **« −X PV » des effets de carte révélée** : affiché au bilan seulement (le moteur ne publie ces effets qu'à la fin de l'écran).
- **Cache téléphone/tablette** de la version en ligne (fichiers servis avec max-age 1 an) : pas de solution durable ; empreintes `?v=` comme sur Play à concevoir, sans toucher BUILD à l'aveugle.
- **Version en ligne et défaut d'Assaut** : code identique côté rangement, moteur juste ; non confirmé en navigateur.
- **Palettes** corrigées (75 vilains + TMNT) jamais envoyées en ligne (`data/palettes-heros-corrections.json` exclu des déploiements).
- **Script de déploiement Linux** réutilisable (la procédure du 19/10 a été faite à la main, voir la mémoire `deploiement-verifier-joueurs-en-ligne`).

## Mis de côté (voir aussi 2026-10-19-table-telephone-tablette.md)
- Téléphone et tablette pour la phase du méchant (T13 abandonnée).
- T18 (« sur la table » devient « Étape par étape ») : ANNULÉE, remplacée par les trois choix.
- Draw Their Fire : pas de défaut ; le nom français « Attirer Leur Attention » ne contient pas « Draw Their Fire ».
