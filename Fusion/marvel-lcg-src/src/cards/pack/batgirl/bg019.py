from . import *

# Birds of a Feather — evenement Basic, cout 2, [wild]. « Team-Up (any combination of Batgirl, Black Canary, or Huntress). Max 1 per
# deck. Hero Action: Choose X options below (you may choose the same option multiple times), where X is the number of [[BIRD OF PREY]]
# characters in play: • deal 3 damage to an enemy. • remove 3 threat from a scheme. • stun an enemy. »
# Cartes de reference : `hc022` Divas (Team-Up « any 2 of » : pas de `desc.TeamUp`, condition ecrite a la main), `ma009` (ChooseAbilities).
# ⚠ Team-Up « any combination » : au moins DEUX des trois personnages nommes en jeu (cote joueur) ; X = personnages [[BIRD OF PREY]].

NOMS_EQUIPE = ("Batgirl", "Black Canary", "Huntress")


def ChoisirUnEnnemi(joueur: 'Player', effect: 'Effect') -> 'CardFace|None':
    ennemis = Worlds.GetOnFieldEnemies(effect)
    if not ennemis:
        return None
    return joueur.AskChooseFace(ennemis, effect)


def GetAbilities() -> Sequence['Ability']:

    def personnages(effect: 'Effect'):
        return Worlds.GetOnFieldFriendlyCharacters(effect)

    def deux_en_jeu(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> bool:
        presents = set()
        for perso in personnages(effect):
            for nom in NOMS_EQUIPE:
                if perso.IsName(nom, check_all_face=True):
                    presents.add(nom)
        return len(presents) >= 2

    def birds_of_a_feather(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        joueur = effect.GetInitiator()
        if joueur is None:
            return
        x = sum(1 for perso in personnages(effect) if perso.HasTrait("BIRD OF PREY"))

        def degats(targets) -> None:
            cible = ChoisirUnEnnemi(joueur, effect)
            if cible is not None:
                this.DealDamage([cible], 3, effect)

        def menace(targets) -> None:
            schemes = [f for f in Worlds.GetOnFieldCards(effect) if Scheme2.IsType(f) and f.threat > 0]
            cible = joueur.AskChooseFace(schemes, effect) if schemes else None
            if cible is not None:
                this.RemoveThreatFromSchemes([cible], 3, effect)

        def sonner(targets) -> None:
            cible = ChoisirUnEnnemi(joueur, effect)
            if cible is not None:
                Faces.GiveStatus([cible], "Stunned", effect)

        for _ in range(x):
            joueur.ChooseAbilities(
                effect,
                AbilityFactory.ForChoiceAbility("Deal 3 damage to an enemy", degats).SetHasNoTargetEffect(),
                AbilityFactory.ForChoiceAbility("Remove 3 threat from a scheme", menace).SetHasNoTargetEffect(),
                AbilityFactory.ForChoiceAbility("Stun an enemy", sonner).SetHasNoTargetEffect(),
            )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            birds_of_a_feather,
            conditions=[deux_en_jeu],
        ).SetPlay(),
    ]
