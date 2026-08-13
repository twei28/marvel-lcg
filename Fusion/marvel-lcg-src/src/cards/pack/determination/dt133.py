from . import *

# * Orka

def GetAbilities() -> Sequence['Ability']:

    def personnages_fragiles(effect: 'Effect', ui: List['CardFace']) -> int:
        this = effect.this.CastTo(Ally)
        player = this.GetControlByPlayer()
        if player is None:
            return 0
        # « fragile » n'est pas un mot-cle du moteur : les cartes qui le portent
        # sont celles de l'aspect dont le texte le dit.
        candidats = list(player.GetAllies())
        candidats += Worlds.FindCardsOnField(effect, card_type=Minion,
                                             engaged_with=player)
        return sum(1 for f in candidats if "Fragile." in (f.paper.text or ""))

    def check_pas_de_hero_for_hire(effect: 'Effect', message: 'Message.WhenCalculateEffectCost') -> bool:
        initiator = effect.GetInitiator()
        if initiator is None:
            return False
        return not any(f.HasTrait("HERO FOR HIRE") for f in initiator.GetControlCards())

    return [
        AbilityFactory.ReduceCostToPlayThis(
            -1,
            conditions=[check_pas_de_hero_for_hire]
        ),
        AbilityFactory.ThisGainKeyword(
            personnages_fragiles,
            attack=1,
            change_on_event=OnEvent.CardInPlay(Unit2),
        ),
    ]
