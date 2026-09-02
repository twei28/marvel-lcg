from . import *

# Insubstantial Flight — AMELIORATION signature, x1 (n/15 = 14).
# SUPERPOWER. Cout 2, ressource [energy], Requirement ([energy]).
# You gain the [[AERIAL]] trait.
# Hero Response: After your hero exhausts, exhaust Insubstantial Flight ->
#   ready your hero.
#
# Cartes de reference :
#  - ho011 * Goblin Glider (pack harry_osborn) : meme carte, a la lettre —
#    `CanPlayThisUpgradeCard()` + `GiveKeywordToAttached("You",
#    trait="AERIAL")` + une capacite qui redresse le heros par
#    `Faces.ReadyAll([hero], effect)` sous `CostFunc.Exhaust("This")`. Le seul
#    ecart est le declencheur : Hero ACTION chez ho011, Hero RESPONSE ici ;
#  - vr010 Regeneration (meme auteur, Rainy) pour la forme « Response : apres
#    tel evenement, epuiser cette amelioration -> redresser l'identite ».
#
# ⚠ AUCUNE FABRIQUE POUR « After your hero exhausts ». Verifie le 02/09/2026 :
# le message `Message.AfterCardExhausted` existe (sender_card.py:215, emis par
# `Card.Exhaust`, card.py:594) mais AUCUNE fabrique ne l'enveloppe et AUCUNE
# carte du depot ne s'y abonne — vv009 est la premiere. On construit donc
# l'`Ability` a la main, ce qui est un montage etabli du depot (cd008, aa001b,
# dt009, gb001...). Le filtre « ton heros » passe par
# `Condition.CheckWhichCard("YourHero", message.trigger, effect)`, le litteral
# `CARD_TYPE_EX` prevu pour ca (card_type.py:29).
#
# ⚠ AUCUN script pour le `Requirement` : `desc.Requirement` = "Y", base
# automatique (voir mots-cles/requirement.md).
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « YOU gain the [[AERIAL]] trait » : « you » = l'IDENTITE, donc
#    `GiveKeywordToAttached("You", ...)` et non `(Hero, ...)`. Le trait
#    disparait tout seul si l'amelioration quitte le jeu, `GiveKeywordToAttached`
#    etant continu par construction.
#  - « After your HERO exhausts » : le heros, jamais l'alter-ego ni un allie.
#    D'ou le filtre `"YourHero"` et le type `HeroResponse`.
#  - « exhausts » sans complement : N'IMPORTE quel epuisement du heros —
#    attaque de base, menee de base, defense de base, ou un epuisement paye en
#    COUT par une autre carte. On ne filtre donc PAS sur le pouvoir employe.
#  - « exhaust Insubstantial Flight -> » : la fleche fait de l'epuisement un
#    COUT. La reponse ne se propose donc pas si la carte est deja inclinee, ce
#    qui plafonne le redressement a une fois par round.
#  - « ready YOUR HERO » : le meme heros que celui qui vient de s'epuiser,
#    c'est-a-dire `message.trigger`.
#  - Pas de boucle possible : redresser n'emet pas `AfterCardExhausted`, et le
#    cout d'epuisement de la carte porte sur l'AMELIORATION, dont le message
#    est ecarte par le filtre `"YourHero"`.


def GetAbilities() -> Sequence['Ability']:

    def ton_heros(effect: 'Effect', message: 'Message.AfterCardExhausted') -> bool:
        return Condition.CheckWhichCard("YourHero", message.trigger, effect)

    def redresser(effect: 'Effect', message: 'Message.AfterCardExhausted') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)

        heros = message.trigger
        if heros is not None:
            Faces.ReadyAll([heros], effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        *AbilityFactory.GiveKeywordToAttached(
            "You",
            trait="AERIAL",
        ),
        Ability(
            AbilityType.HeroResponse,
            Message.AfterCardExhausted,
            [ton_heros],
            redresser,
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
