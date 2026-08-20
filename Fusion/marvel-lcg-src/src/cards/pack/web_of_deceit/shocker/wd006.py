from . import *

# * Sandman

def GetAbilities() -> Sequence['Ability']:

    def sandman(effect: 'Effect', message: 'Message.AfterUnitAttackUnit') -> None:
        this = effect.this.CastTo(Minion)
        Unused(this)
        # « discard the top 6 cards of the encounter deck. »
        Faces.DiscardAll(Search.EncounterCardsTop(effect, None, 6) or [], effect)

    return [
        # ⚠ Le texte dit « attacks », pas « attacks and damages » : une attaque
        # entierement bloquee ou defendue a 0 declenche quand meme. C'est
        # `AfterUnitAttackUnit` qu'il faut, comme wd064 (Princess Python) et
        # wd088 (Feather Daggers) — pas la variante « AndDamage », qui exige
        # des degats.
        AbilityFactory.AfterUnitAttackUnit(
            AbilityType.ForcedResponse,
            "This",
            "Character",
            sandman
        ),
        AbilityFactory.AfterMinionEngagePlayer(
            AbilityType.ForcedResponse,
            "This",
            "You",
            sandman
        ),
    ]
