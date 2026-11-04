from . import *

# Ultimate Teamwork : EVENEMENT Leadership, cout 2, [physical]. TACTIC. (carte de l'auteur)
# Hero Action: Choose a team trait. If you control at least 4 characters that share the chosen team trait, they each get +2 ATK until the end of the phase.
#
# CARTES DE REFERENCE : `27185b` (`identite.GainUntilPhaseEnd(effect, hand_size=1, end_phase="Player")`), `face_action.py::GainUntilPhaseEnd(.., attack=n)`.
# TEXTE CONTRE CODE : DECISION UTILISATEUR (04/11) : « team trait » = n'IMPORTE QUEL trait partage par au moins 4 des personnages que le joueur controle (identite + allies) ; pas de liste de traits d'equipe.
#  Le joueur choisit le trait parmi ceux qui atteignent 4 (un seul : pris d'office) ; aucun : l'evenement est joue pour rien. « they EACH get +2 ATK until the end of the PHASE » : les personnages qui partagent
#  le trait, au moment de la resolution ; `end_phase="Player"`. Chiffres : cout 2, 4 personnages, +2 ATQ.


def GetAbilities() -> Sequence['Ability']:

    def teamwork(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        Unused(message)
        joueur = effect.GetInitiator()
        if not EstJoueur(joueur):
            return
        personnages = [joueur.GetIdentity()] + [f for f in joueur.allies.Get() if f.IsInPlay()]
        compte: Dict[str, List['CardFace']] = {}
        for p in personnages:
            for trait in list(p.traits_internal.keys()):
                if p.HasTrait(trait):
                    compte.setdefault(trait, []).append(p)
        valides = sorted(t for t, liste in compte.items() if len(liste) >= 4)
        if not valides:
            return
        trait = valides[0] if len(valides) == 1 else joueur.AskChooseOneText(valides, valides, "Choose a team trait")
        for p in compte[trait]:
            p.GainUntilPhaseEnd(effect, attack=2, end_phase="Player")

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            teamwork,
        ).SetPlay().SetLabel(),
    ]
