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
        # ⚠ `GetThreat()` N'EXISTE PAS : la menace se lit par la PROPRIETE
        # `this.threat` (idiome du depot : ab005, 50154, bt006, 01111). Le
        # moteur avalait l'AttributeError, la condition ne rendait donc jamais
        # True et l'Interruption forcee ne partait JAMAIS — la carte perdait
        # silencieusement la moitie de son texte. Trouve le 04/09/2026 par la
        # gate `verifier_appels_modules` une fois reparee : elle ne lisait
        # aucun sous-dossier de pack, donc aucun module de heros.
        return this.threat > 0

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
