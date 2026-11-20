from . import *

# Chamber of Vile Secrets (2B) — MANIGANCE PRINCIPALE, stade 2. Menace cible 9 par joueur, depart 1 par joueur, escalade +1 par joueur.
# When Revealed : In expert mode, the villain activates against each player.
# Forced Response : After you or an ally you control thwarts this scheme, reveal the top card of the trap deck. (Limit once per round per player.)
# If this stage is completed, the players lose the game.
# (Non imprime, regle du jeu : le vilain Dark Protege vaincu = les joueurs gagnent ; le moteur ne le declare pas seul tant que d'autres vilains sont de cote.)
#
# Cartes de reference : shadowland/shadows_in_the_night/sl001b (victoire a la defaite du vilain : `Worlds.SetGameOver(True)`), dazzler/dz006 (`DoActivate`-like),
# hunting_season/trap (`LimiteParJoueurEtParRound` : limite « une fois par round et par joueur » sur un declencheur sans joueur cible), mc16/`AfterUnitThwartScheme`
# (thwart.py). La phrase « If this stage is completed » est native (`MainScheme.GetAbilities`).
# ⚠ Mots-pieges : « you OR AN ALLY YOU CONTROL thwarts » : un personnage d'un joueur (identite ou allie), jamais un sbire ni une carte sans personnage ; le joueur qui revele
#  le piege est CELUI dont le personnage a contre ; « once per round PER PLAYER » : une fois par joueur, pas globale ; expert : le vilain active contre CHAQUE joueur.


def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        Unused(message)
        if not Worlds.IsExpert(effect):
            return
        vilain = Worlds.FindVillain(effect)
        if vilain is None:
            return
        Players.ForEachPlayer(effect, lambda joueur: vilain.DoActivate(joueur, effect))

    def joueur_du_contre(message: 'Message.AfterUnitThwartScheme') -> 'Player|None':
        joueur = message.trigger.GetControlByPlayer()
        return joueur if joueur is not None and Player.IsType(joueur) else None

    def limite_libre(effect: 'Effect', message: 'Message.AfterUnitThwartScheme') -> bool:
        joueur = joueur_du_contre(message)
        return joueur is not None and LimiteParJoueurEtParRound(effect, joueur, "sl039b", 1, consommer=False)

    def contre(effect: 'Effect', message: 'Message.AfterUnitThwartScheme') -> None:
        joueur = joueur_du_contre(message)
        LimiteParJoueurEtParRound(effect, joueur, "sl039b", 1, consommer=True)
        ReveleDuPaquetPiege(effect, joueur)

    def vilain_vaincu(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> None:
        Worlds.SetGameOver(True, effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
        AbilityFactory.AfterUnitThwartScheme(AbilityType.ForcedResponse, None, "This", contre, remove_threat=True, conditions=[limite_libre]),
        AbilityFactory.WhenUnitBeDefeated(AbilityType.NonKeywordBold, Villain, vilain_vaincu),
    ]
