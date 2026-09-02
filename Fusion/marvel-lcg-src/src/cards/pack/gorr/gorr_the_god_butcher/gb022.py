from . import *

# Stalking Berserker — SBIRE NECROVERSE a DOS DE CARTE JOUEUR (×4), mis de
# cote au setup. Le complot 3A en melange une copie dans le deck de chaque
# joueur. MNG 0 / ATQ 0 — 2 PV.
#
# Forced Response: After you draw Stalking Berserker or discard it from the
#   top of your deck, reveal it.
# Forced Response: After your turn ends, discard the top 2 cards of your deck
#   and place 1 necro counter on the All-Black Necroverse environment.
# When Defeated: Put this card into the engaged player's discard pile.
#
# ---------------------------------------------------------------------------
# CARTES DE REFERENCE
#
# - Pioche/defausse du dessus qui revele : 45178 et aa007, comme gb021 — les
#   deux cartes a dos joueur du pack partagent ce couple de declencheurs.
# - « After your turn ends » : `AfterPlayerTurnEnd`, le declencheur employe
#   par al001a pour sa Reponse Obligatoire de fin d'activation.
# - « When Defeated: put this card into <une pile> » : jj013 / 01166 pour le
#   `WhenUnitBeDefeated`, et 33027 pour la redirection du rangement.
#
# ---------------------------------------------------------------------------
# TEXTE CONTRE CODE
#
# « After YOUR turn ends » -> le tour du joueur ENGAGE avec ce sbire, pas
#   n'importe quel tour : le sbire ne frappe que son hote.
# « discard the top 2 cards AND place 1 necro counter » -> les deux, pas un
#   choix. Le compteur ne se pose que si l'environnement est sur sa face
#   Necroverse ; sinon rien (le sbire n'arrive qu'a l'etape 3, ou elle l'est).
# « When Defeated: put this card into the ENGAGED PLAYER'S discard pile » ->
#   la defausse du JOUEUR, pas celle de rencontre : comme Heroes' Labor, le
#   sbire revient dans le deck au prochain melange.
# ⚠ MNG 0 / ATQ 0 : il ne fait rien en phase du vilain. Tout son poids est
#   dans la defausse qu'il impose a chaque tour.


def GetAbilities() -> Sequence['Ability']:

    def reveler(effect: 'Effect', message: 'Message2') -> None:
        this = effect.this.CastTo(Minion)

        joueur = this.card.GetOwner()
        if isinstance(joueur, Player):
            this.Reveal(joueur, effect)

    def fin_de_tour(effect: 'Effect', message: 'Message.AfterPlayerTurnEnd') -> None:
        this = effect.this.CastTo(Minion)
        Unused(message)

        joueur = this.GetEngagedPlayer()
        if isinstance(joueur, Player):
            joueur.DiscardDeckTopCards(2, effect)
        PoserNecro(effect, 1)

    def quand_vaincu(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> None:
        this = effect.this.CastTo(Minion)
        Unused(message)

        joueur = this.GetEngagedPlayer()
        if isinstance(joueur, Player):
            Faces.DiscardAll([this], effect, into_area=joueur.discard_pile)

    return [
        AbilityFactory.AfterCardEnterHand(
            AbilityType.ForcedResponse,
            "This",
            reveler,
        ),
        AbilityFactory.AfterCardDiscardInternal(
            AbilityType.ForcedResponse,
            "This",
            reveler,
            from_where="PlayerDeckTop",
        ),
        AbilityFactory.AfterPlayerTurnEnd(
            AbilityType.ForcedResponse,
            "EngagedPlayer",
            fin_de_tour,
        ),
        AbilityFactory.WhenUnitBeDefeated(
            AbilityType.WhenDefeated,
            "This",
            quand_vaincu,
        ),
    ]
