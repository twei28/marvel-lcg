# Showtime!

**Texte imprimé / définition** : mot-clé maison du pack `dazzler` (héroïne
custom **Dazzler**, contenu de « Lord Havok »), imprimé littéralement comme
titre de seconde capacité sur les événements de trait [[SONG]] du pack,
après leur « Hero Action ». Texte exact transmis pour `dz003` (* A Little
Girl's Dream) : « Hero Action: Reduce the resource cost of the next ally or
event you play this round by 3. Showtime!: Confuse a non-[[ELITE]] enemy. »

**Mécanisme moteur** : composé dans le même fichier central
`Fusion/marvel-lcg-src/src/cards/pack/dazzler/dazzler/__init__.py`, absent
de ce worktree et de l'historique git de ce dépôt (vérifié lors de cette
tâche). Contenu ci-dessous lu directement par l'agent coordinateur dans le
checkout original `/mnt/c/Users/arnau/Desktop/Marvel LCG/` et
transmis verbatim ; non relu de façon
indépendante par l'agent qui rédige cette fiche.

```python
def Showtime(operation: Any) -> 'Ability':
    """La seconde capacite d'un [[SONG]], celle qui n'agit que dans la Setlist.

    Elle n'est jamais declenchee par un message : `jamais` la verrouille, et
    seule `ResoudreShowtime` sait l'atteindre. `NoOutOfPlayLimit` est
    indispensable : la carte vit dans la Setlist, que le moteur ne compte pas
    comme « en jeu ».
    """
    def jamais(effect: 'Effect', message: 'Message2') -> bool:
        return False

    return Ability(
        AbilityType.Special,
        Message.WhenCardRevealed,
        [jamais],
        operation,
    ).SetName(NOM_SHOWTIME).NoOutOfPlayLimit()


def ResoudreShowtime(faces, player, effect) -> int:
    """Resout le « Showtime! » de chaque carte donnee. Rend le nombre resolu."""
    return Faces.ResolveAbility(faces, player, AbilityType.Special, effect)
```

`Showtime(operation)` construit une `Ability` nominalement accrochée au
message `Message.WhenCardRevealed`, mais dont l'unique condition, `jamais`,
renvoie toujours `False` : elle ne peut donc jamais se déclencher d'elle-même
par ce message. Le commentaire de tête du fichier central explique le
choix : le moteur sait déjà résoudre une capacité d'un type donné sur une
autre carte via `Faces.ResolveAbility(faces, player, ability_type, effect)`
(déjà utilisée par des cartes officielles citées dans ce commentaire :
Quatre Cavaliers `45090`, Celestial Tech `45158`) ; il fallait donc un type
de capacité libre, qu'aucune autre carte du jeu n'utilise.
`AbilityType.Special` répond à ce besoin : déclaré, doté de ses flags
(`ui_display_name`, donc son nom s'affiche), absent de `TYPE_PRIORITY` (qui
a un défaut) mais non utilisé par aucune autre carte du jeu selon le même
commentaire, donc réquisitionnable sans modification du moteur commun.
`.NoOutOfPlayLimit()` est nécessaire parce que la carte, une fois dans la
Setlist (zone `PlaceCardArea` de Live Concert, voir `setlist.md`), n'est
plus comptée « en jeu » par le moteur, ce qui bloquerait sinon la
résolution d'une capacité à limite d'utilisation par tour/partie.

`ResoudreShowtime(faces, player, effect)` est l'unique point d'entrée
capable de déclencher effectivement ces capacités : il appelle
`Faces.ResolveAbility(faces, player, AbilityType.Special, effect)` sur la
liste de cartes passée, et rend le nombre de capacités résolues. Le
commentaire de tête du fichier central décrit le point d'appel prévu pour
l'ensemble de la Setlist : la Hero Action de Live Concert retourne la carte
sur sa face Showtime! (`dz017b`), dont le texte imprimé transmis dit
« When Revealed: Resolve the "Showtime!" ability on each card in the
Setlist, in any order. Then, discard all cards from the Setlist. If 4 cards
were discarded this way, you may either... ». Le script `dz017b.py`
lui-même (l'appel effectif attendu, du type
`ResoudreShowtime(Setlist(...), ...)`) ne m'a pas été transmis : seuls le
commentaire de conception du fichier central et le texte imprimé de la
carte confirment ce point d'entrée, pas une lecture directe de
`dz017b.py`. À vérifier sur pièce avant de s'appuyer dessus pour une
fiche future.

**Carte exemple** : `dz003` (* A Little Girl's Dream, Event, trait SONG),
script complet transmis par le coordinateur :

```python
from . import *

def GetAbilities():
    def reve(effect, message):
        this = effect.this.CastTo(Event)
        joueur = effect.GetInitiator()
        if joueur is None: return
        Worlds.UpdateNextCardPlayCost(
            joueur, -3, effect,
            finder=CardFinder(card_type=Ally | Event),
            in_this="Phase",
        )

    def showtime(effect, message):
        this = effect.this.CastTo(Event)
        Faces.GiveStatus(CiblesShowtime(effect), "Confused", effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(AbilityType.HeroAction, reve).SetPlay().SetLabel(),
        Showtime(showtime).SetTarget(Enemy, non_trait="ELITE", canbe_confused=True, range=(0, 1)),
    ]
```

La capacité Showtime! est construite par `Showtime(showtime)`, ciblée sur
un ennemi non-[[ELITE]] confusable (`.SetTarget(Enemy, non_trait="ELITE",
canbe_confused=True, range=(0, 1))`), et son opération applique le statut
Confused via `Faces.GiveStatus(CiblesShowtime(effect), "Confused",
effect)`.

**Pièges connus** : `CiblesShowtime` (helper cité dans le brief de tâche
mais dont le corps ne m'a pas été transmis) existe précisément parce que le
chemin normal du moteur, `CardFace.ResolveAbility` (appelé en interne par
`Faces.ResolveAbility`), prend automatiquement la première cible légale
sans rien demander au joueur : pour une capacité Showtime! avec cible comme
celle de `dz003`, ce comportement par défaut empêcherait un vrai choix.
`CiblesShowtime` sert à forcer ce choix. Toute future carte Showtime! avec
cible doit passer par ce helper plutôt que reconstruire un ciblage manuel,
sous peine de retomber dans ce défaut moteur (ciblage automatique, sans
choix). Deuxième piège : ne pas chercher `AbilityType.Special` en lui
prêtant un sens générique dans le moteur, c'est un type autrement inutilisé
par le jeu, réquisitionné spécifiquement par ce pack pour verrouiller
Showtime! contre tout déclenchement accidentel via
`Message.WhenCardRevealed`. Enfin, le mécanisme d'appel final sur
l'ensemble de la Setlist (`dz017b.py`) n'a pas été lu, seulement inféré du
texte imprimé et du commentaire de conception : à confirmer avant de
documenter le retournement de Live Concert lui-même dans une fiche future.

**Variantes maison** : aucune connue au 29/08/2026, hors le pack `dazzler`
lui-même. `dz003` est la seule carte Showtime! avec ciblage lue en détail ;
le pack en compte d'autres (40 cartes au total d'après la mémoire de
session du projet) qui portent vraisemblablement des opérations
`Showtime()` différentes, non vérifiées ici.
