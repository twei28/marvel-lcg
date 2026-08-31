from . import *

# * Ghost Agatha — soutien PERSONA, mis de cote a la mise en place (aa001b).
# Permanent. The first player controls Ghost Agatha.
# Action: Exhaust Ghost Agatha -> look at the top 3 cards of your deck.
#   Draw 1 of them, discard 1 of them, and place 1 of them back on top of
#   your deck.
#
# Cartes de reference (RECETTES-MOTEUR) :
#  - Permanent : desc, base automatique (fiche permanent.md) ;
#  - le tri : 51016 (`LookAtDeck` + `AskChooseFaces`) — trois choix
#    successifs : pioche, defausse, la troisieme reste dessus ;
#  - « The first player controls » : la carte entre en jeu chez son
#    PROPRIETAIRE (le joueur elimine, cf. aa001b) mais « your deck » se lit
#    du point de vue du CONTROLEUR — regle du pack (agatha-rules.png) : elle
#    sert le premier joueur une fois sa proprietaire eliminee. En pratique
#    l'action est offerte au controleur courant et fouille SON deck.
#
# ⚠ Si la proprietaire n'est PAS eliminee (mise en jeu par un effet de test),
# le controleur reste le joueur courant : le transfert « premier joueur »
# n'est force qu'au moment ou la carte entre en jeu apres l'elimination —
# l'`Action` (type neutre, ni Hero ni AlterEgo) reste jouable par le
# controleur quel qu'il soit, fidele au texte qui ne verrouille aucune forme.

def GetAbilities() -> Sequence['Ability']:

    def trier(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Support)
        Unused(this, message)

        initiator = effect.GetInitiator()
        if initiator is None:
            return
        faces = initiator.LookAtDeck(initiator.player_deck, 3, effect)
        if not faces:
            return

        restantes = list(faces)
        piochees = initiator.AskChooseFaces(restantes, (1, 1), effect,
                                            prompt="Draw 1 of them")
        if piochees:
            initiator.GainCard(list(piochees), effect)
            restantes = [f for f in restantes if f not in piochees]
        if restantes:
            defaussees = initiator.AskChooseFaces(restantes, (1, 1), effect,
                                                  prompt="Discard 1 of them")
            if defaussees:
                Faces.DiscardAll(list(defaussees), effect)
        # la derniere reste sur le dessus du deck : rien a faire, regarder
        # n'est pas deplacer (lecon ag004)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            trier
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
