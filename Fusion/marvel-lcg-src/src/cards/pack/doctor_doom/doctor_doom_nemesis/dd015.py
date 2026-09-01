from . import *

# * Mister Fantastic — sbire nemesis (2/4). FANTASTIC FOUR. GENIUS.
# 4 PV, SCH 2, ATQ 2. Boost 2. Guard. Patrol.
# While Mister Fantastic is engaged with you, each time you generate a
#   [mental] resource, generate a [physical] instead.
# When Revealed: Mister Fantastic engages the Doctor Doom player.
#
# Cartes de reference :
#  - substitution de couleur a la generation : ah001a « Hypermind » (pack
#    totally_awesome_hulk), qui traite TOUTE ressource generee comme du
#    [wild]. Meme montage exact : une `Ability` brute sur
#    `Message.CheckEffectGeneratedResources`, filtree sur le joueur, puis
#    `message.SetResources(...)`. Seule difference : Hypermind convertit tout,
#    Mister Fantastic ne convertit QUE le [mental], et en [physical].
#  - « engages the X player » : 20025 / vp-plotting, `face.EngagePlayer`.
#  - Guard, Patrol et Boost sont des BASES AUTOMATIQUES (`desc`) : aucun
#    module (fiches guard.md / patrol.md).
#
# ⚠ CETTE CARTE EST LE CONTRE-FEU DU PACK. Tout Doctor Doom carbure au
# [mental] : Power Syphon (dd001a), les bonus « paye uniquement en mental »
# (dd004, dd005, dd006), Doom's Mask (dd011) et jusqu'a la ressource a trois
# mentales (dd007). Tant que Mister Fantastic est engage, plus rien de tout
# cela ne se declenche. C'est voulu, et c'est ce qui rend le set nemesis
# redoutable — a ne surtout pas « adoucir » en codant.
#
# ⚠ « While ... ENGAGED WITH YOU » : la substitution ne vaut que pour le joueur
# avec lequel il est engage, pas pour toute la table.
#
# ⚠ « each time you GENERATE » : c'est la production qui change de couleur, pas
# le cout ni les icones imprimees. Une carte qui PORTE une icone mentale reste
# mentale ; seule une capacite qui produit du mental produit du physique.

def GetAbilities() -> Sequence['Ability']:

    def mental_devient_physique(effect: 'Effect',
                                message: 'Message.CheckEffectGeneratedResources') -> None:
        res = message.res
        if res.val <= 0:
            return
        mental = res.GetColor("B", convert_green_res=False)
        if mental <= 0:
            return
        # On ne touche QUE la part mentale : le reste de la production est
        # rendu tel quel. `Hypermind` peut se permettre de tout remplacer,
        # pas nous.
        nouveau = res.Copy()
        nouveau -= Resources("B") * mental
        nouveau += Resources("R") * mental
        message.SetResources(nouveau, effect)

    def engage_avec_ce_sbire(effect: 'Effect',
                             message: 'Message.CheckEffectGeneratedResources') -> bool:
        this = effect.this.CastTo(Minion)
        joueur = message.GetToPlayer()
        return joueur is not None and this.GetEngagedPlayer() == joueur

    def engage_le_joueur_doom(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Minion)

        for player in Worlds.GetPlayers(effect):
            identite = player.GetIdentity()
            if identite is not None and identite.IsName("Doctor Doom", check_all_face=True):
                this.EngagePlayer(player, effect)
                return

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            engage_le_joueur_doom,
        ),
        Ability(
            AbilityType.NonKeyword,
            Message.CheckEffectGeneratedResources,
            [engage_avec_ce_sbire],
            mental_devient_physique,
        ),
    ]
