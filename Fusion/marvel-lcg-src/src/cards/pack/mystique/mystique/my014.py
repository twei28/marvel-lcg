from . import *

# Happy Family (Famille Heureuse) : EVENEMENT (CONDITION.), cout 2, [energy].
# Action: If you are in hero form, flip to alter-ego form. Heal 4 damage among Raven Darkhölme, Destiny/Irene Adler, Rogue/Anna Marie.
# (FR 1.1.1 : « Malicia/Anna Marie » = Rogue/Anna Marie)
#
# CARTES DE REFERENCE
#  - `th011` / `01025` : `identite.ChangeToOtherIdentityForm(effect)` pour passer en alter-ego ; `42017` : `joueur.AssignHeal(personnages, N, effect)` pour « heal N damage among ... » (le joueur repartit).
#
# TEXTE CONTRE CODE
#  « If you are in HERO form, flip to alter-ego » : sans « may » (obligatoire) ; deja en alter-ego : on ne retourne pas. « Heal 4 damage AMONG Raven Darkhölme, Destiny/Irene Adler, Rogue/Anna Marie » : 4 points au TOTAL
#    repartis par le joueur entre les personnages EN JEU qui portent l'un de ces noms (apres le retournement : l'identite est alors Raven Darkhölme) ; un personnage absent n'est pas une cible.
#  Chiffres : cout 2, soin 4.


def GetAbilities() -> Sequence['Ability']:

    def happy_family(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        Unused(message)
        joueur = effect.GetInitiator()
        if joueur.IsHero():
            joueur.GetIdentity().ChangeToOtherIdentityForm(effect)
        cibles = [f for f in EnJeuNomme(effect, NOM_RAVEN, NOM_DESTINY, "Irene Adler", "Rogue", "Anna Marie") if Degats(f) > 0]
        if cibles:
            joueur.AssignHeal(cibles, 4, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            happy_family,
        ).SetPlay().SetLabel(),
    ]
