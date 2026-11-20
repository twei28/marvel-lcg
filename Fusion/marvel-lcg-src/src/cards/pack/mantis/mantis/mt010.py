from . import *

# * The Celestial Madonna : AMELIORATION (TITLE), cout 2, [energy]. Unique. Hero Class.
# Hero Interrupt: When you resolve Mantis' "Empathetic Advantage" ability, exhaust The Celestial Madonna → this use does not count against that ability's limit.
#
# CARTES DE REFERENCE
#  - `mt001a` (meme pack) : le compteur de round partage (`CLE_EMPATHETIC_ADVANTAGE`) ; `AfterYouSpendThisCard` (`resources.py:579`) pour lire `AfterCardsBeSpendAsResource` (`message.faces` = les cartes qui ont paye).
#  - `dt009` Savior Complex / `32036` : `Ability(.., <un message>, [conditions], op).SetCostFunc(CostFunc.Exhaust("This"))` pour une capacite a inclinaison.
#
# TEXTE CONTRE CODE
#  « When you resolve Mantis' Empathetic Advantage » : l'emploi qui vient d'etre PAYE (la face heros de Mantis figure parmi les cartes qui ont paye). « exhaust The Celestial Madonna → » = COUT. « this use does not count » :
#  le compteur de round de la capacite retombe d'une unite (un emploi libre). ⚠ ECART de moteur : le message de paiement `WhenPlayerPayingResources` n'admet pas d'Interruption (categorie « Paying », assert de
#  `RegisterEffect`) ; la capacite part donc sur `AfterCardsBeSpendAsResource`, juste apres le paiement, ce qui revient au meme effet de jeu (l'emploi ne compte pas) mais pas a la meme fenetre.
#  Chiffres : cout 2.


def GetAbilities() -> Sequence['Ability']:

    def mantis_a_paye(effect: 'Effect', message: 'Message.AfterCardsBeSpendAsResource') -> bool:
        joueur = effect.GetInitiator()
        if joueur is None or effect.world.stat.GetRoundCounter(joueur, CLE_EMPATHETIC_ADVANTAGE) <= 0:
            return False
        return any(f.card.IsOnField() and f.IsName(NOM_MANTIS, check_all_face=True) and f.GetControlByPlayer() == joueur
                   and Hero.IsType(f) for f in message.faces)

    def celestial_madonna(effect: 'Effect', message: 'Message.AfterCardsBeSpendAsResource') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this, message)
        joueur = effect.GetInitiator()
        effect.world.stat.AddRoundCounter(joueur, CLE_EMPATHETIC_ADVANTAGE, -1)

    return [
        Ability(
            AbilityType.HeroInterrupt,
            Message.AfterCardsBeSpendAsResource,
            [mantis_a_paye],
            celestial_madonna,
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
