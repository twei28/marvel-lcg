from . import *

# * Blink (Clarice Ferguson) : allie RECRUITED, cout 3, PV 2, THW 1*, ATK 1*.
# Any of the players may play Blink from the Recruited Mutants discard pile during their own turn (paying its resource cost).
# Forced Response: When Blink is defeated, shuffle her into the Recruited Mutants deck.
#
# Cartes de reference : dz014 / 53021 (`AbilityFactory.YouMayPlayCardLikeInHand(..., from_where="YourDiscardPile", during="YourTurn")`,
# play.py:436), `RecruitedMutants` (__init__.py : le deck de table, E2).
# ⚠ La PERMISSION de jouer Blink depuis la defausse Recruited n'est PAS portee par cette carte (une capacite de carte endormie dans une defausse
# n'est pas active) : voir `PermissionDeJouerLesRecrutes` (__init__.py), portee par Xavier's Institute (hf048) et Rally the Survivors (hf045).
def GetAbilities() -> Sequence['Ability']:
    def blink(effect: 'Effect', message: 'Message.AfterUnitBeDefeated') -> None:
        this = effect.this.CastTo(Ally)
        deck, _ = RecruitedMutants(effect)
        Faces.MoveAllTo([this], deck, effect)
        deck.Shuffle(effect)

    return [
        AbilityFactory.AfterUnitBeDefeated(
            AbilityType.ForcedResponse,
            "This",
            blink,
        ),
    ]
