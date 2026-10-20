
---

## 11. Les pièges déjà payés, classés — **lis-les avant d'écrire**

Chaque ligne est une erreur qui a déjà coûté du temps sur ce projet. Les pièges **communs** aux campagnes et aux
héros (données, scripts, textes, méthode) sont repris en fin de chapitre, tels qu'ils figurent dans le manuel de
campagne (annexe L).

### 11.1 Le deck de départ et l'extension

| Piège | Ce qui se passe | Parade |
|---|---|---|
| Pas de `deck/starter/<héros>.json` | le héros n'apparaît **nulle part**, pas même dans le deck-builder | toujours écrire le fichier, avec ce qui est imprimé |
| `player_deck` composé par l'IA pour un héros maison | 33 decks « générés » ont dû être vidés le 12/09/2026 | vide, sauf decklist de l'auteur citée dans `metadata.note` |
| Carte signature d'un autre héros dans un deck | le moteur ne valide pas : la carte entre dans la partie | contrôle de classe `Hero` + `set_name` (le vérificateur le fait) |
| `set_aside` rempli dans le deck | **ignoré** en vraie partie ; un cas de test vert peut cacher une carte absente en jeu réel | `BeginGameWithSetAside` sur l'alter ego (§6.4) |
| Bio ou réplique indexée par le **nom** | « Spider-Man » désigne **trois** héros (`01001a`, `27030a`, un troisième) | bio : `card_id` de la face héros ; réplique : id du deck |
| Variante d'un deck sans `variante_nom` sur la base | la modale du héros ne replie pas la variante | `variante_nom` **des deux côtés** |
| Un deuxième deck de départ pour une identité alternative | un deuxième héros apparaît dans la grille | `metadata.hero_alts` (§5.3) |
| Règle de deck-building non déclarée | le moteur ne la connaît pas, le deck-builder laisse tout passer | `metadata.deckbuilding` + `deckbuilding_note` |
| Set némésis emprunté sans le dire | les cartes qui cherchent « le sbire némésis » ne trouvent pas le bon | `metadata.nemesis_note`, et un sbire marqué `desc.Nemesis` |
| `sets_info.heroes` oublié ou faux | le héros n'est dans aucune extension | `heroes: ["<id du deck>"]`, `scenarios` et `encounters` vides |
| Total de `hero_deck` ≠ 15 sans explication | en général une carte oubliée ou un exemplaire de trop | recompte sur les images ; sinon `QUESTIONS.md` |

### 11.2 Les cartes

| Piège | Ce qui se passe | Parade |
|---|---|---|
| Icône de ressource lue à vue | « ressource os » inventée sur Lockjaw : 4 cartes fausses cinq jours | comparer à une carte connue du même pack ; sinon question |
| `desc.GiveTo` = nom du héros au lieu de l'alter ego | l'obligation n'est pas donnée au bon joueur | nom de l'**alter ego**, sans étoile |
| `custom` absent d'une face d'identité | le créateur ne s'affiche pas | sur **toutes** les faces |
| Valeur de `desc` en nombre | refusé / mal lu | chaînes partout |
| `Uses` avec un compteur inconnu | **assertion à la construction** : la carte ne se construit pas | `reference/compteurs.json`, sinon `BESOINS-MOTEUR.md` **avant tout** |
| Trait inconnu de la liste typée | aucun effet à l'exécution | à signaler tout de même (`BESOINS-MOTEUR.md`) |
| Texte avec « Uses (3 counters) » mais `desc.Uses` absent | la carte entre sans compteur, l'action reste grisée | `desc.Uses: "3,<compteur>"` |
| `Victory` à `"0"` | la carte va quand même dans la pile de victoire | ne l'écris que si imprimé |
| Face héros sans les cinq stats ; alter ego avec ATK/THW/DEF | stats absentes ou parasites | face héros : HP ATK THW DEF HS ; alter ego : HP REC HS |
| Complot annexe de némésis en portrait | image tournée à l'envers | les complots annexes sont **paysage** (le serveur tourne l'image) |

### 11.3 Les scripts

| Piège | Ce qui se passe | Parade |
|---|---|---|
| Fonction ou clé inventée | la carte se construit et ne fait rien, **sans erreur** | annexe I ; aucune fabrique qui n'y est pas |
| `from . import *` absent / dossier de set sans `__init__.py` | toutes les cartes du set muettes | contrôlé par le vérificateur |
| Script dans le mauvais dossier | muet | `<pack>/<set_nettoyé>/<id>.py` |
| `CardFinder(name="* Carte")` | ne trouve **jamais** rien | le nom **sans** l'étoile |
| `CardFinder(trait=…)` sans `card_type` | assertion à la construction | toujours les deux |
| `WhenCardSetup` à **un** argument | la capacité ne fait rien | `("This", op)` |
| « Hero » écrit `"You"` dans un bonus continu | contre-cas alter ego faux | le nom de la face : `Hero` |
| « Limit once per round » oubliée | la capacité se répète | `LimitOncePerRound()` + témoin d'épuisement |
| Fabrique d'un modèle qui a **le même défaut** | `an001a` copiait `vp001a`, qui avait déjà une limite muette | une carte modèle se vérifie par un test, pas par ressemblance |
| `GetAbilities()` vide « parce que la carte est simple » | une capacité imprimée sans effet | `# A_FAIRE_CLAUDE:` ou un script réel |
| « play a card » écrit comme « put into play » | la capacité se déclenche pour les cartes mises en jeu | deux accroches différentes |
| Compteur « here » posé ailleurs que sur l'identité | le décompte ne se voit pas, la cible est fausse | `CostFunc.Counter("YourIdentity", n, '<compteur>')` |
| Un jeton de forme : que devient-il au retournement ? | décision de règle | le Rules Reference : le personnage **garde** dégâts, statuts, attachements, **jetons**, état prêt/épuisé |

### 11.4 Les tests

| Piège | Ce qui se passe | Parade |
|---|---|---|
| Cas qui s'arrête avant le point de rupture | le moteur **avale** l'exception ; 338 occurrences invisibles par fournée | le cas mesure **tout** ce que la carte annonce |
| `main_exclusive` défausse la main **après** la mise en place | une défausse préparée pour le cas est vidée | la poser dans `declencher` |
| Cas d'une carte « mise de côté » vert, carte absente en jeu réel | `Puzzle.CreatePlayerAdditionalDeck` fait exister la carte | vérifier le `BeginGameWithSetAside` du script |
| Pilote qui joue une carte du deck et fausse la mesure | Moxie donnait +1/+1/+1 et sauvait trois cas | écrire la ligne de base dans le cas |
| Un deck « prouvé » mais injouable (`lady_sif`) | assert de construction non exercé | **`verifier_tous_les_decks`** est une gate |
| Une gate qui répond OK sans avoir jamais échoué | aucune information | la voir échouer une fois |

### 11.5 Textes et habillage

| Piège | Ce qui se passe | Parade |
|---|---|---|
| Aucun texte français | aucun tooltip français, rien ne le signale | `textes-fr/<pack>.fragment.txt`, une entrée par `card_id` (doublons compris) |
| « Robustesse », « Inébranlable », « étourdi »… | la gate `vocabulaire-statuts` échoue | tableau du §7.1 |
| Biographie qui décrit la mécanique | hors sujet | le personnage seulement |
| Réplique **traduite** ou inventée | ce sont des répliques de comics / films | telles quelles, en anglais ; sinon demander |

### 11.6 Pièges communs aux campagnes et aux héros (extrait du manuel de campagne, annexe L)

Les renvois `§N` de cet extrait renvoient au **manuel de campagne** (annexe L), pas à ce manuel.

{{SECTION:docs/kit-campagne-ia/KIT-CAMPAGNE-COMPLET.md|### 14.1 Données|### 14.3 Logique|3}}

{{SECTION:docs/kit-campagne-ia/KIT-CAMPAGNE-COMPLET.md|### 14.4 Textes, images|## 15.|3}}
