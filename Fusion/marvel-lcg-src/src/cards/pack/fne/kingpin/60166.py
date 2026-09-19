from . import *

# * Kingpin's Cane (WEAPON) — +1 ATK (desc ATK+), boost [star]+1.
# When Revealed: Attach to Kingpin. You are stunned.
# Forced Response: After Kingpin attacks and damages a hero, stun that hero.
#   If a hero is stunned this way, discard this card.
# [star] Boost: You are stunned. If you were already stunned, take 1 damage.
# Modeles : ReponseForceeCoupDeBoule (60086, AfterUnitAttackAndDamageUnit),
# retour de Faces.GiveStatus (19001a : compte les unites servies, un Stalwart
# refuse en silence), 08029 (identity.TakeDamage(this, 1, effect)).

def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        Faces.GiveStatus([message.GetToPlayer().GetIdentity()], "Stunned", effect)

    def coup_de_canne(effect: 'Effect', message: 'Message.AfterUnitAttackUnit') -> None:
        this = effect.this
        cible = message.attacked
        if Faces.GiveStatus([cible], "Stunned", effect) > 0:
            Faces.DiscardAll([this], effect)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        this = effect.this
        identite = message.GetToPlayer().GetIdentity()
        deja = identite.IsStunned()
        Faces.GiveStatus([identite], "Stunned", effect)
        if deja:
            identite.TakeDamage(this, 1, effect)

    return [
        AttacheAKingpin(),
        AbilityFactory.WhenThisRevealed(None, revele),
        AbilityFactory.AfterUnitAttackAndDamageUnit(
            AbilityType.ForcedResponse,
            CardFinder(name="Kingpin", card_type=Villain),
            Hero,
            coup_de_canne,
            target_in_play=True,
        ),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
