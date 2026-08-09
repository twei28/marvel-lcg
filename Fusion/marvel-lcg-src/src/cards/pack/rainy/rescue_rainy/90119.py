from . import *

# Search and Rescue

def GetAbilities() -> Sequence['Ability']:

    def crise_en_jeu(effect: 'Effect') -> bool:
        """Une icone de crise est-elle presente sur un complot en jeu ?"""
        for face in Worlds.GetOnFieldCards(effect.this.card.game_area):
            if Scheme2.IsType(face) and face.IsInPlay() and getattr(face, 'crisis', 0):
                return True
        return False

    def search_and_rescue(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)

        if crise_en_jeu(effect):
            # 2 menaces de plus ET le thwart ignore l'icone de crise.
            this.RemoveThreatFromSchemes(effect.targets, 5, effect, ignore_crisis=True)
        else:
            this.RemoveThreatFromSchemes(effect.targets, 3, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            search_and_rescue
        ).SetPlay().SetLabel('thwart')
        .SetTarget(Scheme2),
    ]
