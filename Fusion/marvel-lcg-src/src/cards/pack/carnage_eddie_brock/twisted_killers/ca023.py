from . import *

# * Hunting Victims : TRAITRISE (x3), boost 1. Set modulaire « Twisted Killers ».
# When Revealed: Each KILLER minion engaged with a player activates against that player. If no minion activates this way, this card gains surge.
# [star] Boost: If this activation is an attack that defeats a character, excess damage dealt by this attack is placed as threat on the main scheme.
#
# CARTES DE REFERENCE
#  - « Each X minion engaged with a player activates against that player ; if none, surge » : `ar014` (Lead the Charge) / `bw021` : `enemy.DoActivate(joueur, effect)` (rend `None` si l'ennemi ne s'est pas active, enemy.py:303), `this.GainSurge(1, effect)` (ca016, my015).
#  - Boost etoile qui concerne l'ACTIVATION en cours : `sk116` (`WhenCardBecomeBoost("This", op)`), `GiveBoostCardForThisActivation` / `message.would_message` (sender_card.py:776) ; capacite temporaire de l'ennemi qui s'active : `RegisterTemp` (`GainBoostIcon`, sender_card.py:748).
#  - Exces en menace, EN REMPLACEMENT : meme mecanique que ca021 (`AfterUnitDefeatedUnit(.., has_excess_damage=True)` + `message.excess_damage` ; transfert d'overkill `property.is_from_overkill` empeche par `PreventDamage("All")`).
#
# TEXTE CONTRE CODE
#  « EACH KILLER minion ENGAGED WITH A PLAYER activates AGAINST THAT PLAYER » : chaque sbire KILLER engage avec un joueur s'active contre CE joueur (attaque en forme heros, manigance en alter-ego, selon `DoActivate`) ; un sbire non KILLER ou non engage n'agit pas. « If NO minion activates this way » : aucun sbire KILLER engage -> surge.
#  « [star] Boost: If THIS ACTIVATION is an attack that DEFEATS A CHARACTER, EXCESS damage dealt BY THIS ATTACK is placed as threat ON THE MAIN SCHEME » : DECISION UTILISATEUR du 03/11 (lecture B, coherente avec ca021) : l'exces est CONVERTI en menace sur le complot PRINCIPAL et N'EST PLUS INFLIGE. Seule l'attaque de CETTE activation
#    (les autres attaques du tour ne sont pas touchees) ; pas de defaite, pas d'exces : rien. Chiffres : boost 1.


def GetAbilities() -> Sequence['Ability']:

    def hunting_victims(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        joueur = message.GetToPlayer()
        chasseurs = [
            f for f in Worlds.GetOnFieldEnemies(effect)
            if Minion.IsType(f) and f.IsInPlay() and f.HasTrait("KILLER")
            and f.CastTo(Minion).engaged_player is joueur
        ]
        active = False
        for chasseur in chasseurs:
            if chasseur.IsInPlay() and chasseur.CastTo(Enemy).DoActivate(joueur, effect) is not None:
                active = True
        if not active:
            this.GainSurge(1, effect)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        activant = message.activating_enemy
        attaque = getattr(message, "would_message", None)
        if activant is None or attaque is None:
            return

        # « THIS activation » : le drapeau tombe a la fin de l'activation de l'ennemi (`AfterThisActivation`). On ne compare PAS les messages d'attaque entre eux :
        # le message d'une Reponse differee est une COPIE (`CopyForDelay`), la comparaison d'identite echouait (constate le 03/11).
        etat = {"actif": True}
        message.AfterThisActivation(effect, lambda: etat.update(actif=False))

        def cette_attaque(effect2: 'Effect', message2: 'Message2') -> bool:
            Unused(effect2, message2)
            return etat["actif"]

        def exces_en_menace(effect2: 'Effect', message2: 'Message.AfterUnitDefeatedUnit') -> None:
            Unused(effect2)
            exces = int(getattr(message2, "excess_damage", 0) or 0)
            if exces > 0:
                effect.this.PlaceThreatOnSchemes("MainScheme", exces, effect)

        def exces_non_inflige(effect2: 'Effect', message2: 'Message.WhenUnitWouldTakeDamage') -> None:
            Unused(effect2)
            message2.PreventDamage("All", effect)

        def de_l_activant(effect2: 'Effect', message2: 'Message2') -> bool:
            Unused(effect2)
            tueur = getattr(message2, "killer", None) or getattr(message2, "source", None)
            return etat["actif"] and tueur is activant

        # Temporaires portees par CETTE carte de boost (modeles `40017` pour WhenUnitWouldTakeDamage, `uw006` pour AfterUnitDefeatedUnitInternal) :
        # enregistrees sur l'ennemi qui s'active elles ne partaient jamais (constate le 03/11).
        effect.this.effect.RegisterTemp(
            AbilityFactory.AfterUnitDefeatedUnitInternal(
                AbilityType.Temp0,
                None,
                Unit2,
                exces_en_menace,
                is_from_attack=True,
                has_excess_damage=True,
                conditions=[de_l_activant],
            ),
            unregister_after_exec=True,
            until_turn_end=True,
        )
        effect.this.effect.RegisterTemp(
            AbilityFactory.WhenUnitWouldTakeDamage(
                AbilityType.Temp0,
                Unit2,
                exces_non_inflige,
                conditions=[lambda effect2, message2: bool(message2.property.is_from_overkill) and de_l_activant(effect2, message2)],
            ),
            unregister_after_exec=True,
            until_turn_end=True,
        )

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            hunting_victims,
        ),
        AbilityFactory.WhenCardBecomeBoost(
            "This",
            boost,
        ),
    ]
