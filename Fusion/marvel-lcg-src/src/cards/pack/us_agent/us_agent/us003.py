from . import *

# Deflection — evenement signature, x2 (4/15, 5/15). TACTIC. Cout 1, ressource [physical].
# Hero Response: After an enemy deals 2 or more damage to you, if U.S. Agent's Shield is in play, stun up to 2 minions.
#
# Cartes de reference :
#  - `sh007` Trading Blows (`AfterUnitTookDamage(HeroResponse, "You", op, is_from_attack=True, who_dealt_damage=Enemy)
#    .SetPlay()`) : evenement qui repond a des degats subis.
#  - `AfterUnitTookDamage` : `message.took_damage` = les degats REELLEMENT subis (apres prevention).
#  - `53039`/`45113` : « up to N » = `SetTarget(Minion, canbe_stunned=True, range=(0, N))` + `Faces.GiveStatus`.
#
# ⚠ Mots-pieges :
#  - « deals 2 OR MORE damage to YOU » : `took_damage >= 2` sur l'identite du joueur (« You »), degats d'un ENNEMI
#    (`who_dealt_damage=Enemy`), attaque ou non ; 1 degat ne declenche rien.
#  - « if U.S. Agent's Shield is IN PLAY » : le bouclier d'un joueur quelconque, en jeu. Place dans `conditions` : sans lui,
#    la carte n'est pas proposee (elle serait jouee pour rien).
#  - « stun UP TO 2 minions » : cibles facultatives (0 a 2), uniquement des SBIRES (jamais le vilain).


def GetAbilities() -> Sequence['Ability']:

    def bouclier_en_jeu(effect: 'Effect', message: 'Message.AfterUnitTookDamage') -> bool:
        Unused(message)
        return len(Worlds.FindCardsOnField(effect, name=NOM_BOUCLIER, card_type=Upgrade)) > 0

    def deux_degats_ou_plus(effect: 'Effect', message: 'Message.AfterUnitTookDamage') -> bool:
        Unused(effect)
        return message.took_damage >= 2

    def deflection(effect: 'Effect', message: 'Message.AfterUnitTookDamage') -> None:
        this = effect.this.CastTo(Event)
        Unused(this, message)

        Faces.GiveStatus([c for c in effect.targets if c is not None], "Stunned", effect)

    return [
        AbilityFactory.AfterUnitTookDamage(
            AbilityType.HeroResponse,
            "You",
            deflection,
            who_dealt_damage=Enemy,
            conditions=[deux_degats_ou_plus, bouclier_en_jeu],
        ).SetPlay().SetLabel()
        .SetTarget(Minion, canbe_stunned=True, range=(0, 2)),
    ]
