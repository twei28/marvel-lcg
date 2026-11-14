from . import *

# Conditioned by the Hand — OBLIGATION d'Elektra (ELEKTRA 1/1). 2 icones de boost.
# Give to the Elektra Natchios player.
# Forced Response (Hero): After the player phase ends, deal 3 damage to another identity or ally in play.
# Alter-Ego Action: Exhaust your identity -> discard this card.
#
# SOURCE : texte releve par un joueur sur la carte (14/11/2026) ; pas de scan officiel au depot (image maison).
#
# CARTES DE REFERENCE
#  - `aos/maria_hill/50029` Press Conference : MEME structure (obligation qui reste chez son joueur,
#    `AfterPhaseEnd(ForcedResponse, "Player")` + `PlayerActionToDiscardThis(AlterEgoAction)` au cout `Exhaust("YourIdentity")`).
#  - `luke_cage_nemesis/62028` Internal Injury : degats infliges par l'obligation (`this.DealDamage`).
#  - choix d'une carte par un joueur dans une reponse forcee de fin de phase : `batgirl_nemesis/bg016` (`AskChooseFace`).
#
# TEXTE CONTRE CODE
#  ⚠ « (Hero) » : ne part que si le joueur d'Elektra est en forme HEROS a la fin de la phase des joueurs.
#  ⚠ « ANOTHER identity » : jamais l'identite d'Elektra elle-meme. « or ALLY in play » : tout allie en jeu, les siens
#    comme ceux des autres joueurs. Seule en jeu et sans allie : aucune cible, rien ne se passe.
#  ⚠ Forcee : s'il existe une cible, le joueur d'Elektra DOIT en choisir une (pas de « may »).
#  ⚠ « deal 3 damage » : degats ordinaires (un statut Tenace les absorbe), infliges par cette carte.
#  ⚠ « ALTER-EGO Action » + « Exhaust your identity » (cout) : impossible en heros ou identite deja inclinee.
#  ⚠ « DISCARD this card » : defausse de rencontre (pas retiree du jeu).

DEGATS = 3


def GetAbilities() -> Sequence['Ability']:

    def conditionnee(effect: 'Effect', message: 'Message.AfterPhaseEnd') -> None:
        this = effect.this.CastTo(Obligation)
        joueur = this.GetGaveToPlayer()
        if joueur is None or not joueur.IsInHeroForm():
            return
        cibles: List['CardFace'] = []
        for autre in Worlds.GetPlayers(effect):
            identite = autre.GetIdentity()
            if autre is not joueur and identite is not None:
                cibles.append(identite)
            cibles.extend(autre.GetControlCardsByType(ally=True))
        if not cibles:
            return
        cible = joueur.AskChooseFace(cibles, effect)
        if cible is not None:
            this.DealDamage([cible], DamageProperty(damage=DEGATS), effect)

    return [
        AbilityFactory.AfterPhaseEnd(
            AbilityType.ForcedResponse,
            "Player",
            conditionnee,
        ),
        AbilityFactory.PlayerActionToDiscardThis(
            AbilityType.AlterEgoAction,
        ).SetCostFunc(CostFunc.Exhaust("YourIdentity")),
    ]
