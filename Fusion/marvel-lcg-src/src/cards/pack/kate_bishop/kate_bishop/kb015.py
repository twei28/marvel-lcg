from . import *

# Tandem Archery — BASIC, Team-Up (Hawkeye (Clint Barton) and Hawkeye (Kate
#   Bishop)). Max 1 per deck.
# Hero Action: Ready Hawkeye's Bow or put 2 arrow counters on Kate's Bow.
#   Draw 1 card.
#
# CORRECTIF DE DONNEES (test de comportement) : `desc.TeamUp` valait
# "Clint Barton;Kate Bishop" (noms d'alter-ego seuls), sur l'hypothese que
# `HasTeamUp.GetTeamUpUnits` teste le nom sur LES DEUX FACES d'une identite.
# FAUX : `CardFace.IsName` (face_name.py:34) ne verifie QUE la face
# ACTUELLEMENT AFFICHEE (`check_all_face=False` par defaut), et
# `GetTeamUpUnits` ne passe jamais `check_all_face=True`. Comme cette carte
# n'est jouable qu'en forme Heros (Hero Action), Kate y affiche "Hawkeye"
# (son nom de heros, IDENTIQUE a celui de Clint), pas "Kate Bishop" -- la
# carte ne trouvait donc jamais de correspondance pour son propre camp et
# restait injouable EN PERMANENCE (confirme par sonde : `CanPlayBy` = False).
# Corrige en listant les DEUX noms possibles par camp, separes par "/" --
# modele Black Panther/T'Challa;Black Panther/Shuri (bp/51025), seule autre
# carte du depot a devoir distinguer une face Heros partagee de l'alter-ego :
# `desc.TeamUp` vaut maintenant "Hawkeye/Clint Barton;Hawkeye/Kate Bishop".
# `.SetTarget("TeamUp")` exige les deux personnages en jeu pour pouvoir jouer
# la carte, modele Two Against the World (warm/23024.py). "Hawkeye's Bow" est
# l'upgrade signature de Clint (trors/hawkeye, card_id 04002), distincte de
# Kate's Bow.


def GetAbilities() -> Sequence['Ability']:

    def tandem_archery(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)

        initiator = effect.GetInitiator()
        if initiator is None:
            return

        arc_de_clint = Worlds.FindCardOnField(effect, name="Hawkeye's Bow")
        arc_de_kate = TrouverArcEnJeu(effect)

        choix: List['Ability'] = []
        if arc_de_clint:
            choix.append(
                AbilityFactory.ForChoiceAbility(
                    "Ready Hawkeye's Bow",
                    lambda targets: Faces.ReadyAll([arc_de_clint], effect),
                )
            )
        if arc_de_kate:
            choix.append(
                AbilityFactory.ForChoiceAbility(
                    "Put 2 arrow counters on Kate's Bow",
                    lambda targets: PlacerCompteursFlecheSurArc(effect, 2),
                )
            )
        if choix:
            initiator.ChooseAbilities(effect, *choix)

        initiator.DrawUp(1, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            tandem_archery,
        ).SetPlay().SetLabel()
        .SetTarget("TeamUp"),
    ]
