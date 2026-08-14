from . import *

# Lizard Brain

def GetAbilities() -> Sequence['Ability']:

    def dernier_compteur(effect: 'Effect', message: 'Message.WhenTheLastCounterIsRemovedFromHere') -> None:
        # « [star] Forced Response: After the last sanity counter is removed
        # from here, flip Curt Connors, then set The Lizard's hit point dial to
        # his printed hit points. »
        #
        # Meme precaution que partout dans ce pack : les PV sont portes par la
        # CARTE. On remet la face d'arrivee a son maximum APRES le retournement,
        # sinon The Lizard revient deja vaincu.
        connors = Worlds.FindCardOnField(effect, name="Curt Connors", card_type=Villain)
        if not connors:
            return
        connors.card.Flip(effect)
        lizard = connors.card.face.CastTo(Villain)
        lizard.ResetHealth(effect)

    return [
        # « In expert mode, each minion gains the REPTILIAN trait. »
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            CardFinder(card_type=Minion),
            trait=["REPTILIAN"],
            expert_mode_only=True,
        ),
        AbilityFactory.WhenTheLastCounterIsRemovedFromHere(
            AbilityType.ForcedResponse,
            'sanity',
            dernier_compteur
        ),
    ]
