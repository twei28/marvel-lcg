from . import *

# * Lady Deathstrike (III) — VILAIN, stade 3. REAVER. PV 19 par joueur, ATK 3, SCH 1.
# When Revealed: Resolve the "Special" ability on each copy of Bleeding Out in play. Find Reaver Commander and reveal it.
# Forced Response: After a REAVER attacks and damages you, resolve the "Special" ability on the copy of Bleeding Out attached to
#   your identity.
#
# Cartes de reference :
#  - `ld002` (Find.FindAndReveal, Special sur chaque copie) ; `41013` pour `AfterUnitAttackAndDamageUnit` avec un FILTRE d'attaquant
#    (`CardFinder(trait=..., card_type=Enemy)`).
#
# ⚠ Mots-pieges :
#  - « a REAVER attacks and damages you » : N'IMPORTE QUEL ennemi REAVER (Lady Deathstrike elle-meme, Reaver Tracker, les sbires du
#    set Reavers), pas seulement elle ;
#  - ORDRE : le Special sur chaque copie d'ABORD, puis le Commandant (la phrase le dit dans cet ordre) ; si le Commandant est
#    introuvable on ne fait rien de plus (aucun « If you cannot » imprime ici).


def GetAbilities() -> Sequence['Ability']:

    def revelee(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Villain)
        Unused(this)

        ResoudreSurTous(effect)
        Find.FindAndReveal(effect, message.GetToPlayer(), name=NOM_COMMANDANT, card_type=Attachment)

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
            CardFinder(trait="REAVER", card_type=Enemy),
            "You",
            saigner,
        ),
    ]
