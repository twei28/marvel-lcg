from . import *

# * Mongo — SBIRE UNIQUE. BRUTE. FOOT CLAN. NINJA. MNG 0 / ATQ 2 / PV 4, 1 icone de boost + etoile.
# Guard. Retaliate 1.
# [star] Boost: Stun your hero.
#
# Cartes de reference : `01101` (Guard dans `desc`), `01099`/fiche retaliate.md
# (Retaliate dans `desc`) ; `core klaw 01123` Sonic Boom (boost « exhaust your
# hero » : `player.IsHero()` puis action sur `player.GetHero()`) ; `Faces.GiveStatus`
# pour Stunned.
#
# Mots-pieges : « YOUR HERO » : le HEROS du joueur qui subit le boost ; en
# forme alter-ego il n'a pas de heros en jeu : rien ne se passe (meme lecture que
# Sonic Boom). Mongo n'a ni « When Revealed » ni autre capacite.


def GetAbilities() -> Sequence['Ability']:

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        joueur = message.GetToPlayer()
        if joueur is not None and joueur.IsHero():
            Faces.GiveStatus([joueur.GetHero()], "Stunned", effect)

    return [
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
