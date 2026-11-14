from . import *

# Acid Blood — ATTACHEMENT (set « Predator Nemesis »), CONDITION, +1 ATQ, Boost 1.
# Attached minion gains retaliate 1.
# When Revealed: Find the Xenomorph Queen and put it into play engaged with you and attach this card to it.
#
# Cartes de reference :
#  - `GiveKeywordToAttached("AttachedCharacter"...)` : `core/captain_america/03009` (retaliate pour un personnage porteur),
#    `ts007` (`this.AttachTo2(villain, effect)`) pour attacher une carte de rencontre a un sbire ;
#  - `AmenerLaReine` (helper du set) : « find the Xenomorph Queen and put it into play engaged with you ».
#
# ⚠ Mots-pieges :
#  - « +1 ATK » : l'icone imprimee a gauche (« +1 ATQ ») est un bonus du sbire PORTEUR : `GiveKeywordToAttached(..., attack=1)`.
#  - « Attached minion gains retaliate 1 » : constant, tant que l'attachement est en place.
#  - « Find the Xenomorph Queen ... AND attach this card to it » : si la Reine est DEJA en jeu, elle ne peut pas « entrer en jeu »
#    mais la carte s'attache quand meme a elle (sinon l'attachement n'a pas d'hote) ; Reine introuvable : la carte s'attache
#    au sbire engage de son choix, a defaut elle est defaussee.


def GetAbilities() -> Sequence['Ability']:

    def sang_acide(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Attachment)
        Unused(message)
        joueur = message.GetToPlayer() or JoueurDeCetteCarte(effect)
        if joueur is None:
            return
        reine = LaReineEnJeu(effect) or AmenerLaReine(effect, joueur)
        if reine is not None and reine.card.IsOnField():
            this.AttachTo2(reine, effect)
        else:
            Faces.DiscardAll([this], effect)

    return [
        *AbilityFactory.GiveKeywordToAttached(
            "Character",
            attack=1,
            retaliate=1,
        ),
        AbilityFactory.WhenThisRevealed(
            None,
            sang_acide,
        ),
    ]
