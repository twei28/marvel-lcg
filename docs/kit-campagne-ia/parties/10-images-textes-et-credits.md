---

## 10. Images, textes français, pages du livret, biographies et crédits

Les images sont **fournies par l'utilisateur** : tu ne les produis pas. Tu livres les **tableaux** qui permettent à
Claude de les placer sans ambiguïté, et tous les **textes**.

### 10.1 Les images de cartes : `assets/pics/<card_id>.<jpg|png|webp>`

* **Une image par `card_id`**, nommée exactement comme l'identifiant. **L'extension est obligatoire** (le
  chargeur `engine/file/cache.py` cherche `.webp`, `.jpg`, `.png`). Une face = une image (`wd001a.jpg`, `wd001b.jpg`).
* Une carte `full_link` **n'a pas d'image propre**. Une carte `pic_id` emprunte celle d'une autre.
* **Format** : portrait ≈ **600 × 840** (le petit côté est ramené à 600–615 px). **Les complots (principaux et
  annexes) sont stockés en PAYSAGE** (largeur > hauteur, ≈ 840 × 600 ou 882 × 615), texte à l'horizontale :
  **le serveur les fait pivoter en portrait en les servant** (`ImageLib.TryRotateImage`) et le plateau les
  retourne à l'affichage. **Ne les pré-tourne pas.**
* Les **miniatures** de la table (`assets/vignettes/`, `tools/generer_vignettes.py`) sont **générées** : rien à livrer.
* Les scans de **haute définition** (`/hd/…`) et **français** (`assets/pics-fr/`) ne concernent que le contenu officiel.

**Ton livrable : `integration/images.md`**, un tableau (une ligne par face) :

| `card_id` | Fichier source (nom dans le dossier de l'auteur) | Orientation | Remarque (recto/verso, copie, art alternatif, qualité) |
|---|---|---|---|
| `wd001a` | `Scenarios/Shocker/1A Shocker.png` | portrait | |
| `wd002a` | `Scenarios/Shocker/2A Shock Party.png` | **paysage** | complot principal |

**Une carte en plusieurs exemplaires physiques n'a qu'une image** (celle du `card_id` répété dans les sets).

### 10.2 L'image de la boîte : `assets/textures/sets/<cle_extension>.webp`

Le nom du fichier est **exactement** la `cle_extension` (`21. The Mad Titan's Shadow.webp`,
`120. Custom (Web of Deceit).webp`). C'est elle que l'écran des campagnes affiche en illustration de la boîte
(`/sets/<clé>`). Pour une campagne maison, l'utilisateur fournit la pochette ou une illustration ; indique-le
dans `images.md`. La pochette recadrée (`public/img/prepare/boites/<n>.webp`) est **générée** par
`outils/pochettes-boites.py` : Claude ajoute le rectangle de recadrage.

### 10.3 Le texte français de chaque carte fan-made — **obligatoire à chaque pack**

Un pack livré sans ce texte laisse **toutes ses cartes sans tooltip français, et rien ne le signale**. Le plateau
cherche le français d'une carte dans cet ordre : (1) un scan français (`assets/pics-fr/`) ; (2) le texte officiel
(`textes-fr.ts`, **généré**, ne jamais éditer) ; (3) **`ui-app/src/board/textes-fr-fanmade.ts`**, **écrit à la
main** ; (4) marvelcdb en ligne (coupé par défaut et sans effet sur du fan-made). **Une carte fan-made n'a ni scan
français ni page marvelcdb : la ligne (3) est le seul français que le joueur verra dessus.**

**Ta livraison** : `integration/textes-fr/<pack>.fragment.txt`, **une entrée par `card_id`, y compris pour les
exemplaires en double** (recopie le même texte), au format exact du fichier :

```
  // <pack> — <Nom de la carte> (<Type>)
  '<card_id>': "texte français avec <b>balises</b>, [star], [[TRAIT]]…",
```

**Entrées réelles de Hunting Season** (modèle de forme ; le pack Web of Deceit n'a pas encore ses textes
français : c'est un manque connu) :
{{TEXTESFR:hs|6}}

**Vocabulaire officiel (Guide de référence v1.8 FR) — la gate `vocabulaire-statuts.test.ts` échoue sinon :**

| Anglais | Français | **Interdit** |
|---|---|---|
| Stunned / Confused | Sonné / Désorienté | « étourdi » |
| Tough (carte d'état) / Toughness | carte d'état **Tenace** / **Ténacité** | « Robustesse » |
| Stalwart | **Robuste** | « Inébranlable » |
| Steady | **Solide** | « Stable » |
| Surge / Overkill | Renfort / Déferlement | |
| Piercing / Ranged | Perçant / Distance | |
| Villainous | Vilenie | |
| Incite X / Hinder X | Incitation X / Entrave X | |
| When Revealed | **Une fois révélée** (manigance, traîtrise) | |
| When Defeated (personnage) | **Une fois vaincu** | |
| When Defeated (manigance) | **Une fois déjouée** | |
| Forced Interrupt / Forced Response | Interruption forcée / Réponse forcée | |
| Hero Action / Hero Response / Alter-Ego Action | Action de héros / Réponse de héros / Action d'alter ego | |
| ATK / THW / DEF / REC / SCH | ATQ / CTR / DEF / REC / MNG | |
| counter / token | **jeton** (compteur de carte) ; « pion Accélération » ; « compteur polyvalent » (all-purpose) | |
| stage | stade (« achevé ») | |
| boost / star icon | champ de boost / icône d'étoile | |
| Aggression / Justice / Leadership / Protection | Agressivité / Justice / Leadership / Protection | |
| deck / encounter deck / victory display | deck / deck Rencontre / pile de victoire | |
| exhaust / ready | incliner / redresser | |

* **Noms propres et traits `[[…]]` laissés en ANGLAIS** : le joueur a la carte anglaise sous les yeux.
* **Jetons recopiés tels quels** : `[mental]`, `[physical]`, `[energy]`, `[wild]`, `[star]`, `[per_hero]`,
  `[crisis]`, `[acceleration]`, `[hazard]`, `[amplify]`, `[boost]`.
* Cherche **toujours** comment une phrase équivalente est rendue sur une carte **officielle**
  (`ui-app/src/board/textes-fr-complets.ts`) avant d'écrire la tienne ; les textes d'ambiance (italiques de
  récit) se traduisent comme le reste.
* « est censé(e) » (jamais « devrait ») ; « n'importe quelle quantité de dégâts » ; « perd le texte imprimé dans
  sa boîte de texte » ; « choisissez : soit vous inclinez…, soit vous… ».

### 10.4 Les textes de l'interface de la description de campagne

`resume`, `enjeu`, `libelle`, `aide`, `nom_fr` sont **en français** (ce sont les clés de traduction). Pour
l'interface **en anglais**, l'écran passe ces chaînes à `t()` (dictionnaire français → anglais :
`public/js/prepare/dico-en.js`, `ui-app/src/board/dico-en.ts`). **Une chaîne sans entrée reste en français**
dans l'interface anglaise. Liste, dans `BESOINS-MOTEUR.md`, les chaînes **nouvelles** avec leur traduction
anglaise : Claude les ajoute au dictionnaire.

### 10.5 Biographies (survol dans l'écran de choix)

* **Vilain** — `public/js/prepare/mechants-info.js`, indexé par le **`card_id` de la première face du vilain**
  du scénario (jamais par le nom : plusieurs vilains partagent un nom). Texte sur le **personnage**, jamais sur
  sa mécanique. Tout champ est facultatif sauf `bio`/`bioEn` ; mieux vaut omettre que d'inventer :

```js
"hs001": {
    bio:   "3 ou 4 phrases : origine, pouvoirs, ce qui définit le personnage.",
    bioEn: "Same, in English.",
    civil: "Joseph",
    equipes: "Maggia",       equipesEn: "Maggia",
    ennemis: "Spider-Man",   ennemisEn: "Spider-Man",
    apparition: "The Amazing Spider-Man #113 (1972)",
},
```

  Tu livres `integration/public/js/prepare/mechants-info.fragment.js` (les entrées seules).
* **Héros** — `public/js/prepare/heros-info.js`, indexé par le `card_id` de la **face héros** (même forme + `base`,
  `civilEn`, `baseEn`) ; seulement si la campagne apporte un héros.

### 10.6 Les pages du livret : `public/stories/<code>/`

L'écran affiche le livret en **double page** qu'on tourne. Les pages sont des **images carrées de 975 × 975 px**
(rendues depuis le PDF du livret : les livrets officiels sont des PDF vectoriels aux pages carrées de 540 points,
facteur 1,806). Nommage **par rôle** :

| Fichier | Rôle |
|---|---|
| `00-couverture.jpg` | couverture du livret (page 1 d'un livret officiel) ; à défaut, l'illustration de la boîte |
| `00-campagne-intro-<n>.jpg` | planche d'ouverture de la campagne (référencée par `pages_intro`) |
| `00-campagne-regles-<n>.jpg` | règles générales de la campagne (`pages_regles`) |
| `00-campagne-expert-<n>.jpg` | règles de la campagne experte (`pages_expert`) |
| `<NN>-<scénario>-intro-<n>.jpg` | planche de bande dessinée d'ouverture du scénario `NN` (numéro sur 2 chiffres) |
| `<NN>-<scénario>-regles-<n>.jpg` | page de règles du scénario |
| `<NN>-<scénario>-epilogue-<n>.jpg` | planche de fin (montrée par le panneau après la victoire) |
| `fr/<même nom>.jpg` | la même page **refaite en français** (active si `livret_fr: true`) |
| `00-vilains-<n>.jpg` | portraits des sous-fifres (ordre libre) |

Dans un livret, la page **paire** porte la bande dessinée et la page **impaire** d'en face les règles du même
scénario. Une planche qui termine un scénario **et** ouvre le suivant n'est **pas dupliquée** : elle garde son
nom d'épilogue et le scénario suivant la référence comme intro.

**Ton livrable : `integration/livret-pages.md`**, au format que lit `tools/pages_livret.py` (`CARTES`), qui dit
**quelle page du PDF joue quel rôle** (c'est « le vrai travail » de cet outil) :

```python
"<code>": {
    "pdf": "<fichier du livret>.pdf",
    "regles_campagne": [4, 5],            # pages de règles de la campagne
    "scenarios": [                        # (id, numero, page_intro, [pages_regles], page_epilogue)
        ("ebony_maw", 1, 5, [6, 7], 8),
        ("the_tower_defense", 2, 9, [10, 11, 12, 13], 14),
        ("hs_vermin", 1, None, [4], None),   # pas de planche : le récit et les règles partagent la page
    ],
},
```

**Exemple réel** (Hunting Season, livret fan-made à pages portrait, sans planche de BD) :
{{BLOC:Fusion/marvel-lcg-src/tools/pages_livret.py|"hunting_season": {|"next_evol": {|python}}

Le livret **français** d'une campagne fan-made est refait par `tools/livret_fr.py` à partir d'un fichier de
traductions `tools/livrets_fr/<code>.json` (une entrée par bloc de texte du PDF, `p<page>b<bloc>`) : si tu
traduis le livret, livre ce fichier ; sinon laisse `livret_fr` à `false`.

### 10.7 Le préfixe : `tools/prefixes_fanmade.json`

Fragment à livrer (`integration/tools/prefixes.<pack>.fragment.json`) ; **forme exacte** (entrée du préfixe `hs`) :
{{PREFIXE:hs}}

`cartes` = nombre de **faces** du pack ; `depuis` = date ; `note` = auteur, contenu, particularités.

### 10.8 Crédits

Les **créateurs** sont crédités **automatiquement** par la clé `custom` de chaque carte (§4.2) : filtre
« Fan-made » de l'écran de préparation, pastille CUSTOM du deck-builder, remerciements. **Renseigne `custom` sur
toutes les cartes, faces d'identité comprises.** Livre en plus `integration/CREDITS.md` : l'auteur de la
campagne (nom exact et pseudonyme), l'équipe (organisateurs, développeurs, testeurs, traducteurs, éditeur du
livret français), le lieu et la date de l'événement s'il y en a un, et les **illustrateurs** imprimés sur les
cartes. Claude les place dans les remerciements du jeu.

### 10.9 Ce que tu **n'écris pas** dans cette chaîne

Les checksums de `cards.json`/`sets_info.json` ; les vignettes ; les scans HD/FR ; `textes-fr.ts` ;
`public/js/traduction/*` (générés) ; `dico-en` ; `data/translate_fr.json` (narration du moteur, traduite par
gabarit) ; l'éditeur de pochettes ; les hauts faits.
