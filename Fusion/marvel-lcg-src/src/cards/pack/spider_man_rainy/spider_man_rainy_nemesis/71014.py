from . import *

# For My Next Trick... — custom « Rainy » (nemesis de Peter Parker)
# Uses (2 illusion counters).
# Forced Response: After the villain phase begins, remove 1 illusion counter
#   from here.
# Forced Interrupt: When this card would leave play, if it was not defeated,
#   deal each player a facedown encounter card.

def GetAbilities() -> Sequence['Ability']:
    # EncounterSideScheme n'herite pas de HasUses : la cle desc.Uses ferait
    # planter la creation de partie (meme lecon que les compteurs psionic de
    # Julia Carpenter, madame_web). Les 2 compteurs illusion sont donc poses
    # par ThisEnterPlayWithCounters, et la defausse au dernier compteur est
    # geree a la main.

    def retirer_illusion(effect: 'Effect', message: 'Message.WhenPhaseBegin') -> None:
        this = effect.this.CastTo(EncounterSideScheme)
        Faces.RemoveCountersOn([this], 1, 'illusion', effect)

    def plus_de_compteurs(effect: 'Effect', message: 'Message.AfterCardRemovedCounter') -> None:
        this = effect.this.CastTo(EncounterSideScheme)
        Faces.DiscardAll([this], effect)

    def dernier_tour(effect: 'Effect', message: 'Message.WhenCardWouldLeavePlay') -> None:
        this = effect.this.CastTo(EncounterSideScheme)
        Unused(this)
        Utility.DealEachPlayerEncounterCard(effect)

    def pas_vaincue(effect: 'Effect', message: 'Message.WhenCardWouldLeavePlay') -> bool:
        # Un plan annexe vaincu part avec 0 menace ; s'il quitte le jeu avec de
        # la menace dessus (fin des compteurs illusion), il n'a pas ete vaincu.
        this = effect.this.CastTo(EncounterSideScheme)
        return this.GetThreat() > 0

    return [
        AbilityFactory.ThisEnterPlayWithCounters(2, 'illusion'),

        AbilityFactory.WhenVillainPhaseBegin(
            AbilityType.ForcedResponse,
            retirer_illusion,
        ),

        AbilityFactory.AfterCardRemovedCounter(
            AbilityType.ForcedResponse,
            "This",
            'illusion',
            plus_de_compteurs,
            is_last_counter=True,
        ),

        AbilityFactory.WhenCardWouldLeavePlay(
            AbilityType.ForcedInterrupt,
            "This",
            dernier_tour,
            conditions=[pas_vaincue],
        ),
    ]
