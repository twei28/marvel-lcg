from core import *

from game.card.face import *

from game.ability import *
from game.message import *

from game.ability.factory import *
from game.ability.condition import Condition
Unused(Condition)

from game.ability.factory.campaign import AbilityFactoryCampaign
Unused(AbilityFactoryCampaign)

from game.message import OnEvent
Unused(OnEvent)

from game.player import Player, Scenario, PlayerFinder
Unused(Player, Scenario, PlayerFinder)
from game.player import Form
Unused(Form)

from game.world.game_area import GameArea
from game.element.resources import Resources
from game.element.cost import Cost
Unused(GameArea)
Unused(Resources)
Unused(Cost)

from game.selector import Select
Unused(Select)

from game.card import Card
Unused(Card)

from game.deck import Deck, Deck2, DeckType
Unused(Deck, Deck2, DeckType)


from game.card.factory import CardFactory
Unused(CardFactory)

from game.operate.rand import Rand
Unused(Rand)

from game.effect.rule import ResetKeyword
from game.effect.rule import MainSchemePhasePlaceThreat
Unused(ResetKeyword)
Unused(MainSchemePhasePlaceThreat)

from game.element.damage_property import DamageProperty
Unused(DamageProperty)

from game.operate.faces import Faces
from game.operate.faces_counter import FacesCounter
from game.operate.filter import Filter
from game.operate.effects import Effects
from game.operate.search import Search
from game.operate.find import Find
from game.operate.players import Players
from game.operate.campaign_logs import CampaignLog
from game.operate.utility import Utility
Unused(Faces)
Unused(FacesCounter)
Unused(Filter)
Unused(Effects)
Unused(Search)
Unused(Find)
Unused(Players)
Unused(CampaignLog)
Unused(Utility)

from game.operate.run_at import RunAt
from game.operate.setup_cards import SetupCards
from game.operate.worlds import Worlds
from game.operate.modular_set import AsideModularSet
from game.operate.store import Stores
Unused(RunAt)
Unused(SetupCards)
Unused(Worlds)
Unused(AsideModularSet)
Unused(Stores)

# Briques communes Punisher MC×DC / Galactic Storm (20/10/2026),
# RECETTES-MOTEUR.md §15 : « insensible aux cartes joueur ».
from game.operate.immunity import PlayerCardImmunity
from game.operate.villains import Villains
from game.operate.ville import Ville
Unused(Ville)
from game.operate.assemblee import Assemblee, ErreurAssemblee
Unused(Assemblee, ErreurAssemblee)
Unused(PlayerCardImmunity)
Unused(Villains)

from game.element.utility import IsCounter, IsTrait
Unused(IsCounter, IsTrait)

from game.buff import *

CardFinder.NonEliteMinion = CardFinder(non_trait="ELITE", card_type=Minion)
# CardFinder2.Null = CardFinder2()
NonEliteMinion = CardFinder.NonEliteMinion

################################################################################
#
def ShuffleThisCardIntoEncounter(by_effect: 'Effect', message: 'Message2') -> None:
    this = by_effect.this
    encounter_deck = Worlds.GetEncounterDeck(by_effect)
    Faces.ShuffleAllTo([this], encounter_deck, by_effect)

def ThisCardGainSurge(by_effect: 'Effect', message: 'Message2|None'=None) -> None:
    this = by_effect.this.CastTo(CanSurge)
    this.GainSurge(1, by_effect)

def DiscardThisCard(by_effect: 'Effect', message: 'Message2') -> None:
    this = by_effect.this
    Faces.DiscardAll([this], by_effect)

def RemoveThisFromGame(by_effect: 'Effect', message: 'Message2') -> None:
    this = by_effect.this
    Faces.RemoveAllFromGame([this], by_effect)

def DiscardSelectedCards(by_effect: 'Effect', message: 'Message2') -> None:
    Faces.DiscardAll(by_effect.targets, by_effect)

def PutThisIntoPlay(by_effect: 'Effect', message: 'TriggerNonePlayerMessage') -> None:
    this = by_effect.this
    player = message.GetToPlayer()
    this.PutIntoPlay(player, by_effect)

def RevealThisCard(by_effect: 'Effect', message: 'TriggerNonePlayerMessage') -> None:
    this = by_effect.this
    player = message.GetToPlayer()
    this.Reveal(player, by_effect)

################################################################################
# Player
"""
Player.DiscardDeckTopCards
Player.DiscardDeckUntil
"""

def YouMayFlipToYourAlterEgoForm(player: 'Player', effect: 'Effect'):
    if player.IsHero():
        player.MayChooseOneAbility(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Flip to alter-ego form",
                lambda targets:
                    player.GetIdentity().ChangeToForm(AlterEgo, effect)
            )
        )

def YouMayChangeForm(player: 'Player', effect: 'Effect'):
    identity = player.GetIdentity()

    face = player.MayChooseOneText(player.GetAllIdentityFace(exclude=identity))
    if face:
        player.GetIdentity().ChangeToFace(face, effect)

################################################################################
# TMNT SHINOBI (Inkwire, 17/10/2026) : helpers PARTAGES par tous les packs `tmnt_shinobi_*` (et par
# jennika, qui a les siens, equivalents). Voir docs/reference/mots-cles/shinobi.md.
#
# Une carte SHINOBI = une carte portant l'une des quatre classes Bushido / Ninjutsu / Kuji-Kiri /
# Taijutsu dans `desc.Class` (separees par « ; »). Une carte DUAL en porte DEUX (« Bushido;Kuji-Kiri ») et
# compte donc pour LES DEUX en jeu comme a la construction (livret p.7). Les classes Shinobi ne sont ni
# des ASPECTS ni « Basic » : `IsClass("Aspect")` et `IsClass("Basic")` restent faux (livret p.8 :
# « Shinobi cards do not count as aspect or basic cards when triggering abilities »).
CLASSES_SHINOBI: List[str] = ["Bushido", "Ninjutsu", "Kuji-Kiri", "Taijutsu"]

def CarteShinobi(*classes: str) -> 'CardFinder':
    """Filtre « une carte Shinobi » ; avec des classes, « une carte <classe> » (OU entre elles)."""
    # Un PATH porte les classes de ses types (desc.Class) mais n'est pas une « carte Shinobi » du deck : exclu.
    return CardFinder(card_classes=list(classes) if classes else list(CLASSES_SHINOBI), non_card_type=Path)  # type: ignore

def EstShinobi(face: 'CardFace|None', *classes: str) -> bool:
    """Vrai si `face` est une carte Shinobi (de l'une des `classes` si precisees ; Dual : l'une ou l'autre). Un Path : faux."""
    if face is None or not ClassCard.IsType(face) or Path.IsType(face):
        return False
    return face.IsClass(*(classes or CLASSES_SHINOBI))  # type: ignore

def PayeAvecUnEvenement(effect: 'Effect', *traits: str) -> bool:
    """« If you paid for this card with an ATTACK / THWART / DEFENSE event » : un AUTRE evenement
    portant l'un des traits, defausse pour sa ressource, figure dans le paiement de `effect.this`."""
    this = effect.this
    return any(
        Event.IsType(e.this) and e.this != this and any(e.this.HasTrait(t) for t in traits)  # type: ignore
        for e in effect.context.paid_this_res_effects
    )

def ShinobiCloak(effect: 'Effect', faces: 'CardFace|Sequence[CardFace|None]|None') -> int:
    """« Cloak X » : pose la carte d'etat Cloaked (une seule par personnage). Rend le nombre de
    personnages reellement camoufles (porte le « if you cannot »)."""
    if faces is None:
        return 0
    cibles = [faces] if isinstance(faces, CardFace) else [f for f in faces if f is not None]
    return Faces.GiveStatus(cibles, "Cloaked", effect) if cibles else 0

def ShinobiDaze(effect: 'Effect', faces: 'CardFace|Sequence[CardFace|None]|None') -> int:
    """« Daze X » : pose la carte d'etat Dazed (une seule par personnage). Rend le nombre de personnages hebetes."""
    if faces is None:
        return 0
    cibles = [faces] if isinstance(faces, CardFace) else [f for f in faces if f is not None]
    return Faces.GiveStatus(cibles, "Dazed", effect) if cibles else 0

