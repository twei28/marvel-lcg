from . import *

# Misdiiirection — AMELIORATION d'aspect PROTECTION, cout 1, RES [mental].
# PREPARATION. Max 1 per player.
# Hero Response: After you defend against an enemy attack and take no damage,
#   discard this card -> deal damage to a different enemy equal to the
#   attacking enemy's ATK.
#
# ⚠ « MISDIIIRECTION » EST LA COQUILLE IMPRIMEE de l'auteur (trois i). Sa
# propre decklist ecrit pourtant « Misdirection ». Le nom de la carte garde ce
# qui est IMPRIME.
#
# CARTE DE REFERENCE
#  - `09020` Unflappable (pack drs) : le montage EXACT de la fenetre —
#    `AfterUnitDefendAgainstAttack(Response, "You", op, take_no_damage=True)`.
#    Son module porte meme la note officielle : « after you defend against an
#    attack and take no damage » se verifie APRES la resolution de l'attaque,
#    et ne regarde PAS si des degats ont ete pris pendant.
#
# TEXTE CONTRE CODE
#  ⚠ « Max 1 per player » : base native `desc.MaxPerUnit`, aucun module.
#  ⚠ « a DIFFERENT enemy » : pas celui qui attaquait. La cible se choisit
#    parmi TOUS les ennemis (`SetTarget(Enemy)` — l'attaquant n'est connu qu'a
#    la resolution, pas a la selection), et l'attaquant est ecarte a ce
#    moment-la. Un seul ennemi en jeu : rien n'est inflige.
#  ⚠ « equal to the ATTACKING ENEMY'S ATK » : l'ATQ de l'attaquant AU MOMENT
#    de l'attaque, modificateurs compris — d'ou la lecture sur la carte, pas
#    sur le papier.
#  ⚠ Un seul ennemi en jeu : il n'y a pas de « different enemy », la carte ne
#    se defausse pas pour rien.


def GetAbilities() -> Sequence['Ability']:

    def detournement(effect: 'Effect', message: 'Message.AfterUnitDefendEnd') -> None:
        this = effect.this.CastTo(Upgrade)
        attaquant = message.attacker
        if attaquant is None:
            return
        # ⚠ L'ATQ se lit sur la CARTE, pas sur le papier : `attack` rend la
        # valeur courante, modificateurs compris, ce que dit « the attacking
        # enemy's ATK ».
        degats = attaquant.CastTo(Unit2).attack
        cibles = [c for c in effect.targets
                  if c is not None and c is not attaquant]
        if cibles and degats > 0:
            this.DealDamage(cibles, degats, effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard("Players"),
        AbilityFactory.AfterUnitDefendAgainstAttack(
            AbilityType.HeroResponse,
            "You",
            detournement,
            take_no_damage=True,
        ).SetCostFunc(CostFunc.Discard("This"))
        .SetTarget(Enemy),
    ]
