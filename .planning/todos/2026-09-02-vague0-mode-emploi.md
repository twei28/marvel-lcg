# VAGUE 0 — mode d'emploi pour la session qui portera

Écrit le 02/09/2026 par une session qui **n'a rien codé**, pendant qu'une autre
session travaillait sur le dépôt. Quatre dossiers de portage sont prêts :

| Ordre | Pack | Dossier | Cartes | Diff. |
|---|---|---|---|---|
| 1 | Viv Vision | `2026-09-02-prep-vague0-viv-vision.md` | 12 | 2/5 |
| 2 | Hulk | `2026-09-02-prep-vague0-hulk.md` | 14 | 2/5 |
| 3 | Lady Sif | `2026-09-02-prep-vague0-lady-sif.md` | 18 | 2/5 |
| 4 | Iron Man (Model 42) | `2026-09-02-prep-vague0-iron-man-model-42.md` | 15 | 2/5 |

Chaque dossier contient : l'inventaire complet avec le **texte imprimé de
chaque carte relevé sur les scans**, l'étape 2 du `PROCESSUS-CARTE` déjà
remplie (carte de référence + pourquoi, avec les chemins de fichiers), les
collisions de noms vérifiées dans `data/cards.json`, et les questions à poser
à l'utilisateur avant d'écrire la première ligne.

## 1. La correction la plus utile de cette préparation

**La « provenance du paiement » n'est pas une brique à construire.** Six cartes
de la vague 0 disent « si tu as payé cette carte avec une ressource X ». J'avais
annoncé une extension moteur. C'est faux, vérifié le 02/09 :

- `effect.GetPaidResources().HasColor("Y")`, une ligne — modèle `01013`
  Photonic Blast, `src/cards/pack/core/captain_marvel/01013.py` ;
- la fabrique expose déjà `message.paid_resources.HasColor(...)`
  (`src/game/ability/factory/play.py:292`) ;
- **306 cartes officielles** portent cette tournure ;
- variante « using **only** X » : modèles `10004` et `10006`, dans le pack du
  Hulk **officiel** ;
- variante « **overpaid** with X » : modèle `58005` Starstruck (Wonder Man).

Conséquence : la vague 0 est encore plus légère qu'annoncée, et le seul vrai
inconnu du lot est `hk001b` Bruce Banner (une Interruption qui remplace un
complot par une attaque).

## 2. À faire EN PREMIER par la session qui porte : réserver les préfixes

C'est le seul geste qui touche un fichier partagé, et il doit être fait une
fois, par une seule session. Ajouter ces 4 entrées dans
`Fusion/marvel-lcg-src/tools/prefixes_fanmade.json`, clé `prefixes`, en
respectant l'ordre alphabétique du fichier :

```json
"hk": {
    "pack": "hulk_rainy",
    "libelle": "148. Custom (Hulk)",
    "cartes": 0,
    "depuis": "2026-09-02",
    "note": "RESERVE, pas encore cree. Vague 0 du deuxieme arrivage. Auteur Rainy. 14 cartes, difficulte 2/5. set_name a trancher : 'Hulk' est pris par le heros officiel 10001a. Pas de set nemesis dans le zip. Voir .planning/todos/2026-09-02-prep-vague0-hulk.md"
},
"im": {
    "pack": "iron_man_model_42",
    "libelle": "149. Custom (Iron Man Model 42)",
    "cartes": 0,
    "depuis": "2026-09-02",
    "note": "RESERVE, pas encore cree. Auteur Rainy. 15 cartes, difficulte 2/5. Toute l'economie tient au compteur `reactor`, lu par 10 cartes sur 15. set_name a trancher : 'Iron Man' est pris. Pas de set nemesis. Voir .planning/todos/2026-09-02-prep-vague0-iron-man-model-42.md"
},
"ls": {
    "pack": "lady_sif",
    "libelle": "150. Custom (Lady Sif)",
    "cartes": 0,
    "depuis": "2026-09-02",
    "note": "RESERVE, pas encore cree. Auteur Rainy. 18 cartes, difficulte 2/5. Seul pack de la vague 0 avec un set nemesis complet (Enchantress, Skurge). set_name 'Lady Sif' verifie libre. Voir .planning/todos/2026-09-02-prep-vague0-lady-sif.md"
},
"vv": {
    "pack": "viv_vision",
    "libelle": "147. Custom (Viv Vision)",
    "cartes": 0,
    "depuis": "2026-09-02",
    "note": "RESERVE, pas encore cree. Auteur Rainy. 12 cartes, difficulte 2/5, le plus petit pack du deuxieme arrivage. Mot-cle maison `breakthrough` non defini par l'auteur. Pas de set nemesis. Voir .planning/todos/2026-09-02-prep-vague0-viv-vision.md"
}
```

Puis `python3 tools/verifier_prefixes.py` : aucun défaut attendu.

## 3. Les 4 numéros de set sont libres

Dernier utilisé le 02/09 à 10h : `146. Custom (Necroverse)`. Les numéros 147 à
150 sont donc libres, et attribués ci-dessus.

⚠ **À revérifier au moment de la réservation** : une autre session travaillait
sur le dépôt pendant la préparation. Si elle a livré un pack entre-temps, elle
a pu prendre `147`. Relire `tools/prefixes_fanmade.json` avant d'écrire, et
décaler les quatre numéros en bloc si besoin. Les préfixes `hk`, `im`, `ls`,
`vv`, eux, ne collisionnent avec aucun des 48 préfixes existants.

## 4. Ce qui reste entièrement dû, pour chaque pack

La préparation couvre l'étape 1 (données) et l'étape 2 (cartes de référence) du
`PROCESSUS-CARTE`. **Restent dues, sans exception** :

- étape 3 : les scripts, après avoir posé les questions du §5 de chaque dossier ;
- étape 4 : les images dans `assets/pics/<card_id>.jpg` (les scans sont dans les
  zips à la racine du projet) ;
- étapes 5 et 6 : texte-contre-code et nombres, **carte par carte** — et les
  valeurs chiffrées des tableaux de préparation sont un premier relevé, à
  revérifier sur le scan, pas une source de vérité ;
- étape 7 : un cas dans `tools/test_capacites.py` par capacité, avec preuve par
  substitution (`tools/substituer_pack.py`) ;
- étape 8 : autoplay ciblé, 8 parties minimum, contre un héros témoin ;
- `PROCESSUS-HEROS` étapes 3 à 8 : deck de départ, `sets_info.json`, images,
  biographie dans `heros-info.js`, textes FR dans `textes-fr-fanmade.ts` ;
- la gate finale : un « Carte terminée : OUI » par carte, plus une partie
  complète jouée.

## 5. Le message à donner à l'autre session

> Prends la vague 0 du deuxième arrivage de packs fan-made. Tout est préparé
> dans `.planning/todos/`, commence par lire
> `2026-09-02-vague0-mode-emploi.md`, puis
> `2026-09-02-prep-vague0-viv-vision.md`.
>
> Fais les packs dans cet ordre : Viv Vision, Hulk, Lady Sif, Iron Man
> (Model 42). Un pack à la fois, terminé et commité avant de passer au suivant.
>
> Avant d'écrire quoi que ce soit : ajoute les 4 entrées RESERVE du §2 du mode
> d'emploi dans `tools/prefixes_fanmade.json` et lance
> `python3 tools/verifier_prefixes.py`.
>
> Le dossier de chaque pack a un §5 « Questions à poser AVANT d'écrire le
> premier script ». Pose-les-moi une par une, en multichoix, avant de coder ce
> pack-là. Ne les groupe pas et ne tranche pas tout seul.
>
> Les textes des cartes dans les tableaux sont un relevé fait sur les scans,
> pas une source de vérité : les étapes 5 et 6 du PROCESSUS-CARTE restent dues
> carte par carte, contre les scans des zips à la racine du projet.
>
> Suis `docs/reference/PROCESSUS-HEROS.md` et `PROCESSUS-CARTE.md` du début à la
> fin. Rien n'est terminé sans le gabarit rempli et « Carte terminée : OUI »
> pour chaque carte.

## 6. Deux fichiers de doc modifiés par la session de préparation, non commités

Pour éviter qu'ils soient ramassés par erreur dans un commit d'un autre
chantier :

- `.planning/todos/2026-08-29-plan-heros-vilains-fanmade.md` : état réel du
  plan remis à jour, §6 réécrit après lecture des 425 cartes, §7 sur les deux
  campagnes incomplètes, §8 sur les 9 mots-clés maison à ficher ;
- `docs/reference/mots-cles/acceleration.md` : encart signalant que le pack
  Spider-Man 2099 appelle « Acceleration » une capacité d'identité sans rapport
  avec le mot-clé officiel.
