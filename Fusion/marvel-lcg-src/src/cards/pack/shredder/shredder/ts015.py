from . import *

# Disarming Assault (x2) — TRAITRISE. 1 icone de boost + etoile.
# When Revealed: Shredder attacks you. Do not give Shredder any boost cards for
#   this activation. If this attack deals damage to you, discard a WEAPON you control.
# [star] Boost: Discard a WEAPON you control.
#
# Cartes de reference : `aoa four_horsemen` (`DoActivate(..., do_not_give_boost=
# True)` ; ici `DoAttackYou(property=AttackProperty(do_not_give_boost=True))`,
# l'attaque seule) ; `if_characters_damaged_by_this` (do_attack) pour « deals
# damage to YOU » ; `Caught Off Guard 01188` (`player.DiscardControlCards`).
#
# Mots-pieges : « attacks YOU » (l'identite du joueur) ; « deals damage to YOU »
# : l'IDENTITE doit etre blessee (un allie qui encaisse ne compte pas) ; « a
# WEAPON you control » (trait WEAPON, jamais le trait KATANA seul) ; « if you
# cannot » absent : sans arme, rien ne se passe.


def GetAbilities() -> Sequence['Ability']:

    def defausser_arme(effect: 'Effect', joueur: 'Player') -> None:
        joueur.DiscardControlCards(effect, control=True, finder=CardFinder(trait="WEAPON"))

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()

        def blesse(unites) -> None:
            if joueur.GetIdentity() in unites:
                defausser_arme(effect, joueur)

        ShredderAttaqueSansBoost(effect, joueur, if_characters_damaged_by_this=blesse)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        defausser_arme(effect, message.GetToPlayer())

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
