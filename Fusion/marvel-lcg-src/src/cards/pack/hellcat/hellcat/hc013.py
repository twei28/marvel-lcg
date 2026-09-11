from . import *
# Mental Episode — OBLIGATION, boost 2. Give to the Patsy Walker player.
# Flip to alter-ego form and discard all cards attached to your identity. Deal
#   1 damage to your identity for each discarded this way. If at least 2 cards
#   were discarded from your identity this way, remove this card from the game.
#   If not, discard this card.
#
# Modeles : ag005 (`identity.ChangeToForm(AlterEgo, effect)` — PAS
# `ChangeForm`, piege nomme), ze012 (obligation `WhenThisRevealed`),
# `Faces.RemoveAllFromGame`. ⚠ « If not, discard this card » DOIT etre code :
# une obligation revelee ENTRE EN JEU dans ce moteur et y reste (vu au harnais
# le 11/09/2026, « hc013 est encore en jeu »).
# ⚠ Relire l'identite APRES le flip : la face change, la zone des cartes
#   glissees est celle de la CARTE (verifie par le cas « survit au flip »).

def GetAbilities() -> Sequence['Ability']:

    def mental_episode(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Obligation)
        joueur = message.GetToPlayer()
        identite = joueur.GetIdentity()
        if Hero.IsType(identite):
            identite.ChangeToForm(AlterEgo, effect)
        identite = joueur.GetIdentity()
        accrochees = CartesAttacheesA(identite)
        n = len(accrochees)
        if n:
            Faces.DiscardAll(accrochees, effect)
            identite.TakeDamage(this, n, effect)
        if n >= 2:
            Faces.RemoveAllFromGame([this], effect)
        else:
            Faces.DiscardAll([this], effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            mental_episode,
        ),
    ]
