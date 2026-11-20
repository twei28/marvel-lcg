# Setlist

> **Mise à jour du 20/10/2026 (backlog 12).** `Concert()` passait son filtre
> de joueur en `check_effect_fn` à `Worlds.FindCardOnField`, qui ne l'appelle
> jamais : la fonction rendait la Live Concert de n'importe quel joueur. Le
> filtre est maintenant fait à la main (même correctif pour `AngoisseEnJeu`,
> qui reconnaît l'obligation à la ZONE d'obligations du joueur : son
> propriétaire reste le scénario). La Hero Action de Live Concert n'est plus
> offerte quand la Setlist est vide (blocage du pilote d'autoplay).
> `JoueurDeDazzler()` désigne la Setlist de DAZZLER pour les cartes qui la
> nomment (`dz022` Stealing Sound). Les compteurs `sound` partent avec les
> cartes à CHAQUE vidage de la Setlist (Showtime!, Karaoke Night, Stealing
> Sound).

**Texte imprimé / définition** : « Setlist » désigne, dans le pack maison
`dazzler` (héroïne custom **Dazzler**, contenu de « Lord Havok »), la zone
de jeu créée par l'upgrade permanent **Live Concert** (`dz017a`) où
s'accumulent les événements de trait [[SONG]] joués. Le mot « Setlist »
n'apparaît pas littéralement dans le texte imprimé de `dz017a` : « Response:
After you resolve a [[SONG]] event attach it here, placed in a row to the
side of this card (to a maximum of 4). Once placed here, it cannot be
swapped with a new card. Hero Action: Flip this card to its Showtime! side
and reveal it. » « Setlist » est le nom donné par le pack, et repris dans le
code (commentaire de tête du fichier central : « Tout le set tourne autour
d'une zone, la SETLIST »), à cette zone à 4 emplacements, plutôt qu'un
mot-clé imprimé verbatim sur une carte.

**Mécanisme moteur** : composé dans
`Fusion/marvel-lcg-src/src/cards/pack/dazzler/dazzler/__init__.py`. Ce
fichier n'existe ni dans ce worktree ni dans l'historique git de ce dépôt
(vérifié lors de cette tâche : absent de `master` et de toutes les branches
accessibles via `git log --all`). Son contenu ci-dessous a été lu
directement par l'agent coordinateur dans le checkout original
`/mnt/c/Users/arnau/Desktop/Marvel LCG/` (hors
du périmètre de ce worktree) et transmis verbatim ; il n'a pas été relu de
façon indépendante par l'agent qui rédige cette fiche.

```python
def Concert(effect, joueur=None):
    """Live Concert en jeu, quelle que soit sa face (Live Concert / Showtime!),
    chez le joueur courant."""
    # cherche par nom, les deux faces de la meme carte physique

def Setlist(effect, joueur=None) -> list:
    """Les [[SONG]] actuellement dans la Setlist (zone PlaceCardArea de
    Live Concert), dans l'ordre de pose."""
    concert = Concert(effect, joueur)
    if concert is None: return []
    zone = concert.GetPlacedCardArea()
    if zone is None: return []
    return list(zone.Get(True))

def SetlistALaPlace(effect) -> bool:
    """« to a maximum of 4 » : la Setlist accepte-t-elle une carte de plus ?"""
    return len(Setlist(effect)) < 4  # PLACES_SETLIST = 4
```

`Setlist()` s'appuie sur `Concert()` pour retrouver Live Concert en jeu
(quelle que soit sa face, Live Concert ou Showtime!, chez le joueur
courant, recherché par nom), puis lit sa `PlaceCardArea` (zone de cartes
attachées) via `GetPlacedCardArea()` et rend la liste des cartes qui s'y
trouvent (`zone.Get(True)`), dans l'ordre de pose. Si Live Concert n'est
pas en jeu, ou si sa zone est absente, `Setlist()` rend une liste vide.

La pose dans la zone est gérée par `dz017a` lui-même, pas par la fonction
`Setlist()` : sa capacité Response (`ranger_dans_la_setlist`, voir Carte
exemple) attache l'événement [[SONG]] résolu via
`this.PlaceCardHere([chanson], True, effect)` (face visible), sous
condition `SetlistALaPlace(effect)` (`len(Setlist(effect)) < 4`), la limite
de 4 emplacements imprimée sur la carte (« to a maximum of 4 »). La limite
est donc imposée côté condition de pose, pas par une limite native de
`PlaceCardArea`.

La sortie de la Setlist se fait par le retournement de Live Concert sur sa
face Showtime! (`dz017b`) : mécanisme traité par le mot-clé Showtime! (voir
`showtime.md`), pas par Setlist lui-même.

**Carte exemple** : `dz017a` (Live Concert, upgrade permanent recto),
extrait de `dz017a.py`, transmis par le coordinateur :

```python
def GetAbilities():
    def ranger_dans_la_setlist(effect, message):
        this = effect.this.CastTo(Upgrade)
        chanson = message.played_face
        if chanson is None: return
        this.PlaceCardHere([chanson], True, effect)  # FACE VISIBLE

    def lever_le_rideau(effect, message):
        joueur = effect.GetInitiator()
        Faces.FlipAllTo(effect.targets, None, effect)
        for face in effect.targets:
            montree = face.card.face
            if montree is not None and montree.IsInPlay():
                montree.Reveal(joueur, effect, is_by_flipping=True)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.AfterPlayerPlayedCard(
            AbilityType.Response, "You",
            CardFinder(card_type=Event, trait=TRAIT_SONG),
            ranger_dans_la_setlist,
            conditions=[lambda effect, message: SetlistALaPlace(effect)],
        ),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction, lever_le_rideau,
            conditions=[lambda effect, message: not AngoisseEnJeu(effect)],
        ).SetTarget("This"),
    ]
```

`AngoisseEnJeu`, condition de la Hero Action de retournement, n'a pas été
expliquée par le coordinateur ni lue par l'agent rédacteur : ne pas
supposer son comportement, à vérifier sur pièce avant de s'appuyer dessus.

**Pièges connus** : « Setlist » n'est pas un texte imprimé verbatim sur les
cartes, contrairement à « Showtime! » qui l'est : c'est le nom donné par le
pack et par le code à la zone `PlaceCardArea` de Live Concert. Ne pas
chercher le mot « Setlist » dans `cards.json` en espérant une
correspondance de texte de carte. La limite de 4 emplacements est une
condition de script (`SetlistALaPlace`), pas une propriété native de la
zone : une carte hypothétique qui poserait directement dans cette zone sans
passer par cette condition ne serait pas bornée par ce mécanisme (aucune
autre carte du pack ne le fait, d'après le fichier central transmis).

**Variantes maison** : aucune connue au 29/08/2026, hors le pack `dazzler`
lui-même.
