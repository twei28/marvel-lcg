from . import *

# Cosmic Energy — Evenement, cout X, ressource [energy]. ATTACK. COSMIC. THWART.
# Hero Action (attack): Remove X threat divided among schemes as you choose and deal X damage to an enemy,
#   where X is the number of [energy] resources you paid for Cosmic Energy's cost.
#
# Cartes de reference :
#  - `14006` Speed Cyclone : cout X (`desc.Cost = "X"`).
#  - `06006` Lightning Strike / `52018` Energy Shield : X lu dans le paiement (`GetPaidResources().GetColor("Y")`,
#    qui convertit les [wild] en energie).
#  - `13003` Giant Help (wsp) : menace « divided among schemes as you choose ».
#
# ⚠ Mots-pieges :
#  - X = ressources ENERGIE PAYEES (un [wild] paye en vaut une), pas le cout total paye : payer avec du mental
#    ne compte pas.
#  - « divided among schemes as you choose » : X menaces au total, retirees une par une ou groupees, sur les
#    manigances de son choix ; on s'arrete quand il n'y a plus de menace.
#  - les DEUX effets (menace ET degats) ont lieu, sans condition l'un de l'autre.
#  - (attack) : evenement d'attaque (statut Etourdi), le texte du pack porte aussi les traits ATTACK et THWART.


def GetAbilities() -> Sequence['Ability']:

    def energie_cosmique(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)

        x = effect.GetPaidResources().GetColor("Y")
        joueur = JoueurDeCetteCarte(effect)
        if joueur is not None:
            for _ in range(x):
                candidates = Worlds.FindCardsOnField(effect, card_type=Scheme2, has_threat=True)
                if not candidates:
                    break
                choisie = joueur.AskChooseFace(
                    candidates,
                    effect,
                    prompt="Remove 1 threat from a scheme",
                )
                if choisie is None:
                    break
                this.RemoveThreatFromSchemes([choisie], 1, effect)
        this.DealDamage(effect.targets, x, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            energie_cosmique,
        ).SetPlay().SetLabel('attack')
        .SetTarget(Enemy),
    ]
