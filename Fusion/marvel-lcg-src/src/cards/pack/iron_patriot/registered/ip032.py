from . import *

# * Penance — SBIRE du deck REGISTERED (19/20). 6 PV, ATQ 4, MNG 1, boost 4.
# AVENGER. ELITE.
# Retaliate 2. Vulnerable.
# [star] Penance's attacks gain overkill.
# Unleashed Pain — Special: Exhaust this card -> choose a player. Deal X damage
#   to the villain and each minion engaged with that player, where X is equal
#   to the amount of damage this ally has sustained.
#
# ⚠⚠ LA CARTE RECOMPENSE SA PROPRE SOUFFRANCE. Vulnerable (les degats qu'elle
# recoit sont doubles) n'est pas un defaut ici, c'est le carburant : plus
# Penance encaisse, plus son « Special » frappe fort. Retaliate 2 l'alimente
# tout seul.
#
# CARTES DE REFERENCE
#  - `16121` Badoon Warlord : `UnitAttackGainKeyword("This", overkill=True)`.
#  - `04006` Explosive Arrow imprime la meme cible et la resout par
#    `.SetTarget("VillainAndEngagedSamePlayerMinion")`. INUTILISABLE ICI :
#    voir la note ci-dessous. On refait donc le geste a la main —
#    `vise.GetEngagedMinions()` plus `Worlds.FindVillain`.
#  ⚠⚠ PAS DE `.SetTarget()` SUR CETTE CARTE. Le moteur l'interdit aux ENNEMIS :
#    `Ability.Initialize` leve `assert self.selectors == []` des que la face
#    est un `Enemy` (ability.py:168), et les cartes du deck REGISTERED sont
#    chargees comme des SBIRES. La cible se demande donc DANS l'operation, par
#    `joueur.AskChooseFaces`. Mesure du 09/09/2026, sur `ip021`.
#
# TEXTE CONTRE CODE
#  ⚠ « the amount of damage THIS ALLY HAS SUSTAINED » : les degats encaisses,
#    `sustained` (can_health.py:89), et non les points de vie manquants au
#    maximum. Les deux coincident tant que rien ne change ses PV max — mais
#    c'est `sustained` qui est ecrit.
#  ⚠ « Exhaust this card -> » : COUT.
#  ⚠ Penance a 0 degat encaisse : la carte se resout et ne fait rien. C'est
#    coherent, on ne l'interdit pas.
#  ⚠ Retaliate 2 et Vulnerable sont des BASES NATIVES de sbire, qui tombent a
#    la conversion. L'allie ne garde que l'overkill et le « Special ».


def GetAbilities() -> Sequence['Ability']:

    def douleur_dechainee(effect: 'Effect', message: 'Message.WhenResolveSpecialAbility') -> None:
        this = effect.this
        Unused(message)
        joueur = effect.GetInitiator()
        degats = this.CastTo(Unit2).sustained
        if joueur is None or degats <= 0:
            return

        # « choose a player » : on passe par les identites en jeu, une par
        # joueur, ce qui EST le choix du joueur en langage de cartes.
        identites = [j.GetIdentity() for j in Worlds.GetPlayers(effect)]
        identites = [i for i in identites if i is not None]
        if not identites:
            return
        choisie = joueur.AskChooseFaces(identites, (1, 1), effect,
                                        prompt="Choose a player")
        if not choisie:
            return
        vise = JoueurQuiControle(choisie[0])
        if vise is None:
            return

        cibles: List['CardFace'] = list(vise.GetEngagedMinions())
        vilain = Worlds.FindVillain(effect)
        if vilain is not None:
            cibles.append(vilain)
        if not cibles:
            return
        this.DealDamage(cibles, degats, effect)

    return [
        AbilityFactory.UnitAttackGainKeyword(
            "This",
            overkill=True,
        ),
        SpecialRegistered("Unleashed Pain", douleur_dechainee)
        .SetCostFunc(CostFunc.Exhaust("This")),
    ]
