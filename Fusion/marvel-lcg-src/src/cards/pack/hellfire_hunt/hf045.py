from . import *

# Rally the Survivors (manigance annexe de campagne, scenario 5 Cassandra Nova). Victory 1.
# While this side scheme is in the victory display, each campaign ally gains +1 THW, +1 ATK, and +1 hit-point.
# When Defeated: The player who defeated this scheme takes a card from the Recruited Mutants deck and put it into play under their control.
# Then, if there still has card in the Recruited Mutants deck, place 5 threat here.
#
# Cartes de reference : 40006 (`GiveKeywordToInPlayWhenApplyThis(..., works_in_the_victory_display=True)`, environment.py:66),
# `RecruitedMutants` (__init__.py, E2).
# ⚠ « each CAMPAIGN ally » : les allies RECRUITED ; « THEN, if there still has card » : seulement si le deck n'est pas vide APRES la mise en jeu.
# ⚠ « place 5 threat HERE » : la manigance RESTE EN JEU (elle n'est pas defaite) : le texte pose les menaces sur CETTE carte, qui ne peut donc pas partir
# en pile de victoire. On le rend par une Interruption forcee sur `WhenSchemeWouldBeDefeated` (modele `CardCannotLeavePlayWhile`, defeated.py :
# `message.SetBeInstead(effect)`) au lieu d'un « When Defeated » : la carte est prise dans le deck, et la defaite est REMPLACEE tant qu'il reste des cartes ;
# quand le deck est vide, la defaite se deroule normalement (pile de victoire, l'effet de la carte s'y applique). Le joueur est celui dont c'est le tour.
def GetAbilities() -> Sequence['Ability']:
    def rally(effect: 'Effect', message: 'Message.WhenSchemeWouldBeDefeated') -> None:
        this = effect.this.CastTo(EncounterSideScheme)
        joueur = effect.world.GetCurrentPlayer()
        deck, _ = RecruitedMutants(effect)
        face = deck.GetTop()
        if face is not None:
            face.PutIntoPlay(joueur, effect, under_control=True)
        if deck.GetSize() > 0:
            message.SetBeInstead(effect)
            this.PlaceThreatOnSchemes([this], 5, effect)

    return [
        *PermissionDeJouerLesRecrutes(),
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            CardFinder(card_type=Ally, trait="RECRUITED"),
            works_in_the_victory_display=True,
            thwart=1,
            attack=1,
            health=1,
        ),
        Ability(
            AbilityType.ForcedInterrupt,
            Message.WhenSchemeWouldBeDefeated,
            [lambda effect, message: message.trigger == effect.this],
            rally,
        ),
    ]
