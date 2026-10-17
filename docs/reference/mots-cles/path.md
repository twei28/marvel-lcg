# Path (la Voie) : type de carte, mise en jeu au Setup, « -1 hand size »

**Texte imprimé / définition** : type imprimé **PATH** (« Shinobi Path »), carte **Permanent**, « You get -1 hand size ».
Le livret : « During deck-building, select a Shinobi Path card [...] Make sure to put your Path card into play during
setup. [...] Path cards are not support cards. » Onze Paths dans `tmnt_shinobi_paths` (se001-se011) ; un douzième, le
Sosaiken de Jennika (`tj011`), est la Voie PROPRE d'un héros.

**Mécanisme moteur** :
- Type : `card_type/path.py` (créé pour `tj011`, 16/10/2026) : rangé dans l'aire de soutien du joueur, invisible aux effets
  « Support ». `Permanent` : `desc.Permanent = "1"`, aucun script (`permanent.md`).
- **Un Path choisi au deck-building** (le deck-builder le place dans `player_deck`) : `PlayerSetup.SelectIdentity` retire de la
  liste du deck tout card_id de type Path (`EstUnPath`), le fabrique dans la réserve du joueur (`additional_discard_pile`) et
  le met en jeu SOUS SON CONTRÔLE à `WhenGameBeginSetup` (`RunAt.WhenGameBeginSetup`), pour n'importe quel héros, AVANT la
  pioche de départ : la main de départ tient déjà compte du -1. Le Path n'est donc jamais mélangé ni en main.
- **Un Path propre à un héros** (Sosaiken) : `BeginGameWithSetAside(['tj011'], op)` dans le Setup de l'alter-ego (modèle
  Ionic Physiology) ; son entrée est `set_aside` dans le deck de départ, pas dans `player_deck`.
- **« You get -1 hand size »** : `*GiveKeywordToInPlayWhenApplyThis("You", hand_size=-1)` (modèle `04165` Martial Law,
  `st005b`) ; `"You"` = les deux formes de l'identité.
- **Classe d'un Path** : `desc.Class` = ses types Shinobi (`"Ninjutsu"`, `"Bushido;Kuji-Kiri"`...), traits imprimés = ces types
  en majuscules (NINJUTSU...) ou SENPAI (Last Ronin). Le deck-builder en déduit les types autorisés ; `data/shinobi_paths.json`
  porte le reste (aspects, plafonds).
- **Deck-builder** : `paths-shinobi.js` / `regles.js` : Path obligatoire pour toute carte Shinobi, UN seul Path, types du Path,
  un aspect (Last Ronin : libre, 1 exemplaire de toute carte), Basic permis, Path hors des 40-50 (Permanent). Un héros qui
  porte sa Voie propre le déclare dans `metadata.deckbuilding.path` de son deck de départ (Jennika) et n'en choisit pas
  d'autre.

**Carte exemple** : `se001` Kagemusha (Hero Action), `se005` The Last Ronin (tuck), `tj011` Sosaiken (Path propre).

**Pièges connus** :
- l'identifiant `seNNN_dos` désigne un DOS de Path (insert de règles, aucune carte jouable, jamais dans `cards.json`) ;
- un Path ne se déplace pas d'un effet d'un autre set (Permanent, `has_permanent.py`) ;
- `Puzzle.PutIntoPlay('seNNN', under_control=True)` met un Path en jeu dans un cas de test ; le chemin réel se prouve avec la
  clé de cas `deck_ajoute` ;
- lecture littérale du livret : AUCUN Path n'est réservé aux héros TMNT (question Q-S3).

**Variantes maison** : le type et le système sont maison.
