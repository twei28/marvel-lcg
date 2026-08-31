from . import *

# * Hela — sbire nemesis. ASGARD. ELITE. MYSTIC. PV 4 / SCH 2 / ATK 2.
# While there are other minions in play, Hela may not take damage.
# Forced Interrupt: When you defeat a minion, discard a card from your hand.
# (Angela's nemesis minion.)
#
# ⚠ CETTE CARTE EST LE CONTRE EXACT DU PACK. Angela gagne a tuer des sbires
# (an001a, an004, an007, an009) : Hela lui fait defausser une carte a CHAQUE
# sbire vaincu, et se rend intouchable tant qu'un autre sbire est en jeu. Le
# joueur doit donc vider le plateau AVANT de pouvoir la frapper — en payant
# une carte par sbire.
#
# Carte de reference : 05027 * Thomas Edison (pack msm), jumeau presque
# parfait — « cannot take damage while you are engaged with another minion »,
# rendu par `AbilityFactory.ThisCannotTakeDamageWhile(conditions=[...])`.
# Difference : Edison regarde les sbires ENGAGES avec le joueur, Hela dit
# « other minions IN PLAY », donc on balaie tout le plateau.
#
# ⚠ « OTHER minions » : Hela elle-meme ne compte pas. Sans le filtre, elle
# serait invulnerable en permanence, y compris seule en jeu.
# ⚠ « When YOU defeat a minion » : c'est le joueur engage, pas n'importe qui.

def GetAbilities() -> Sequence['Ability']:

    def autres_sbires_en_jeu(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> bool:
        this = effect.this
        Unused(message)
        autres = [f for f in Worlds.FindCardsOnField(effect, card_type=Minion)
                  if f is not this]
        return len(autres) > 0

    def hela(effect: 'Effect', message: 'Message.AfterUnitDefeatedUnit') -> None:
        this = effect.this.CastTo(Minion)
        Unused(this, message)

        joueur = effect.GetInitiator()
        if isinstance(joueur, Player):
            joueur.DiscardHandCards(1, effect)

    return [
        AbilityFactory.ThisCannotTakeDamageWhile(
            conditions=[autres_sbires_en_jeu],
        ),
        AbilityFactory.AfterUnitDefeatedUnit(
            AbilityType.ForcedInterrupt,
            "You",
            Minion,
            hela,
        ),
    ]
