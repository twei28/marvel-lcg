from . import *

# hs172 Taunt (Experience Cost 1)
# Hero Action : donne au vilain jusqu'a trois cartes boost face cachee ;
# pioche 1 carte par carte ainsi donnee.

def GetAbilities() -> Sequence['Ability']:

    def provoquer(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        joueur = effect.GetInitiator()
        vilain = Worlds.FindVillain(effect)
        if vilain is None:
            return

        def donner(n: int):
            def op(cibles: Sequence['CardFace']) -> None:
                paquet = vilain.components.boostable.GetDeck()
                avant = paquet.GetSize()
                Faces.GiveFacedownBoostCards([vilain], n, effect)
                donnees = paquet.GetSize() - avant
                if donnees > 0:
                    joueur.DrawUp(donnees, effect)
            return op

        joueur.ChooseAbilities(
            effect,
            *[AbilityFactory.ForChoiceAbility(f"Give the villain {n} facedown boost card(s)", donner(n)) for n in (3, 2, 1)],
        )

    return [
        AbilityFactory.WhenInYourPlayTurn(AbilityType.HeroAction, provoquer).SetPlay(),
    ]
