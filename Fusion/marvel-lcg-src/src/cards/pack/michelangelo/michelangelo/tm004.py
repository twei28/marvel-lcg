from . import *

# Impulsive — evenement signature, x2 (3/15 et 4/15). Cout 1, [energy].
# Hero Action: Place 2 threat on the main scheme -> ready Michelangelo and a
#   WEAPON you control. Draw 1 card.
#
# Cartes de reference :
#  - poser de la menace sur la principale : `mister_fantastic/mf013` —
#    `this.PlaceThreatOnSchemes("MainScheme", n, effect)` ;
#  - redresser le heros et une arme : `vnm/20005` Run and Gun (cible ici
#    ecrite a la main, la carte ne dit PAS « si vous en controlez une »).
#
# ⚠ Mots-pieges :
#  - Le « → » est un COUT dans le texte imprime : on pose d'abord les 2
#    menaces, puis le reste (ecrit en sequence, pas en `SetCostFunc`).
#  - « ready Michelangelo AND a WEAPON you control » : le heros est TOUJOURS
#    redresse ; l'arme est facultative en l'absence d'arme (pas de blocage).
#    # TODO-QUESTION (question 4 : sans arme en jeu, la carte se joue-t-elle ?).
#  - « WEAPON you control » : toute amelioration WEAPON que vous controlez
#    (`GetControlUpgrade`), pas seulement celles du heros.
#  - « Draw 1 card » : phrase separee, hors du « → ».

def GetAbilities() -> Sequence['Ability']:

    def impulsive(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)

        initiator = effect.GetInitiator()
        if initiator is None or not initiator.IsHero():
            return

        this.PlaceThreatOnSchemes("MainScheme", 2, effect)

        heros = initiator.GetHero()
        a_redresser = [heros]
        armes = CardFinder(trait="WEAPON", card_type=Upgrade).Checks(
            initiator.GetControlUpgrade())
        if armes:
            arme = initiator.AskChooseFace(
                list(armes), effect, prompt="Ready a WEAPON you control")
            a_redresser.append(arme or armes[0])
        Faces.ReadyAll(a_redresser, effect)

        initiator.DrawUp(1, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            impulsive,
        ).SetPlay(),
    ]
