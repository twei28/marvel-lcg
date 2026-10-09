from . import *

# hs114 Tooth Necklace
# Attache a Kraven. SCH+1 (donnees).
# Forced Response (etoile) : apres que Kraven complote, cherche une arme (WEAPON, attachement) dans le paquet et la defausse de rencontre et la revele.
# Interrupt : quand vous attaquez Kraven, placez 2[per_hero] menaces sur le complot principal → defaussez cet attachement.

def GetAbilities() -> Sequence['Ability']:

    def porteur_complote(effect: 'Effect', message: 'Message.AfterUnitSchemeEnd') -> bool:
        cible = effect.this.CastTo(Attachment).bind_face
        return cible is not None and message.trigger is cible

    def armer(effect: 'Effect', message: 'Message.AfterUnitSchemeEnd') -> None:
        Find.FindAndReveal(
            effect, Worlds.GetFirstPlayer(effect),
            finder=CardFinder(trait="WEAPON", card_type=Attachment,
                              check_face_fn=lambda f: not f.IsInPlay()),
        )

    def cout(targets, effect) -> bool:
        effect.this.PlaceThreatOnSchemes("MainScheme", 2 * Worlds.GetPlayerNumIcon(effect), effect)
        return True

    return [
        AttacherALaRevelation(),
        AbilityFactory.AfterUnitSchemeEnd(AbilityType.ForcedResponse, Villain, armer, conditions=[porteur_complote]),
        InterruptContrePorteur(None, CostFunc.Custom(None, cout)),
    ]
