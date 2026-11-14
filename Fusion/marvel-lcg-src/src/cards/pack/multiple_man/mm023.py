from . import *

# Got Your Back : EVENEMENT Leadership, cout 2, [mental]. TACTIC. (carte de l'auteur)
# Play only if you control an ally while you have 3 or fewer remaining hit points.
# Hero Action: Each character you control cannot take damage until the end of the round.
#
# CARTES DE REFERENCE : `29025` (Go for Champions! : `RegisterTemp(UnitCannotTakeDamageWhile(Temp0, ..), unregister_after_exec=False, until_round_end=True)`), RECETTES (« They cannot take damage until the end
#  of the round » : `conditions=[lambda e, m: m.trigger in cibles]`).
# TEXTE CONTRE CODE : « remaining hit points » : la valeur lue sur le cadran (`identite.health`, RRG 1.2). « you have 3 OR FEWER » : <= 3. « control AN ALLY » : au moins un allie. « EACH character YOU CONTROL » :
#  l'identite et les allies, y compris ceux qui entrent en jeu plus tard dans le round (condition lue au moment de chaque degat). Chiffres : cout 2, seuil 3.


def GetAbilities() -> Sequence['Ability']:

    def jouable(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> bool:
        Unused(message)
        joueur = effect.GetInitiator()
        if not EstJoueur(joueur):
            return False
        return len(joueur.allies.Get()) > 0 and joueur.GetIdentity().health <= 3

    def got_your_back(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)
        joueur = effect.GetInitiator()

        def personnage_du_joueur(effect2: 'Effect', message2: 'Message.WhenUnitWouldTakeDamage') -> bool:
            Unused(effect2)
            cible = message2.trigger
            if not (Hero.IsType(cible) or AlterEgo.IsType(cible) or Ally.IsType(cible)):
                return False
            return cible.GetControlByOrOwner() is joueur

        this.effect.RegisterTemp(
            AbilityFactory.UnitCannotTakeDamageWhile(
                AbilityType.Temp0,
                Unit2,
                conditions=[personnage_du_joueur],
            ),
            unregister_after_exec=False,
            until_round_end=True,
        )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            got_your_back,
            conditions=[jouable],
        ).SetPlay().SetLabel(),
    ]
