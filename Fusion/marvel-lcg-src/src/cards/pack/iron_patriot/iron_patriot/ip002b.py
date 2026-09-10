from . import *

# * Dark Reign — le VERSO de `ip002a` Registration Act. Permanent.
# This scheme does not count against the player side scheme limit.
# Accept Change — Action: Reveal the top card of the REGISTERED deck. You may
#   spend resources equal to the number of boost icons on that card to take
#   control of that minion and treat it as a REGISTERED ally. If you do not, it
#   enters play as a minion engaged with you.
# Minions with the REGISTERED trait are treated as REGISTERED allies. They take
#   1 consequential damage after they attack or thwart, and their THW is equal
#   to their printed SCH.
#
# ⚠ LA SEULE DIFFERENCE AVEC LE RECTO TIENT EN QUATRE MOTS. Registration Act
# fait payer « AT THE END OF THE ROUND » ; Dark Reign fait payer TOUT DE SUITE.
# C'est la recompense d'avoir contre la manigance : on recrute avant que le
# sbire n'ait eu le temps d'agir. Le reste du texte est identique, et le
# montage partage (`RevelerEtProposerLeRecrutement`) le dit mieux qu'un
# commentaire.
#
# ⚠ Pas de « When Defeated » ici : la face est deja retournee, et le texte n'en
# porte pas. Pas de cout ni de menace de depart non plus — c'est un verso.


def GetAbilities() -> Sequence['Ability']:

    def accepter_le_changement(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(PlayerSideScheme)
        Unused(this, message)
        joueur = effect.GetInitiator()
        if joueur is None:
            return
        RevelerEtProposerLeRecrutement(joueur, effect, a_la_fin_du_round=False)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            accepter_le_changement,
        ).SetName("Accept Change"),
    ]
