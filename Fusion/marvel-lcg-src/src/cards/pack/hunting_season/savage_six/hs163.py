from . import *

# hs163 * Stegron
# [star] +1 SCH par ennemi SAVAGE SIX en jeu (max +4). Forced Response : apres son entree en jeu, il complote.
# Boost : +1 icone de boost si un serviteur SAVAGE SIX est en jeu.

def GetAbilities() -> Sequence['Ability']:

    def nombre(effect: 'Effect', ui: List['CardFace']) -> int:
        faces = Worlds.FindCardsOnField(effect, trait=TRAIT, card_type=Enemy)
        ui.extend(faces)
        return min(4, len(faces))

    def comploter(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        this = effect.this.CastTo(Minion)
        joueur = this.engaged_player
        if joueur is not None and this.IsInPlay():
            this.DoSchemes(joueur, effect)

    def serviteur_en_jeu(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> bool:
        return len(Worlds.FindCardsOnField(effect, trait=TRAIT, card_type=Minion)) > 0

    return [
        AbilityFactory.ThisGainKeyword(nombre, scheme=1, change_on_event=OnEvent.CardInPlay(CardFinder(trait=TRAIT))),
        AbilityFactory.AfterCardEnterPlay(AbilityType.ForcedResponse, "This", comploter),
        BoostPourIconeSi(serviteur_en_jeu),
        IconeEnPlus(),
    ]
