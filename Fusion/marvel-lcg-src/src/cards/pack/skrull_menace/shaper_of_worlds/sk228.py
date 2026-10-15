from . import *

# * Shaper of Worlds — SBIRE (Shaper of Worlds). COSMIC ENTITY. ELITE. SKRULL. MNG 2, ATQ 2,
# PV infinis (badge ∞), aucune icone de boost.
# Forced Response: After a player attacks Shaper of Worlds, shuffle this card into that player's deck.
# Forced Interrupt: When Shaper of Worlds enters your hand, discard the top 4 cards of the encounter
#   deck. Put Shaper of Worlds into play engaged with you.
#
# Cartes de reference :
#  - Reponse apres avoir ete attaque : **`24045`** Shocker (`AfterUnitBeAttacked(ForcedResponse, "This", ...)`).
#  - « enters your hand » : **`bk002`** Sabretooth et **`vz036`** Flash Fire (`AfterCardEnterHand(..., "This", ...)`,
#    qui pose `CanWorkOnlyInHand` tout seul) ; encounter card dans un deck joueur : `vz036` (weakness).
#  - Melange dans le deck d'un joueur : `Faces.ShuffleAllTo(faces, joueur.player_deck, effect)`.
#  - Defausser N cartes du deck rencontre : **`sk139`** (`Worlds.DiscardEncounterCards(n, effect)`).
#
# ⚠ Mots-pieges : « a PLAYER attacks » (le joueur qui controle l'attaquant : identite ou allie) ;
# « shuffle THIS card into THAT player's deck » (pas le deck rencontre) ; « enters YOUR hand » (la
# main du joueur qui la recoit, quelle que soit la facon) ; « Put ... into play ENGAGED WITH YOU »
# (le joueur qui l'a en main) ; le texte dit Forced INTERRUPT : la carte arrive en jeu au moment ou
# elle entre en main (aucune Reponse du joueur ne s'insere entre les deux).


def GetAbilities() -> Sequence['Ability']:

    def attaque(effect: 'Effect', message: 'Message.AfterUnitAttackUnit') -> None:
        this = effect.this
        joueur = message.attacker.GetControlByPlayer()
        if joueur is None or not Player.IsType(joueur):
            return
        Faces.ShuffleAllTo([this], joueur.player_deck, effect)

    def en_main(effect: 'Effect', message: 'Message.AfterCardEnterHand') -> None:
        this = effect.this
        Unused(message)
        joueur = this.GetControlByOrOwner()
        if joueur is None or not Player.IsType(joueur):
            return
        Worlds.DiscardEncounterCards(4, effect)
        MettreEnJeuEngage(effect, this, joueur)

    return [
        AbilityFactory.AfterUnitBeAttacked(AbilityType.ForcedResponse, "This", attaque),
        AbilityFactory.AfterCardEnterHand(AbilityType.ForcedInterrupt, "This", en_main),
    ]
