# Marvel Champions LCG : projet custom

Jeu Marvel Champions LCG basé sur le moteur officiel open-source
`irefrixs/marvel-lcg`. Copie vivante du moteur :
`Fusion/marvel-lcg-src/` (détail des deux copies et du piège associé dans
`docs/reference/GUIDE-CREATION-CONTENU.md` §1 : ne jamais y toucher sans
avoir lu cette section en premier).

## Règle impérative : création ou modification de contenu

- **Nouvelle carte ou modification d'une carte existante** : lire et suivre
  `docs/reference/PROCESSUS-CARTE.md` du début à la fin. Rien n'est
  considéré terminé sans le gabarit rempli, preuve à l'appui, à la dernière
  étape (« Carte terminée : OUI »).
- **Nouveau héros** : lire et suivre `docs/reference/PROCESSUS-HEROS.md`, qui
  exige un `PROCESSUS-CARTE.md` complet pour chaque carte du pack.
- **Mot-clé rencontré pendant l'écriture d'un script** (officiel ou maison) :
  ouvrir sa fiche dans `docs/reference/mots-cles/` avant d'écrire une ligne
  de code. Absente → la créer d'abord, sur le gabarit donné en tête de
  `docs/reference/mots-cles/README.md`.

## Règle impérative : tests après un changement du moteur

- **Pas de batterie complète** de `tools/test_capacites.py` : elle dépasse
  4 à 5 heures (12 000+ cas) et sature le disque. Rejouer uniquement les
  cas des cartes que le changement peut toucher, par filtre de nom
  (`python tools/test_capacites.py .game-src <port> <rapport.json> "<filtre>"`).
- Choisir les cartes touchées en cherchant ce qui passe par le code modifié
  (ex. toutes les cartes qui redirigent une défausse, toutes celles qui lisent
  leurs compteurs après un coût « Discard This »), puis lancer un filtre par
  famille. Ajouter un cas dédié dans `tools/cas/` : vert avec le changement,
  rouge sans.
- **Squirrel Girl** (héroïne fan-made, pack `sg`) n'est plus vérifiée : ne
  pas rejouer ses cas, leurs échecs ne bloquent ni un commit ni un push.
- Ports : base <= 36975 (jamais 49152+). Ne jamais lancer deux harnais sur le
  même `game_dir`. Le harnais réécrit `launch.json` : le remettre après coup.

## Règle impérative : vérification à l'écran

- **Toujours l'affichage « Normal » (la version classique)**, jamais le
  « Coloré », jamais le « Sobre » : ni pour regarder une capture, ni pour
  mesurer, ni pour dire « corrigé ». ⚠ PIÈGE DES NOMS : la valeur RANGÉE
  `epure` se lit « Normal » ; la valeur rangée `normal` se lit « Coloré »
  (`ui-app/src/board/affichage.ts`). Le harnais `ui-check` force le coloré par
  défaut (`global-setup`, `normal`) : dans un test temporaire, poser
  `localStorage.mc_affichage_v1 = 'epure'` avant d'ouvrir la page. Quand la
  couleur compte, poser aussi la teinte bleue du compte
  (`mc_teinte_v1` = `63,134,224`) et écarter `/get_preferences`.

Pour toute autre question (mode campagne, multijoueur, stratégie, rapports
d'audit passés), voir `docs/README.md`.
