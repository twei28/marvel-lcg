from cards.pack import *

# Helpers du set Hammerhead (Fear No Evil, 60086-60096).


def TrouverHammerhead(effect: 'Effect') -> 'Villain|None':
    """Le vilain Hammerhead en jeu, quel que soit son stade."""
    return Worlds.FindCardOnField(effect, name="Hammerhead", card_type=Villain)


def ReponseForceeCoupDeBoule(degats: int) -> 'Ability':
    """[star] Forced Response : After Hammerhead attacks and damages a
    character, stun that character. If that character was already stunned,
    deal N damage to them.

    Modele : 01118 Sonic Converter (AfterUnitAttackAndDamageUnit sur
    "Character", target_in_play=True). « already stunned » se lit AVANT de
    poser le statut : un personnage Steady a une carte peut etre re-etourdi
    sans avoir ete « stunned » au sens des regles.
    """
    def coup_de_boule(effect: 'Effect', message: 'Message.AfterUnitAttackUnit') -> None:
        this = effect.this.CastTo(Villain)
        cible = message.attacked
        deja_etourdi = cible.IsStunned()
        Faces.GiveStatus([cible], "Stunned", effect)
        if deja_etourdi:
            this.DealDamage([cible], degats, effect)

    return AbilityFactory.AfterUnitAttackAndDamageUnit(
        AbilityType.ForcedResponse,
        "This",
        "Character",
        coup_de_boule,
        target_in_play=True,
    )
