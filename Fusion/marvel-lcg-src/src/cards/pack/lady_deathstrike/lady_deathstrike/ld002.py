from . import *

# * Lady Deathstrike (II) — VILAIN, stade 2. REAVER. PV 18 par joueur, ATK 3, SCH 1.
# When Revealed: Find Reinforced Adamantium Claws and reveal it. If you cannot, resolve the "Special" ability on each copy of
#   Bleeding Out in play.
# Forced Response: After Lady Deathstrike attacks and damages you, resolve the "Special" ability on the copy of Bleeding Out
#   attached to your identity.
#
# Cartes de reference :
#  - « Find X and reveal it » : `Find.FindAndReveal(effect, joueur, name=..., card_type=...)` (`59003` Embody Pathos, `60134a`),
#    rend la carte revelee ou None (« If you cannot »).
#  - Forced Response : `ld001` (meme texte, meme fabrique).
#
# ⚠ Mots-pieges :
#  - « If you CANNOT » : Griffes introuvables (deja en jeu, ou ni dans le deck ni dans la defausse de rencontre) -> la
#    branche Special sur CHAQUE copie en jeu (une par joueur) ; si on les trouve, AUCUN Special ;
#  - les Griffes se REVELENT (elles s'attachent a Lady Deathstrike par leur propre capacite d'attache) : pas de mise en jeu directe.


def GetAbilities() -> Sequence['Ability']:

    def revelee(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Villain)
        Unused(this)

        joueur = message.GetToPlayer()
        griffes = Find.FindAndReveal(effect, joueur, name=NOM_GRIFFES, card_type=Attachment)
        if griffes is None:
            ResoudreSurTous(effect)

    def saigner(effect: 'Effect', message: 'Message.AfterUnitAttackUnit') -> None:
        this = effect.this.CastTo(Villain)
        Unused(this)

        ResoudreSaignement(effect, message.GetToPlayer())

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            revelee,
        ),
        AbilityFactory.AfterUnitAttackAndDamageUnit(
            AbilityType.ForcedResponse,
            "This",
            "You",
            saigner,
        ),
    ]
