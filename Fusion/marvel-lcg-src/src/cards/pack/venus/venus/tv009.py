from . import *

# * Arcane Emitting Diode — AMELIORATION, cout 2, [wild]. ELEMENT. SUPERPOWER. x1.
# Hero Action (attack): Exhaust this card and discard the top 2 cards of your deck ->
#   deal 2 damage to an enemy.
#
# CARTES DE REFERENCE
#  - `tr011` Raphael's Sai (pack raphael) : amelioration `Hero Action (attack)` qui incline,
#    cible `Enemy`, degats par `heros.DealDamage` ; `td011` pour `CanPlayThisUpgradeCard()`.
#  - `27183b` : `CostFunc.DiscardDeckTopCards("YourDeck", n)` en cout.
#
# TEXTE CONTRE CODE
#  ⚠ « Exhaust this card AND discard the top 2 cards of your deck -> » : DEUX couts, tous
#    deux payes avant les degats. Deck de moins de 2 cartes : la regle « deck vide » du
#    moteur s'applique dans le cout (`DiscardDeckTopCards`).
#  ⚠ « deal 2 damage to AN enemy » : un seul ennemi, au choix (villain ou sbire).
#  ⚠ Libelle `attack` : une action d'attaque (Stunned l'annule). Degats infliges par le HEROS.
#  Aucune limite imprimee (l'inclinaison borne l'usage).


def GetAbilities() -> Sequence['Ability']:

    def diode(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this, message)
        joueur = JoueurDeCetteCarte(effect)
        heros = HerosDuJoueur(effect, joueur) or IdentiteDuJoueur(effect, joueur)
        cibles = [t for t in effect.targets if t is not None]
        if heros is not None and cibles:
            heros.DealDamage(cibles, 2, effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            diode,
        ).SetLabel('attack')
        .SetTarget(Enemy)
        .SetCostFunc(CostFunc.Exhaust("This"))
        .SetCostFunc(CostFunc.DiscardDeckTopCards("YourDeck", 2)),
    ]
