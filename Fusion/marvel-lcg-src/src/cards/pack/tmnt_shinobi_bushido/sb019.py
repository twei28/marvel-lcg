from . import *

# * Gusoku — AMELIORATION unique ✦ ARMOR, classe Bushido (Inkwire, TMNT Shinobi). Cout 2, [physical].
# Hero Response: After you use one of your basic powers, exhaust this card and remove 1 samurai counter from an OATH upgrade you
#   control -> ready your hero.
# « This armor has seen many battles. »
#
# Mots-cles (fiches lues AVANT le code) : samurai counter / OATH (samurai-counter.md). Gusoku n'est PAS OATH et n'a pas de Uses.
#
# Cartes de reference :
#  - « After you use a basic power, <cout> -> ready your hero » : `trors/spider_woman/04032` pour le declencheur
#    (`AfterUnitUseBasicPower(HeroResponse, "You", op)`, sans `powers` : un heros compte ATK, THW, DEF) ; « ready your hero »
#    `sm/27016` What Doesn't Kill Me (`SetTarget("YourHero", canbe_ready=True)` : un heros pret n'est pas une cible) ;
#  - cout « remove 1 <compteur> counter from <carte choisie> » : `CostFunc.Counter(Select.From(fn), 1, 'samurai')` (le cout ajoute
#    lui-meme le filtre « porte assez de compteurs » : seules les OATH a compteurs sont proposees) ;
#  - « <amelioration> you control » : `joueur.GetControlUpgrade(CardFinder(trait=...))` (modele `se003`).
#
# TEXTE CONTRE CODE
#  ⚠ « After YOU use ONE OF YOUR BASIC powers » : les pouvoirs de base du HEROS (ATQ, CTR, DEF), pas ceux d'un allie ; Hero Response :
#    forme heros seule.
#  ⚠ « exhaust THIS card AND remove 1 samurai counter FROM AN OATH upgrade YOU control -> » : DEUX couts ; le compteur vient d'une
#    amelioration OATH sous son controle, AU CHOIX (pas de Gusoku, qui n'en porte pas) ; l'OATH qui perd son dernier compteur est
#    defaussee (Uses).
#  ⚠ « ready YOUR HERO » : le heros, qui doit etre incline (precedent 27016) ; une seule reponse par redressement de Gusoku.


def GetAbilities() -> Sequence['Ability']:

    def oaths_sous_controle(effect: 'Effect') -> 'Sequence[CardFace]':
        joueur = effect.GetInitiator()
        if joueur is None:
            return []
        return list(joueur.GetControlUpgrade(CardFinder(trait="OATH")))  # type: ignore

    def gusoku(effect: 'Effect', message: 'Message.AfterUnitUseBasicPower') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this, message)
        Faces.ReadyAll(effect.targets, effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.AfterUnitUseBasicPower(
            AbilityType.HeroResponse,
            "You",
            gusoku,
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetCostFunc(CostFunc.Counter(Select.From(oaths_sous_controle), 1, 'samurai'))
        .SetTarget("YourHero", canbe_ready=True),
    ]
