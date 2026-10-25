from . import *

# Lash Out — TRAITRISE (x2). SKILL. Boost 1 + etoile.
# When Revealed: Lady Deathstrike attacks you (even if you are in alter-ego). Do not give her a boost card for this attack. If this
#   attack deals any amount of damage, give Lady Deathstrike a tough status card.
# [star] Boost: Give Lady Deathstrike a tough status card.
#
# Cartes de reference :
#  - `02030` I See You : `villain.DoAttackYou(joueur, effect, property=AttackProperty(do_not_give_boost=True))` ;
#    `DoAttackYou(..., if_this_attack_deals_damage=fn)` (enemy.py) pour « if this attack deals damage » ;
#  - `Faces.GiveStatus([vilain], "Tough", effect)` (`22006`) ; Boost etoile : `WhenCardBecomeBoost("This", op)` (`01154`).
#
# ⚠ Mots-pieges :
#  - « even if you are in alter-ego » : l'attaque a lieu dans les deux formes (l'alter-ego encaisse) ;
#  - « Do NOT give her a boost card » : `do_not_give_boost=True` ; « ANY amount of damage » : au moins 1 degat reel (une attaque
#    entierement parree ne donne rien) ;
#  - le Boost est un EFFET d'etoile : il donne Tough meme sans attaque revelee pour cette carte ;
#  - « Lady Deathstrike » : le vilain (card_id), pas un sbire homonyme.


def GetAbilities() -> Sequence['Ability']:

    def revelee(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        Unused(this)

        vilain = LadyDeathstrike(effect)
        joueur = message.GetToPlayer()
        if vilain is None or joueur is None:
            return

        def blesse(degats: int) -> None:
            if degats > 0:
                Faces.GiveStatus([vilain], "Tough", effect)

        vilain.DoAttackYou(
            joueur,
            effect,
            property=AttackProperty(do_not_give_boost=True),
            if_this_attack_deals_damage=blesse,
        )

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        this = effect.this.CastTo(Treachery)
        Unused(this, message)

        vilain = LadyDeathstrike(effect)
        if vilain is not None:
            Faces.GiveStatus([vilain], "Tough", effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            revelee,
        ),
        AbilityFactory.WhenCardBecomeBoost(
            "This",
            boost,
        ),
    ]
