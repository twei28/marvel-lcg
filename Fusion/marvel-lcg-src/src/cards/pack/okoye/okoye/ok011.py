from . import *

# * Upanga
# Each DORA MILAJE ally you control gets +1 hit point.
# Alter-Ego Action: Exhaust Upanga -> shuffle 1 ARMOR, TECH, or WEAPON card
#   from your discard pile into your deck.
#
# "Each ally you control gets +1 HP" tant que la carte est en jeu : modele
# exact trors/04016.py (Team Training), `AbilityFactory
# .GiveKeywordToInPlayWhenApplyThis(...)`, ici restreint aux allies DORA
# MILAJE via un CardFinder au lieu du simple `Ally` de Team Training.
# "shuffle 1 ARMOR/TECH/WEAPON card from discard into deck" : recherche
# multi-trait via `check_face_fn` (modele kb008), `Faces.ShuffleAllTo`
# (modele kb002/ok001b).


def GetAbilities() -> Sequence['Ability']:

    def upanga_alter_ego(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Support)
        Unused(this)

        initiator = effect.GetInitiator()
        if initiator is None:
            return

        face = Search.PlayerCard(
            effect,
            initiator,
            include_player_deck=False,
            include_discard_pile=True,
            finder=CardFinder(
                card_type=Upgrade,
                check_face_fn=lambda f: f.HasTrait("ARMOR") or f.HasTrait("TECH") or f.HasTrait("WEAPON"),
            ),
        )
        if face:
            Faces.ShuffleAllTo([face], initiator.player_deck, effect)

    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            CardFinder(card_type=Ally, trait="DORA MILAJE"),
            control_by="You",
            health=1,
        ),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.AlterEgoAction,
            upanga_alter_ego,
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
