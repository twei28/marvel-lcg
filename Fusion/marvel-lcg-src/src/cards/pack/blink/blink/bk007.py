from . import *

# * Crystal Palace — SOUTIEN, cout 2, [wild]. LOCATION.
# Response: After a [[PORTAL]] upgrade is discarded from play, exhaust Crystal
#   Palace -> attach it facedown here.
# Alter-Ego Action: Exhaust Crystal Palace -> add each [[PORTAL]] upgrade
#   attached here to your hand.
#
# CARTES DE REFERENCE
#  - `ma004` * Santana Family et `27007` George Stacy : la zone de cartes
#    POSEES (`TuckCardUnderHere` / `GetPlacedCardArea`), meme montage exact.
#
# TEXTE CONTRE CODE
#  « FACEDOWN » -> `TuckCardUnderHere` sans `peek=` : face CACHEE
#    (card_face.py). `peek=True` serait « visible pour toi seul », ce n'est
#    pas ce que le texte demande.
#  « EACH PORTAL attached HERE » -> toute la zone d'un coup, pas une carte.
#  « ALTER-EGO Action » -> sous-type dedie : recuperer le stock coute un tour
#    en forme civile.


def GetAbilities() -> Sequence['Ability']:

    def ranger_le_portail(effect: 'Effect', message: 'Message2') -> None:
        this = effect.this.CastTo(Support)
        portail = getattr(message, "trigger", None)
        if portail is None:
            return
        this.TuckCardUnderHere(portail, effect)

    def venait_du_terrain(effect: 'Effect', message: 'Message.AfterCardDiscard') -> bool:
        """« discarded FROM PLAY » : la carte etait-elle EN JEU juste avant ?"""
        Unused(effect)
        zone = getattr(message, "from_area", None)
        return zone is not None and zone.flags.is_in_play

    def reprendre_le_stock(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Support)
        Unused(message)
        zone = this.GetPlacedCardArea()
        if zone is None:
            return
        rangees = list(zone.Get(True))
        if rangees:
            Faces.ReturnToHand(rangees, "Owner", effect)

    return [
        AbilityFactory.CanPlayThisSupportCard(),
        # ⚠ `from_where="PlayerArea"` NE CONVIENT PAS ICI, et c'est propre au
        # kit de Blink : ce filtre teste `from_area.play_area != None`, c'est-
        # a-dire la zone du JOUEUR. Or un portail s'accroche a un ENNEMI ou a
        # une MANIGANCE, donc il vit dans la zone d'ameliorations de sa cible.
        # Aucun portail ne remplissait la condition, la Reponse ne partait
        # jamais et Crystal Palace restait vide sans un mot. « FROM PLAY » se
        # rend donc directement : `from_area.flags.is_in_play`.
        AbilityFactory.AfterCardDiscard(
            AbilityType.Response,
            CardFinder(card_type=Upgrade, trait=TRAIT_PORTAIL),
            ranger_le_portail,
            conditions=[venait_du_terrain],
        ).SetCostFunc(CostFunc.Exhaust("This")),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.AlterEgoAction,
            reprendre_le_stock,
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
