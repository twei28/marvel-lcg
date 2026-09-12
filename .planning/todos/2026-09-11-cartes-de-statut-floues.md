# Les cartes de statut (Stunned, Confused, Tough) sont floues en jeu : CORRIGÉ le 11/09/2026

**Remonté par un joueur (Manu, Discord) le 11/09/2026**, capture à l'appui :
« ce truc est trooop flou. Là dans le screenshot on arrive à lire, mais dans le
jeu c'est pas simple ». La capture montre la carte d'état « Stunned » en grand
sur le plateau, texte à peine lisible.

## Ce qu'on sait

- Le plateau agrandit les cartes au survol et en grand ; les scans de statut
  viennent de `assets/pics/` (300 px de large pour les officielles) et sont
  étirés bien au-delà.
- `tools/telecharger_scans_hd.py` ne télécharge les HD que pour les types
  Hero, AlterEgo, Villain et MainScheme (`TYPES`, ligne ~41) : les cartes de
  statut n'en font pas partie, et `Cache.LoadImageHD` ne les sert donc jamais
  en HD.
- Les trois cartes d'état sont partagées par toutes les parties : trois
  fichiers à traiter, pas une collection.

## Par où commencer

1. Identifier les `card_id` des trois statuts et vérifier ce que `assets/pics`
   et `assets/pics-fr` contiennent pour elles (taille réelle).
2. Soit ajouter le type des statuts à `TYPES` de `telecharger_scans_hd.py`
   (si les serveurs d'images les servent en HD), soit déposer une fois pour
   toutes trois scans HD à la main dans `assets/pics-hd/`.
3. Vérifier à l'œil dans le plateau, en grand, que le texte est lisible.


## ✅ Corrigé le 11/09/2026

**Cause mesurée** : le plateau demande `stunned` / `confused` / `tough` ; le
moteur ne trouve aucun scan dans `assets/pics` ni `pics-fr` et se rabat sur
`assets/textures/<nom>.webp`, qui faisait **149 × 95 px**. La carte en jeu fait
615 px de large : étirement ×4.

**Aucune source HD n'existe** (quatre recherches, deux pages lues : MarvelCDB
et Hall of Heroes ne traitent pas ces cartes comme des cartes, seuls des
jetons 3D circulent). L'utilisateur a fourni une photo produit eBay
(900 × 1200) des trois cartes : découpe, redressement (PCA, numpy pur, ni cv2
ni scipy sur la machine) et remise au ratio d'origine à **615 × 392**. Les
originaux 149 × 95 sont en historique git.

**Preuve** : `Cache.LoadImage('stunned')` sert désormais 392 × 615 (tourné
en portrait comme tout scan), contre 95 × 149 avant.

**Limite assumée** : c'est une photo, pas un scan ; on devine une ombre et un
léger trapèze sur Tough. Largement lisible en grand, ce qui était la demande.


## ✅ Vrais scans le 12/09/2026

L'utilisateur a déposé six scans propres (1484×1060 et 1536×1024, fond
blanc) : Tough / Confused / Stunned en anglais, Tenace / Désorienté / Sonné
en français. Recadrés au bord de la carte (pixels saturés, pas l'ombre) et au
ratio 615/392, sortis en webp de 1230×784.

- anglais : `assets/textures/{tough,confused,stunned}.webp` (versionnés,
  déployés avec le code) ;
- français : `assets/pics-fr/fr_{tough,confused,stunned}.webp` (dossier
  non versionné et exclu du déploiement : **à copier à la main sur le
  serveur**, fait le 12/09), déclarés dans `SCANS_FR_MAISON` de
  `ui-app/src/board/scans-fr.ts` puisque la liste générée ne connaît que les
  codes OCTGN.

La photo eBay redressée du 11/09 est en historique git.
