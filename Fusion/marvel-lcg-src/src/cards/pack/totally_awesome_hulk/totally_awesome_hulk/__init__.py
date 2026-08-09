from cards.pack import *

# Fabriques partagées du pack custom « Totally Awesome Hulk » (DesignHacker).
#
# L'identité a TROIS faces, sur le modèle d'Ant-Man / Invisible Woman :
#   68001a  Totally Awesome Hulk  (héros, traits CHAMPION GAMMA)
#   68001b  Amadeus Cho           (alter-ego)
#   68001c  Uncontrollable Hulk   (héros additionnel, traits BRUTE GAMMA)
#
# Le passage d'une forme à l'autre ne se fait JAMAIS librement : il est piloté
# par les compteurs `rage` posés sur le soutien recto-verso « The Trunk »
# (68012a / 68012b).

TRUNK_NAME = "\"The Trunk\""


def ChangeToBruteForm(player: 'Player', effect: 'Effect') -> None:
    player.GetIdentity().ChangeToForm(CardFinder2("BRUTE", Hero), effect)


def ChangeToChampionForm(player: 'Player', effect: 'Effect') -> None:
    player.GetIdentity().ChangeToForm(CardFinder2("CHAMPION", Hero), effect)


def FindTrunk(effect: 'Effect', player: 'Player|None'=None) -> List['CardFace']:
    """Les faces « The Trunk » en jeu, éventuellement restreintes à un joueur."""
    faces: List['CardFace'] = Worlds.FindCardsOnField(
        effect,
        card_type=Support,
        name=TRUNK_NAME,
    )
    if player is not None:
        faces = [x for x in faces if x.GetControlByPlayer() == player]
    return faces


def IsHypermindActive(player: 'Player') -> bool:
    """« Hypermind » n'est imprimé que sur la face CHAMPION (68001a).

    En forme BRUTE ou en alter-ego, les ressources gardent leur couleur.
    """
    identity = player.GetIdentity()
    if identity is None:
        return False
    return Hero.IsType(identity) and identity.HasTrait("CHAMPION")


def LosingControlGuard() -> 'Ability':
    """« Losing Control » : la forme BRUTE n'est atteignable que par The Trunk.

    Le blocage sec ne suffit pas. Quand le joueur quitte l'alter-ego, le moteur
    lui fait CHOISIR entre les deux formes heros (`DefaultChangeToForm` dans
    `game/card/face/model/form.py`, qui pose la question des qu'il y a plus
    d'une face eligible). S'il repond « BRUTE. GAMMA. », un simple
    `SetBeInstead` annulerait tout : il resterait en alter-ego, action perdue,
    sans rien y comprendre.

    On REDIRIGE donc vers la forme CHAMPION, seul etat legal hors The Trunk.
    La redirection ne se rappelle pas elle-meme : la nouvelle cible n'a pas le
    trait BRUTE.
    """
    def vise_la_forme_brute(effect: 'Effect', message: 'Message.WhenUnitWouldChangeForm') -> bool:
        to_form = message.to_form
        if to_form is None or not Hero.IsType(to_form):
            return False
        if not to_form.HasTrait("BRUTE"):
            return False
        # « by resolving the effects of "The Trunk" support »
        return not CardFinder(name=TRUNK_NAME).Check(message.by_effect.this)

    def rediriger(effect: 'Effect', message: 'Message.WhenUnitWouldChangeForm') -> None:
        message.SetBeInstead(effect)
        player = message.trigger.GetControlByPlayer()
        if player is not None:
            ChangeToChampionForm(player, effect)

    return Ability(
        AbilityType.NonKeyword,
        Message.WhenUnitWouldChangeForm,
        [vise_la_forme_brute],
        rediriger,
    ).SetName("Losing Control")


def PaidOnlyWithWild(effect: 'Effect') -> bool:
    """« If you paid for this card using only [wild] resources ».

    Hypermind (68001a) convertit déjà en [wild] les ressources générées, le
    test sur les ressources réellement payées suffit donc dans les deux formes.
    """
    return effect.GetPaidResources().OnlyHasColor("G")
