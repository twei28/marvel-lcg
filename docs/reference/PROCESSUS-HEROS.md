# Processus : un nouveau héros, du début à la fin

Étapes propres au héros. Chaque carte du pack passe en plus par
`PROCESSUS-CARTE.md` en entier : ce fichier ne duplique pas ses 8 étapes.

> **Aller plus vite SANS rien sauter** : `docs/reference/RECETTES-MOTEUR.md`
> donne, mécanique par mécanique, la fabrique, la carte modèle et le piège
> déjà payé (son §9 liste le chemin outillé complet avec les durées :
> `[filtre]` des cas, `substituer_pack.py`, `DECK_NOM`, règle de portée).
> Toutes les gates restent dues — c'est le chemin vers chacune qui est
> raccourci. Référence : harry_osborn (18 cartes, 26 cas, 17 substitutions)
> a tenu en une demi-journée le 31/08/2026 avec ces outils.

## Étape 1 : Cartes dans `data/cards.json`

Pack du produit, `set_name` = nom du héros :
- `XXXXXa` type `Hero` (`HP/ATK/THW/DEF/HS`) et `XXXXXb` type `AlterEgo`
  (`HP/REC/HS`) : même carte, deux faces ;
- les ~15 cartes signature ;
- 1 obligation (`desc.GiveTo` = nom de l'alter-ego) ;
- 5 cartes némésis (`set_name` = `"<Héros> Nemesis"`).

## Étape 2 : Scripts

Pour chaque carte à capacités, y compris les faces a/b du héros (capacités
imprimées ; ATK/THW/DEF/REC de base sont automatiques).

## Étape 3 : Deck de départ

`deck/starter/<hero>.json` :
```json
{ "version": "0.5.8", "name": "Mon Héros", "metadata": {"url": ""},
  "hero": ["XXXXXa,XXXXXb"],
  "hero_deck": ["...15 cartes..."],
  "set_aside": [],
  "obligations": ["..."],
  "nemesis_set": ["...5 cartes..."],
  "player_deck": ["...~25 cartes d'aspect..."] }
```

⚠ `set_aside` ne sert qu'aux clients (catalogue, lanceur) : le moteur ne lit
pas ce champ en vraie partie (`HeroDescriptor` ne l'a pas, la génération est
en commentaire dans `player_setup.py`). Une carte mise de côté au setup doit
être créée par le héros lui-même, `AbilityFactory.BeginGameWithSetAside([...])`
sur l'alter-ego (modèles bt001b, 09001b, al001b). Le harnais la fait exister
avec `Puzzle.CreatePlayerAdditionalDeck`, ce qui laisse un cas vert pour une
carte absente en jeu réel : ne pas s'y fier (Alligator Loki, 01/09/2026).

## Étape 4 : `data/nemesis/<hero>_nemesis.json`

Facultatif, pour l'UI.

## Étape 5 : Référencer dans `data/sets_info.json`

Dans `heroes` du bon pack.

## Étape 6 : Images

`assets/pics/<card_id>.jpg` pour toutes les cartes (extension obligatoire,
voir §4 de `GUIDE-CREATION-CONTENU.md`).

## Étape 7 : Biographie *(case à cocher avec preuve, pas une ligne qu'on oublie)*

Le wizard affiche, au survol du héros, une fiche qui décrit le personnage
(voir `showHeroHover` dans `public/js/prepare/app.js`) : c'est de la culture
Marvel, jamais sa mécanique de jeu.

Ajouter une entrée dans `public/js/prepare/heros-info.js`, **indexée par le
`card_id` de la face héros** et jamais par le nom (`01001a` Peter Parker et
`27030a` Miles Morales s'appellent tous les deux « Spider-Man ») :

```js
"ht001a": {
    bio:   "3 ou 4 phrases : origine, pouvoirs, ce qui définit le personnage.",
    bioEn: "Same, in English.",
    civil: "Johnny Storm",
    base: "New York (Baxter Building)",
    equipes: "Quatre Fantastiques, Vengeurs",
    equipesEn: "Fantastic Four, Avengers",
    ennemis: "Fatalis, l'Homme-Taupe",
    ennemisEn: "Doctor Doom, Mole Man",
    apparition: "Fantastic Four #1 (1961)",
},
```

Règles : tout champ optionnel sauf `bio`/`bioEn` (mieux vaut omettre que
d'inventer ; un champ absent disparaît simplement de la fiche) ; les `*En`
seulement si la traduction diffère (« New York » ou « Thanos » se passent
de doublon, en anglais un `*En` absent affiche la version française) ;
**`civilEn` et `baseEn` existent aussi** (`app.js:1068-1069`), même si le
gabarit ci-dessus ne les montre pas — utile pour « Institut Xavier » /
« Xavier Institute » (constaté au portage `bt001a`, 31/08/2026) ;
viser 3-4 phrases (panneau étroit, 314 px) ; libellés affichés via `t()`
dans `public/js/prepare/dico-en.js` (voir §11 de `GUIDE-CREATION-CONTENU.md`).
Ce fichier vit hors du dépôt du moteur : on l'édite directement dans la copie
vivante, il n'y a aucune recopie à faire (voir §1.3 de
`GUIDE-CREATION-CONTENU.md`).
Un héros sans entrée retombe silencieusement sur l'ancien affichage :
rien ne casse, mais la fiche manque, donc **preuve obligatoire** = confirmer
au survol du héros dans le wizard que le panneau affiche bien le texte
attendu, pas juste le grand visuel seul.

Ne pas ajouter de biographie pour une identité alternative purement
cosmétique (voir Étape 10 ci-dessous) : le panneau s'indexe sur la face du
deck de base, une entrée pour la variante resterait orpheline.

## Étape 8 : Texte français de chaque carte *(obligatoire)*

`ui-app/src/board/textes-fr-fanmade.ts` (voir §11.1 de
`GUIDE-CREATION-CONTENU.md`). Sans lui, les cartes du pack n'ont aucun
tooltip français, et rien ne le signale.

## Étape 9 : Validation, carte par carte

`PROCESSUS-CARTE.md` en entier pour **chaque** carte du pack (pas seulement
les cartes signature), plus une partie complète jouée avec le héros.

## Étape 10 : Points d'attention transverses

**Jamais une carte signature d'un autre héros dans un deck.** Une carte de
classe `Hero` (`desc.Class = "Hero"`) appartient à un seul héros. Le moteur
ne valide PAS les decks de départ au chargement : le contrôle doit être fait
à la main.

```bash
cd "$W" && python3 - <<'EOF'
import json, glob, os
d = json.load(open('data/cards.json'))
cl = {c['card_id']: (c.get('name',''), c.get('desc',{}).get('Class',''), c.get('set_name',''))
      for p, cs in d.items() if p != 'checksum' for c in cs
      if isinstance(c, dict) and c.get('card_id')}
for f in sorted(glob.glob('deck/starter/*.json')):
    dk = json.load(open(f))
    hero_set = cl.get(dk['hero'][0].split(',')[0], ('','',''))[2]
    for cid in dk.get('player_deck', []):
        n, classe, setn = cl.get(cid, ('?','?','?'))
        if classe == 'Hero' and setn != hero_set:
            print(os.path.basename(f), '->', cid, n, '(set', setn + ')')
EOF
```

**Identité alternative (art alternatif)** : ne pas créer un deuxième deck de
départ. Déclarer la variante dans `metadata.hero_alts` du deck existant.
Détail complet : `GUIDE-CREATION-CONTENU.md` §5.3 (inchangé, conservé là-bas
pour ne pas dupliquer le mécanisme `catalog.heroes()` / `blocIdentiteHeros()`).

## Gate finale

**Héros terminé** exige :
- [ ] Étapes 1 à 8 complètes
- [ ] Un `PROCESSUS-CARTE.md` rempli et « Carte terminée : OUI » pour
      **chaque** carte du pack (lister les card_id)
- [ ] **`tools/verifier_tous_les_decks.py` relancé, et le deck du nouveau
      héros au vert** *(ajouté le 03/09/2026)*
- [ ] Une partie complète jouée avec le héros

> ### ⚠ POURQUOI `verifier_tous_les_decks` EST UNE GATE (leçon `ls005`, 3/9/2026)
>
> `factory.py` pose des **asserts de construction** qu'aucun autre outil ne
> déclenche : un événement à deux capacités `Play` (un « Choose one », ou une
> Action civile + une Action héros sur la même carte) doit être **déclaré dans
> une liste blanche**, sinon la partie plante **au setup**.
>
> `test_cards` ne monte pas de partie. `test_capacites` et `substituer_pack`
> ne montent que les positions écrites à la main, qui n'exercent pas la
> construction du deck complet. **Seul `verifier_tous_les_decks` l'attrape.**
>
> Mesuré : le deck `lady_sif` était **injouable depuis son portage de la
> veille**, ses gabarits cochés, ses 22 cas verts et ses 18 cartes prouvées
> par substitution. Le pack suivant l'a découvert par hasard.

Pas de héros à moitié validé : si une seule carte du pack manque son
« Carte terminée : OUI », le héros entier reste NON.
