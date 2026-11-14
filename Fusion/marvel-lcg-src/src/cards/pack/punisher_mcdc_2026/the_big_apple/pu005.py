from . import *
from cards.pack.fne import PeutCouvrirLeCout

# The City — ENVIRONNEMENT. Setup. Permanent.
# • Players mark their location in the city with a token, starting in Midtown.
# • Players can only interact with locations (abilities & cards attached) they occupy.
# Action: Exhaust a character you control or spend 1 resource of any type → move to an adjacent (↔ or ↕) location.
#
# Cartes de reference : mu004 (Graffitied Streets : environnement a Action payee par `CostFunc.Exhaust("YouControlUnit")`),
# fne/art_museum_heist/60127 (choix payant : `ForChoiceAbilityWithCost` + `PeutCouvrirLeCout`), gmw/16073b (`SetTarget(lambda effect: ...)` :
# la cible est choisie dans une liste calculee), brique `Ville` (spec M1/M2).
# ⚠ Les deux premieres puces sont des regles de MISE EN PLACE et d'acces : la position de depart est posee par `Ville.Installer`
# (scenario) et l'acces aux lieux par `Ville.AuLieu` sur chaque carte de lieu ; elles n'ont pas de capacite propre.
# ⚠ « Exhaust a character you control OR spend 1 resource » : UNE seule Action, nommee « Move » (« Se deplacer » a l'ecran) ; le joueur choisit
# d'abord la case voisine, puis COMMENT PAYER (deux choix : epuiser un personnage, ou depenser 1 ressource). Avant le 22/10/2026 : deux Actions
# jumelles affichees « Action » et « Action_1 », sans libelle clair, et le pilote bloquait sur la seconde quand la main etait vide. Une branche
# impayable n'est pas offerte ; si aucune n'est payable, l'Action n'est pas offerte. Pas de limite par round (FAQ du livret).


def GetAbilities() -> Sequence['Ability']:

    def voisins(effect: 'Effect') -> Sequence['CardFace']:
        etat = Ville.Etat(effect)
        joueur = effect.GetInitiator()
        case = None if etat is None else Ville.Case(effect, joueur)
        if etat is None or case is None:
            return []
        return [etat.cases[v] for v in Ville.Adjacentes(effect, case)]

    def se_deplacer(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        Unused(message)
        cibles = effect.targets
        if not cibles:
            return
        case = Ville.CaseDe(effect, cibles[0])
        if case is None:
            return
        joueur = effect.GetInitiator()

        def deplacer() -> None:
            Ville.Deplacer(effect, joueur, case)

        def epuiser(targets: Sequence['CardFace']) -> None:
            Faces.ExhaustAll(targets, effect)
            deplacer()

        def depenser(targets: Sequence['CardFace'], res: 'Resources') -> None:
            deplacer()

        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility("Exhaust a character you control", epuiser).SetTarget("YouControlUnit", canbe_exhaust=True),
            AbilityFactory.ForChoiceAbilityWithCost(
                Cost("1"), "Spend 1 resource of any type", depenser,
                conditions=[lambda e, m: PeutCouvrirLeCout(joueur, e, Cost("1"))]),
        )

    def ville_en_place(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> bool:
        Unused(message)
        return Ville.Etat(effect) is not None

    def un_cout_payable(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> bool:
        Unused(message)
        joueur = effect.GetInitiator()
        prets = [c for c in joueur.GetControlCharacters() if c.CanExhaust()]
        return bool(prets) or PeutCouvrirLeCout(joueur, effect, Cost("1"))

    return [
        AbilityFactory.WhenInYourPlayTurn(AbilityType.Action, se_deplacer, conditions=[ville_en_place, un_cout_payable])
        .SetTarget(voisins, is_optional=False)
        .SetName("Move"),
    ]
