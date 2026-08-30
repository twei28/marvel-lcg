from . import *

# Inescapable Horror (1/2) — trahison nemesis de Wiccan (3/5)
# When Revealed: Deal 1 damage to each friendly character. If Moridun is in
#   play, you are stunned.
# [star] Boost: Deal 1 damage to each friendly character you control.
#
# Exemplaire physique 1 de 2 (wc021, wc022 : meme texte, deux card_id
# distincts — meme choix de design qu'il021/il022 chez le meme auteur).
# Commentaire complet ici, pointeur bref sur wc022.
#
# DEUX PORTEES DIFFERENTES, a ne surtout pas confondre (piege `each` et piege
# `you control` de PROCESSUS-CARTE) :
#   - When Revealed : « each friendly character » NU -> TOUS les personnages
#     amis de la table, `Worlds.GetOnFieldFriendlyCharacters(effect)`
#     (worlds.py:289 = identites + allies de TOUS les joueurs) ;
#   - Boost : « each friendly character YOU CONTROL » -> le seul joueur qui
#     revele, `[player.GetIdentity()] + player.allies.Get()`.
# L'auteur a explicitement ecrit « you control » sur la seule capacite Boost :
# la difference est voulue, pas une coquille.
#
# « Deal 1 damage » -> `this.DealDamage(faces, 1, effect)`, sans `property` :
# ce n'est pas une attaque, aucune riposte, aucun ranged.
#
# « If Moridun is in play, you are stunned » -> `MoridunEnJeu(effect)` (aide
# du pack) puis `Faces.GiveStatus([identite], "Stunned", effect)`. « you » =
# le joueur qui revele la carte, `message.GetToPlayer()` — jamais le premier
# joueur, jamais tous. Modele du statut sur le releveur : 56177 Venom Blast.
#
# [star] Boost -> `AbilityFactory.WhenCardBecomeBoost("This", ...)`, l'idiome
# du depot (modeles 56177 Venom Blast, 16140 Sound the Alarms).

def GetAbilities() -> Sequence['Ability']:

    def inescapable_horror(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)

        personnages = Worlds.GetOnFieldFriendlyCharacters(effect)
        if personnages:
            this.DealDamage(personnages, 1, effect)

        if not MoridunEnJeu(effect):
            return

        player = message.GetToPlayer()
        if player is None:
            return
        identite = player.GetIdentity()
        if identite is not None:
            Faces.GiveStatus([identite], "Stunned", effect)

    def inescapable_horror_boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        this = effect.this.CastTo(Treachery)

        player = message.GetToPlayer()
        if player is None:
            return

        personnages: List['CardFace'] = []
        identite = player.GetIdentity()
        if identite is not None:
            personnages.append(identite)
        personnages += list(player.allies.Get())

        if personnages:
            this.DealDamage(personnages, 1, effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            inescapable_horror,
        ),
        AbilityFactory.WhenCardBecomeBoost(
            "This",
            inescapable_horror_boost,
        ),
    ]
