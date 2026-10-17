from . import *

# * Splinter Dojo — SOUTIEN 2 [energy], aspect Basic (TMNT Reskins). LOCATION. NYC. STREETS.
# Alter-Ego Response: After a [[MUTANIMAL]] or [[NINJA]] ally enters play, exhaust Splinter Dojo → search your
#   deck and discard pile for a [[TRAINING]] upgrade and attach it to that ally. Any player whose alter-ego has
#   the [[MUTANT]] trait may trigger this ability.
#
# MODIFIEE de 33021 Danger Room : X-MEN -> MUTANIMAL ou NINJA. Script copie de 33021, avec UNE difference
# de fidelite : 33021 appelle `.AnyPlayerCanDoThis()` SANS condition (n'importe quel joueur), alors que le
# texte limite aux joueurs dont l'alter ego a MUTANT : on pose `player_alter_ego_has_trait="MUTANT"`, comme
# 32049 X-Mansion (meme phrase imprimee).


def GetAbilities() -> Sequence['Ability']:

    def splinter_dojo(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        this = effect.this.CastTo(Support)
        Unused(this)

        initiator = effect.GetInitiator()
        face = Search.PlayerCard(
            effect,
            initiator,
            include_player_deck=True,
            include_discard_pile=True,
            card_type=Upgrade,
            trait="TRAINING",
        )
        if face:
            face.AttachTo2(message.trigger, effect)

    return [
        AbilityFactory.AfterCardEnterPlay(
            AbilityType.AlterEgoResponse,
            CardFinder(card_type=Ally, traits=["MUTANIMAL", "NINJA"]),
            splinter_dojo,
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .AnyPlayerCanDoThis(player_alter_ego_has_trait="MUTANT"),
    ]
