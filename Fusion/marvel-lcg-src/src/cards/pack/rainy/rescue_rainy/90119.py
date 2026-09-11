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
        # ⚠ DECLARER l'ignorance, pas seulement la passer a la resolution
        # (11/09/2026). Depuis que la Crise verrouille la CIBLE
        # (`MainScheme.CanBeThwartBy`), le complot principal n'est plus offert
        # aux contres tant qu'une Crise est en jeu. `ignore_crisis=True` dans
        # l'operation arrive trop tard : il faut que le ciblage le sache.
        # `SetIgnoreKeyword` pose exactement ce que lit `IsIgnoreKeyword`.
        #
        # C'est le SEUL contre du depot qui ignore la Crise : les six autres
        # cartes a `ignore_crisis=True` sont des Actions, qui ne passent pas
        # par `CanBeThwartBy`. La gate `verifier_ignore_crise.py` veille a ce
        # qu'un futur contre n'oublie pas cette ligne.
        .SetIgnoreKeyword('Crisis')
        .SetTarget(Scheme2),
    ]
