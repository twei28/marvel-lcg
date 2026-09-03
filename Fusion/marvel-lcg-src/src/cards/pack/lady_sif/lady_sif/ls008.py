from . import *

# * Sif's Steed — soutien signature, x1 (n/15 = 12).
# ASGARD. CREATURE. Cout 3, ressource [energy].
# Hero Response: After Lady Sif exhausts, exhaust Sif's Steed -> ready Lady Sif.
# Hero Action: Exhaust Sif's Steed -> ready Lady Sif.
#
# Cartes de reference :
#  - **`vv009` Insubstantial Flight** (pack viv_vision, meme auteur), jumeau
#    de la premiere capacite : le message `Message.AfterCardExhausted` existe
#    (sender_card.py:215) mais **AUCUNE fabrique ne l'enveloppe**. On construit
#    donc l'`Ability` a la main, montage etabli du depot (cd008, aa001b,
#    dt009, gb001), avec le filtre `Condition.CheckWhichCard("YourHero", ...)` ;
#  - `ho011` * Goblin Glider pour la seconde : `WhenInYourPlayTurn(HeroAction)`
#    + `CostFunc.Exhaust("This")` + `Faces.ReadyAll`.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « After Lady Sif EXHAUSTS », sans complement : n'importe quel
#    epuisement — attaque de base, menee de base, defense de base, ou un
#    epuisement paye en COUT par une autre carte. On ne filtre donc PAS sur le
#    pouvoir employe.
#  - « LADY SIF », un nom propre porte par les DEUX faces ici (heros et
#    alter-ego s'appellent pareil). Mais les deux capacites sont `Hero...` :
#    elles n'existent qu'en forme de heros, ou « Lady Sif » ne peut designer
#    que la face heros. D'ou le filtre `"YourHero"`, comme vv009.
#  - Les DEUX capacites paient le meme cout (`exhaust Sif's Steed`) et font la
#    meme chose. La Response est la version gratuite en fenetre, l'Action la
#    version a la demande : une seule des deux part par round, le soutien ne
#    se redressant pas tout seul.
#  - ⚠ AUCUNE BOUCLE : redresser n'emet pas `AfterCardExhausted`, et le cout
#    d'epuisement porte sur le SOUTIEN, dont le message est ecarte par le
#    filtre `"YourHero"`.
#  - Combine a ls004 Lead The Charge et ls006 Valiant Defense, qui n'inclinent
#    pas, ce soutien donne a Lady Sif jusqu'a quatre pouvoirs de base par
#    round — et autant de declenchements de Valiant Warrior.


def GetAbilities() -> Sequence['Ability']:

    def ton_heros(effect: 'Effect', message: 'Message.AfterCardExhausted') -> bool:
        return Condition.CheckWhichCard("YourHero", message.trigger, effect)

    def redresser_apres_epuisement(effect: 'Effect', message: 'Message.AfterCardExhausted') -> None:
        this = effect.this.CastTo(Support)
        Unused(this)

        heros = message.trigger
        if heros is not None:
            Faces.ReadyAll([heros], effect)

    def redresser_a_la_demande(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Support)
        Unused(this, message)

        initiator = effect.GetInitiator()
        if initiator is None:
            return
        heros = initiator.GetHero()
        if heros is not None:
            Faces.ReadyAll([heros], effect)

    return [
        Ability(
            AbilityType.HeroResponse,
            Message.AfterCardExhausted,
            [ton_heros],
            redresser_apres_epuisement,
        ).SetCostFunc(CostFunc.Exhaust("This")),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            redresser_a_la_demande,
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
