from . import *

# Arch-Enemy's Face — ATTACHEMENT (ensemble Veranke).
# CONDITION.
# Attached minion gains the SKRULL trait.
# When Revealed: If your nemesis minion is in play, attach this card to it. Then, it activates against
#   you. Otherwise, find your nemesis minion, reveal it and attach this card to it.
#
# Cartes de reference :
#  - « Attached minion gains the SKRULL trait » : `AbilityFactory.GiveKeywordToAttached(trait="SKRULL")`.
#  - « If your nemesis minion is in play, attach... Then it activates against you. Otherwise, find your
#    nemesis minion, reveal it and attach » : modele `skrull_menace/standard_skrull/sk255.py` (meme
#    mecanique nemesis, `CardFinder(card_type=Minion, is_nemesis=joueur)` + `Find.FindAndReveal` +
#    `DoActivate`).
#
# ⚠ Mots-pieges : « attach this card to it » se fait dans LES DEUX branches (deja en jeu OU trouve) ;
# « Then, it activates against you » ne vaut QUE pour la branche « deja en jeu » (le sbire nouvellement
# revele ne s'active pas ce tour-ci, texte muet sur ce point dans cette branche) ; « YOUR nemesis minion »
# = celui du joueur qui revele.


def GetAbilities() -> Sequence['Ability']:

    def revelee(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Attachment)
        joueur = message.GetToPlayer()
        if joueur is None:
            return
        finder_sbire = CardFinder(card_type=Minion, is_nemesis=joueur)
        sbire = Worlds.FindCardOnField(effect, finder=finder_sbire)
        if sbire is not None:
            this.AttachTo2(sbire, effect)
            sbire.CastTo(Minion).DoActivate(joueur, effect)
        else:
            trouve = Find.FindAndReveal(effect, joueur, finder=finder_sbire)
            if trouve is not None:
                this.AttachTo2(trouve, effect)

    return [
        *AbilityFactory.GiveKeywordToAttached(trait="SKRULL"),
        AbilityFactory.WhenThisRevealed(None, revelee),
    ]
