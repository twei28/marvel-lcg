from . import *

# Lead the Charge — TRAITRISE nemesis. TACTIC. 2 boost. x2.
# When Revealed: Each minion engaged with a player activates against them.
#   Each player who was not activated against this way searches the encounter
#   deck and discard pile for a minion and puts it into play engaged with them.
#   Give each minion a facedown boost card.
#
# CARTES DE REFERENCE
#  - `04070` Crossbones' Assault / `11051` Ancient Grudge :
#    `enemy.DoActivate(player, effect)`, l'activation d'un ennemi contre un
#    joueur donne.
#  - `04111` * Zola (III) : `Search.EncounterCard(effect, player,
#    include_discard_pile=True, card_type=Minion)` + `Players.ForEachPlayer`.
#  - `br011` Hammer Time : `PutIntoPlay(joueur)` + `EngagePlayer(joueur)`.
#  - `sf011` Hand Ambush : `Faces.GiveFacedownBoostCards(faces, 1, effect)`.
#
# TEXTE CONTRE CODE
#  ⚠ « EACH minion engaged with A PLAYER activates AGAINST THEM » -> pour
#    chaque joueur, chacun de ses sbires engages active contre LUI (pas contre
#    le joueur qui a revele la carte). Un sbire non engage n'active pas.
#  ⚠ « Each player who was NOT activated against this way » -> les joueurs
#    sans sbire engage au moment de la revelation. On note qui a ete vise
#    PENDANT la premiere passe, puis on convoque pour les autres.
#  ⚠ « encounter deck AND discard pile » -> `include_discard_pile=True`.
#  ⚠ « puts it into play ENGAGED WITH THEM » -> `PutIntoPlay(joueur)` +
#    `EngagePlayer(joueur)` explicite, comme br011.
#  ⚠ « Give EACH minion a facedown boost card » -> tous les sbires EN JEU a la
#    fin, y compris ceux qui viennent d'arriver, un par sbire.
#  ⚠ La carte revelee par un joueur en forme CIVILE : le sbire qui active
#    complote au lieu d'attaquer, c'est `DoActivate` qui decide.


def GetAbilities() -> Sequence['Ability']:

    def mener_la_charge(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        Unused(this, message)
        vises: set = set()

        def activer(joueur: 'Player') -> None:
            sbires = [m for m in list(joueur.engaged_minions.GetAll())
                      if m is not None and Minion.IsType(m)]
            for sbire in sbires:
                vises.add(joueur)
                if sbire.card.IsOnField():
                    sbire.CastTo(Minion).DoActivate(joueur, effect)

        Players.ForEachPlayer(effect, activer)

        def convoquer(joueur: 'Player') -> None:
            if joueur in vises:
                return
            sbire = Search.EncounterCard(
                effect, joueur,
                include_discard_pile=True,
                card_type=Minion,
            )
            if sbire is not None:
                sbire.PutIntoPlay(joueur, effect)
                if sbire.card.IsOnField():
                    sbire.CastTo(Minion).EngagePlayer(joueur, effect)

        Players.ForEachPlayer(effect, convoquer)

        sbires = [m for m in Worlds.GetOnFieldEnemies(effect)
                  if m is not None and Minion.IsType(m)]
        if sbires:
            Faces.GiveFacedownBoostCards(sbires, 1, effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            mener_la_charge,
        ),
    ]
