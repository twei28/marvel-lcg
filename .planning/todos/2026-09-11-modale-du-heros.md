# Modale du héros : un seul héros par tuile, ses variantes dans une modale

**Idée de l'utilisateur, 11/09/2026**, cadrée en quatre questions une à une.
**À faire après la clôture de Hellcat et le déploiement** (sa décision).
Premier cas concret : les deux entrées Hellcat (Iron Man / Miss Hulk) et les
deux Superior Spider-Man.

## Ce qui est décidé

| Question | Réponse |
|---|---|
| Contenu de la modale | **Tout** : identité alternative (The Thing Guardian, les deux alter ego de Superior Spider-Man), allié signature alternatif (Hellcat), art alternatif, ressources de base |
| Le bloc « cosmétiques » de la page de préparation | **Disparaît** : la modale seule décide. Le héros sélectionné affiche un rappel (« Iron Man · art classique ») et un bouton « Modifier » qui rouvre la modale |
| Mémoire | **Le dernier choix fait pour ce héros** sur cet appareil ; la modale s'ouvre quand même, pré-remplie |
| Héros sans aucune option | Tranché seul : lancement direct, pas de modale vide |

## Ce qui existe déjà, à réunir

- `metadata.hero_alts` du deck de départ (`the_thing.json`, `viv_vision.json`) :
  identité alternative, lue par `catalog.js:83` (`identites`) et
  `app.js:1863` (`blocIdentiteHeros`).
- `blocArtHeros(p.hero)` (art alternatif) et `blocRessources(p.hero)`
  (ressources de base) : `app.js:2334`, dans `cosmetiques`.
- **Variantes de deck = deux fichiers** aujourd'hui : `hellcat.json` /
  `hellcat_she_hulk.json` (même identité), et Superior Spider-Man (deux
  identités). `catalog.heroes()` construit la liste des héros à partir de
  `deck/starter/*.json` : deux fichiers = deux tuiles.

## Piste de mise en œuvre (à confirmer au moment de faire)

1. **Un seul fichier par héros**, avec un bloc `metadata.variantes` :
   `identites` (déjà `hero_alts`), `allies_signature` (`[{nom, remplace,
   par}]` : `hc002` → `hc012`), `arts`, `ressources`. `hellcat_she_hulk.json`
   disparaît ; le moteur reçoit un deck **résolu** par le lanceur (hero_deck
   avec la carte substituée), rien à changer côté moteur.
2. `catalog.heroes()` : une tuile par fichier, plus par variante.
3. Modale au clic sur la tuile : sections présentes seulement si le héros a
   l'option ; sinon lancement direct.
4. Mémoire : `localStorage` clé `variantes:<hero_id>`.
5. Rappel + bouton « Modifier » à la place des trois blocs cosmétiques.
6. Tests : catalogue (une tuile par héros), résolution du deck (Hellcat →
   hc012 remplace hc002), mémoire, et un cas « héros sans option ».

## Pièges à garder en tête

- `sets_info.json` liste `heroes: ["hellcat", "hellcat_she_hulk"]` : à
  ramener à un seul nom.
- Le harnais et `verifier_tous_les_decks.py` montent les decks par fichier :
  une variante doit rester **montable** (un cas par variante, résolu à la
  main dans le test).
- L'entrée `heros-info.js` est indexée par la face héros (`hc001a`) : une
  identité alternative purement cosmétique ne doit pas en créer une seconde
  (PROCESSUS-HEROS, étape 7).
