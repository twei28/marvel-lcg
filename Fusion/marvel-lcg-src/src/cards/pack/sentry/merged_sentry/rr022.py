from . import *

# * Newfound Nature : ATTACHEMENT (CONDITION.), ATK ☆, boost 2. Set « Merged Sentry ».
# Attach to Merged Sentry. Otherwise, this card gains surge.
# When Revealed: Place X overwhelm counters on Merged Sentry, where X is equal to the villain's current stage number.
# ★ Forced Response: After Merged Sentry attacks and damages a non-hero character, stun that character.
#
# CARTES DE REFERENCE
#  - `ca017` : `AttachToFaceWhenPutIntoPlay(CardFinder(card_type=Minion, name=..), if_cannot_gain_surge=True)` ; stade du vilain : `villain.printed_stage` (`sk270`, `21013`).
#  - « After X attacks and damages » : `AbilityFactory.AfterUnitAttackAndDamageUnit(ForcedResponse, attacker, who_be_attacked, op)` (do_attack.py:477) ; statut : `Faces.GiveStatus(.., "Stunned")`.
#
# TEXTE CONTRE CODE
#  « X = the VILLAIN's stage » (pas celui du complot principal). « non-hero CHARACTER » : un allie ; l'alter-ego et le heros sont exclus. Sans Merged Sentry le When Revealed ne pose rien (la carte a deja gagne surge a l'attache).


def GetAbilities() -> Sequence['Ability']:

    def newfound_nature(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        Unused(message)
        merged = Worlds.FindCardOnField(effect, name=NOM_MERGED, card_type=Minion)
        if merged is None:
            return
        vilain = Worlds.FindCardOnField(effect, card_type=Villain)
        x = int(getattr(vilain, "printed_stage", 1) or 1)
        Faces.PlaceCountersOn([merged], x, NOM_SUBMERSION, effect)

    def etourdir(effect: 'Effect', message: 'Message.AfterUnitAttackUnit') -> None:
        cible = message.attacked
        if cible is not None and cible.IsInPlay():
            Faces.GiveStatus([cible], "Stunned", effect)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(
            CardFinder(card_type=Minion, name=NOM_MERGED),
            if_cannot_gain_surge=True,
        ),
        AbilityFactory.WhenThisRevealed(None, newfound_nature),
        AbilityFactory.AfterUnitAttackAndDamageUnit(
            AbilityType.NonKeywordStar,  # ★ du texte imprime ; ForcedResponse ne se declenchait pas depuis une carte attachee
            "AttachedEnemy",
            Ally,
            etourdir,
        ),
    ]
