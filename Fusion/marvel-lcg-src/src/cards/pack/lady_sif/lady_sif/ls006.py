from . import *

# Valiant Defense — evenement signature, x3 (n/15 = 8, 9 et 10).
# DEFENSE. TACTIC. Cout 1, ressource [energy].
# Hero Interrupt (defense): When an enemy attacks, make a basic defense
#   without exhausting your hero. You get +1 DEF for this attack (+2 DEF
#   instead if you paid for this card using a [energy] resource).
#
# Cartes de reference :
#  - **`25011` Shieldmaiden** (pack valk), jumeau du montage au mot pres :
#    `WhenUnitBeingAttack(HeroInterrupt, ...).SetPlay().SetLabel('defense')`,
#    puis `heros.GainForThisActive(effect, message.would_atk_message,
#    defense=N)` et `message.DeclareDefender(heros, effect)`. Seule la valeur
#    change, et elle est conditionnelle ici ;
#  - `01013` Photonic Blast / `01060` For Justice! pour « if you paid for this
#    card using a [energy] resource » -> `GetPaidResources().HasColor("Y")` ;
#  - `dd003` Doombot pour la regle, ecrite noir sur blanc dans son
#    commentaire : **`DeclareDefender` N'INCLINE PAS de lui-meme**. C'est
#    exactement ce que « without exhausting your hero » demande.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « using A [energy] resource » : AU MOINS une energie, d'ou `HasColor`, et
#    surtout pas `OnlyHasColor`. La carte coute 1 : un seul paiement, mais un
#    wild converti compte.
#  - « +2 DEF INSTEAD » : 2 OU 1, jamais 3.
#  - « for THIS ATTACK » : `GainForThisActive(..., message.would_atk_message,
#    ...)`, borne a l'attaque en cours — et surtout pas `GainUntilRoundEnd`,
#    qui laisserait le bonus courir sur toutes les attaques du round.
#  - « When an ENEMY attacks » : vilain ET sbires, sans filtre de cible.
#  - « make a BASIC defense » : la DEF imprimee compte, donc les ameliorations
#    qui donnent +DEF (ls010 Sif's Spear) s'ajoutent au bonus de cette carte.
#  - Le libelle `(defense)` alimente Sonne ? Non — c'est `attack` qui l'est.
#    `defense` est un libelle a part entiere (RECETTES §4bis), accepte par
#    `HeroInterrupt`.


def GetAbilities() -> Sequence['Ability']:

    def valiant_defense(effect: 'Effect', message: 'Message.WhenUnitBeingAttack') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)

        if not effect.targets:
            return
        heros = effect.targets[0].CastTo(Hero)

        # « +2 DEF instead if you paid ... using a [energy] resource » :
        # au moins une energie, jamais « only ».
        valeur = 2 if effect.GetPaidResources().HasColor("Y") else 1

        heros.GainForThisActive(effect, message.would_atk_message,
                                defense=valeur)
        message.DeclareDefender(heros, effect)

    return [
        AbilityFactory.WhenUnitBeingAttack(
            AbilityType.HeroInterrupt,
            "You",
            Enemy,
            valiant_defense,
        ).SetPlay().SetLabel('defense')
        .SetTarget("YourHero"),
    ]
