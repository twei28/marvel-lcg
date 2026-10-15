from . import *

# Mistrust and Paranoia — COMPLOT ANNEXE (Secret Invasion). Menace 2, icone ACCELERATION, 2 boosts.
# Players cannot attack minions engaged with other players or defend against them. Players cannot pay any card's or
#   ability's costs as a group.
# When Revealed: Place 1 additional threat here for each friendly character in play.
#
# Cartes de reference :
#  - « cannot attack ... » : **`AbilityFactory.UnitCannotAttackTarget`** (do_attack.py, `cannot_attack=...`) et `sk070` pour
#    le style ; « cannot ... defend » : **`AbilityFactory.UnitCannotDefend`** ; « when revealed ... for each friendly character » :
#    **`paibok/sk156`** (`GetControlCharacters`).
#  - Paiement en groupe interdit : lu par `PaiementEnGroupeInterdit` (resources.py, modification de moteur documentee dans
#    defs/secret_invasion_moteur.md) ; la carte pose `interdit_paiement_en_groupe` sur elle-meme a son entree en jeu.
#
# ⚠ Mots-pieges : « minions engaged with OTHER players » (un sbire engage avec MOI reste attaquable) ; « attack OR defend
# against them » (les deux) ; « Players » = heros ET allies que les joueurs controlent ; « any card's OR ABILITY's costs » :
# mot-cle Alliance, Coordinated Effort et les capacites « payees en groupe » (Spider-Woman) ; « each FRIENDLY character »
# (identites et allies de tous les joueurs).


def GetAbilities() -> Sequence['Ability']:

    def autre_joueur(attaquant: 'CardFace', sbire: 'CardFace') -> bool:
        engage = getattr(sbire, 'engaged_player', None)
        controleur = attaquant.GetControlByPlayer() if attaquant is not None else None
        return Minion.IsType(sbire) and engage is not None and controleur is not None and engage != controleur

    def pas_mes_sbires_a_attaquer(effect: 'Effect', message: 'Message.CheckIfUnitCanBeAttackBy') -> bool:
        return autre_joueur(message.attacker, message.being_attack)

    def pas_mes_sbires_a_defendre(effect: 'Effect', message: 'Message.CheckIfUnitCanDefendAgainstAttack') -> bool:
        return autre_joueur(message.check_unit, message.attacker)

    def marquer(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        Unused(message)
        effect.this.interdit_paiement_en_groupe = True

    def revelation(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        Unused(message)
        this = effect.this.CastTo(EncounterSideScheme)
        nombre = sum(len(joueur.GetControlCharacters()) for joueur in Worlds.GetPlayers(effect))
        if nombre:
            this.PlaceThreatOnSchemes([this], nombre, effect)

    return [
        AbilityFactory.AfterCardEnterPlay(AbilityType.NonKeyword, "This", marquer),
        *AbilityFactory.UnitCannotAttackTarget(CardFinder(card_type=Unit2), cannot_attack=Minion, conditions=[pas_mes_sbires_a_attaquer]),
        *AbilityFactory.UnitCannotDefend(CardFinder(card_type=Unit2), Minion, cannot_trigger_defense_ability=False,
                                         conditions=[pas_mes_sbires_a_defendre]),
        AbilityFactory.WhenThisRevealed(None, revelation),
    ]
