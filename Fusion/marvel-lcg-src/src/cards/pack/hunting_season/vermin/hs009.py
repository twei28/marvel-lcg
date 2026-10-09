from . import *

# Regular Rats (hs009)
# Surge. X = nombre de RAT engages avec vous (max 3) : PV imprimes 1 en data,
# plus (X - 1) via ThisGainKeyword (modele 55018, change_on_event).
# [star] Boost: Put Regular Rats into play engaged with you.

def GetAbilities() -> Sequence['Ability']:

    def pv_supplementaires(effect: 'Effect', ui: List['CardFace']) -> int:
        this = effect.this.CastTo(Minion)
        joueur = this.engaged_player
        if joueur is None:
            return 0
        return max(0, min(3, len(RatsEngages(joueur))) - 1)

    def en_jeu_en_renfort(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        effect.this.CastTo(Minion).PutIntoPlay(message.GetToPlayer(), effect)

    return [
        AbilityFactory.ThisGainKeyword(
            pv_supplementaires,
            health=1,
            change_on_event=[OnEvent.CardType(CardFinder(trait="RAT")), OnEvent.EngagedPlayer("This")],
        ),
        AbilityFactory.WhenCardBecomeBoost("This", en_jeu_en_renfort),
    ]
