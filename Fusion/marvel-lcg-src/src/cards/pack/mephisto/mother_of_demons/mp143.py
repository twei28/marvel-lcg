from . import *

# * Lilin Remaking — pacte BARGAIN (Mother of Demons). Boost 3, Peril (natifs). When Revealed : meme texte que les sept pactes (`AbilitesDuPacte`).
# Treat your identity's printed text box as blank (except for TRAITS). You cannot attack Lilith and she cannot activate against you. You gain the MYSTIC trait, retaliate 2, and villainous.
# Response : After your turn begins, discard this card -> find Lilith and reveal her. (If she is already in play, she engages you.) Lilith activates against you.
#
# Cartes de reference : sm/venom/27079 (`treat_as_blank=True`), do_attack.py `UnitCannotBeAttacked` (+ attaquant = l'identite porteuse), mp001 (`WhenEnemyWouldActivate` + `SetBeInstead`),
# mp103 (Response « trouver et reveler » : `TrouverRevelerEtActiver`). `GiveKeywordToAttached(Identity, trait=, retaliate=, villainous=, treat_as_blank=)` (asset.py).
# ⚠ Mots-pieges : « printed text box ... EXCEPT TRAITS » : le texte imprime de l'identite est vide mais ses traits restent ; « YOU cannot attack Lilith » : l'identite porteuse (pas les allies) ;
# « she cannot activate AGAINST YOU » : seulement contre le porteur ; sa Response (comme celle de mp103) n'est pas celle des autres pactes (pas d'icones de boost, pas de Mephisto).


def GetAbilities() -> Sequence['Ability']:
    def le_porteur_attaque(effect: 'Effect', message: 'Message.CheckIfUnitCanBeAttackBy') -> bool:
        return message.attacker is effect.this.CastTo(Attachment).GetBindFace()

    def contre_le_porteur(effect: 'Effect', message: 'Message.WhenEnemyWouldActivate') -> bool:
        porteur = effect.this.CastTo(Attachment).GetBindFace()
        joueur = porteur.GetControlByPlayer() if porteur is not None else None
        return joueur is not None and message.to_player == joueur

    def ne_s_active_pas(effect: 'Effect', message: 'Message.WhenEnemyWouldActivate') -> None:
        message.SetBeInstead(effect)

    def reponse(effect: 'Effect', message: 'Message.AfterPlayerTurnBegin') -> None:
        TrouverRevelerEtActiver(effect, message.to_player, "Lilith")

    return [
        *AbilitesDuPacte(reponse),
        *AbilityFactory.GiveKeywordToAttached(Identity, trait="MYSTIC", retaliate=2, villainous=1, treat_as_blank=True),
        AbilityFactory.UnitCannotBeAttacked(CardFinder(name="Lilith"), conditions=[le_porteur_attaque]),
        AbilityFactory.WhenEnemyWouldActivate(AbilityType.ForcedInterrupt, CardFinder(name="Lilith"), ne_s_active_pas, conditions=[contre_le_porteur]),
    ]
