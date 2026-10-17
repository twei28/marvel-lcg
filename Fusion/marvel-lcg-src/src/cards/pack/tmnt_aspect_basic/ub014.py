from . import *

# * Fugitoid « Professor Honeycutt » — ALLIE 2 [energy], 1*/1*, 2 PV, aspect Basic (TMNT Starter). ANDROID.
# DIMENSION X.
# [star] Response: After Fugitoid uses a basic power, discard 1 card from your hand. If that card's printed
#   resource has:
#   [physical] - Heal 2 damage from a friendly character.
#   [mental] - Remove 2 threat from a scheme.
#   [energy] - Deal 2 damage to an enemy.
#   [wild] - Draw 1 card.
#
# NOUVELLE. Carte de reference : 45020 Legion — meme declencheur `AfterUnitUseBasicPower(Response, "This")`,
# meme lecture `FacesCounter.GetPrintedResources([carte])` puis une branche par icone. Differences : la
# carte vient de la MAIN (choisie : `DiscardHandCards((1, 1))`, modele 15019) et non du dessus du deck ; le
# soin vise « a friendly character » (n'importe lequel), et il existe une 4e branche [wild] -> pioche 1.
# Le [star] devant Response est l'icone etoile (fiche special.md) : zero code. Les « 1★ » de THW/ATK sur le
# scan sont la meme etoile de rappel ; `desc` garde « 1* » (1 degat consecutif, icone sous chaque valeur).
# TEXTE CONTRE CODE : « If that card's printed resource HAS » : chaque icone presente declenche sa branche
# (une carte a deux icones differentes en declenche deux ; une double [physical] n'en declenche qu'une).
# Main vide : rien a defausser, aucune branche.


def GetAbilities() -> Sequence['Ability']:

    def fugitoid(effect: 'Effect', message: 'Message.AfterUnitUseBasicPower') -> None:
        this = effect.this.CastTo(Ally)

        initiator = effect.GetInitiator()
        faces = initiator.DiscardHandCards((1, 1), effect)
        if not faces:
            return
        res = FacesCounter.GetPrintedResources(list(faces))
        if res.r:
            initiator.ChooseAbilities(
                effect,
                AbilityFactory.ForChoiceAbility(
                    "Heal 2 damage from a friendly character",
                    lambda targets: this.HealthUnits(targets, 2, effect)
                ).SetTarget(Friend, canbe_heal=True)
            )
        if res.b:
            initiator.ChooseAbilities(
                effect,
                AbilityFactory.ForChoiceAbility(
                    "Remove 2 threat from a scheme",
                    lambda targets: this.RemoveThreatFromSchemes(targets, 2, effect)
                ).SetTarget(Scheme2)
            )
        if res.y:
            initiator.ChooseAbilities(
                effect,
                AbilityFactory.ForChoiceAbility(
                    "Deal 2 damage to an enemy",
                    lambda targets: this.DealDamage(targets, 2, effect)
                ).SetTarget(Enemy)
            )
        if res.g:
            initiator.DrawUp(1, effect)

    return [
        AbilityFactory.AfterUnitUseBasicPower(
            AbilityType.Response,
            "This",
            fugitoid
        ),
    ]
