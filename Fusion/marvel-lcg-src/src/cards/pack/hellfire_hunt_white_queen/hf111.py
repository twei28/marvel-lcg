from . import *

# Psionic Maelstrom. Attachement ILLUSION PSIONIC. « Attach to White Queen. Uses (1 illusion counter). When Revealed : If White Queen is in
# PSIONIC form, place 1 additional illusion counter here. [star] Forced Response : After White Queen attacks you, take X indirect damage,
# where X is equal to the number of ILLUSION cards in play. Remove 1 illusion counter from here. »
# Uses : natif (`desc.Uses = "1,illusion"`) : le dernier pion retire fait quitter la carte (fiche mots-cles/uses.md).
# ATK burst « etoile » sans nombre : `desc.ATK+ = "0*"` (precedent sv015).
# Cartes de reference : 41029 Telekinetic Dragon (`TakeIndirectDamage`), 06027 (`Worlds.FindCardSizeOnField`), 04064 (attachement a un vilain).


def GetAbilities() -> Sequence['Ability']:
    def revelee(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        if EstPsionique(VilainWQ(effect)):
            Faces.PlaceCountersOn([effect.this], 1, COMPTEUR_ILLUSION, effect)

    def apres_attaque(effect: 'Effect', message: 'Message.AfterUnitAttackEnd') -> None:
        this = effect.this
        joueur = message.GetAgainstPlayer()
        if joueur is not None:
            joueur.GetIdentity().TakeIndirectDamage(this, NombreDIllusions(effect), effect)
        RetirerUnCompteurIllusion(effect)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(ChercheurWQ()),
        AbilityFactory.WhenThisRevealed(None, revelee),
        AbilityFactory.AfterUnitAttackYou(AbilityType.ForcedResponse, ChercheurWQ(), apres_attaque),
    ]
