from . import *

# Behind the Scenes — traitrise NEMESIS. Boost 1.
# When Revealed: Discard the top card of your deck. Then, discard each card
#   from your hand that is of the same card type as that discarded card. If no
#   card was discarded from your hand this way, this card gains surge.
#
# Cartes de reference :
#  - `06030` Trickster / `16152` Contingency Plan pour
#    `player.DiscardDeckTopCards(1, effect)` : la methode rend les faces
#    reellement defaussees, ce qui permet de savoir laquelle.
#  - `ag013` Hallucination (pack agent_13) pour l'idiome global
#    `ThisCardGainSurge(effect)` en cas d'echec.
#  - `FacesCounter.GetDifferentTypesCount` (faces_counter.py:9) montre que le
#    moteur identifie un « card type » par `type(face)` : c'est la meme
#    comparaison qui est faite ici.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « **that** discarded card » : LA carte qui vient d'etre defaussee du
#    deck, pas un type au choix (piege `that <nom>`).
#  - « discard **each** card from your hand that is of the same card type » :
#    TOUTES les cartes du meme type, pas une. Une main de quatre evenements
#    part entierement si le dessus du deck est un evenement.
#  - « **your** deck », « **your** hand » : le joueur a qui la traitrise est
#    revelee, pas le premier joueur.
#  - « If **no card was discarded from your hand** this way » : la condition
#    de Surge porte sur la MAIN, pas sur le deck. Un deck vide donne donc
#    aussi Surge, puisque rien ne peut alors partir de la main — les deux
#    chemins se rejoignent, mais il faut les couvrir tous les deux.
#  - Une main vide donne Surge. Une main qui ne contient pas ce type aussi.


def GetAbilities() -> Sequence['Ability']:

    def behind_the_scenes(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        Unused(this)

        joueur = message.GetToPlayer()
        if joueur is None:
            ThisCardGainSurge(effect)
            return

        defaussees = joueur.DiscardDeckTopCards(1, effect)
        if not defaussees:
            ThisCardGainSurge(effect)
            return

        type_reference = type(defaussees[0])
        de_la_main = [
            face for face in list(joueur.hand_cards.Get())
            if type(face) is type_reference
        ]
        if not de_la_main:
            ThisCardGainSurge(effect)
            return

        Faces.DiscardAll(de_la_main, effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            behind_the_scenes,
        ),
    ]
