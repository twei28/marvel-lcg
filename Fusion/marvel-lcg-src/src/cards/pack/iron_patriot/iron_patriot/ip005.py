from . import *

# * Sentry — ALLIE, cout 5, 6 PV, ATQ 4**, CTR 1*, RES [energy].
# AERIAL. AVENGER. REGISTERED.
# Toughness. Vulnerable.
# Interrupt: When an enemy attacks you, you may declare Sentry the defender
#   without exhausting him.
# Void's Wrath — Special: Until the end of the round, gain retaliate X, where
#   X is equal to Sentry's ATK.
#
# CARTES DE REFERENCE
#  - `dd003` Doombot / `45031` * Colossus : « declare it the defender WITHOUT
#    exhausting it ». La lecon y est deja ecrite noir sur blanc :
#    **`DeclareDefender` N'INCLINE PAS de lui-meme** (`32017` Mutant Protectors
#    appelle `Faces.ExhaustAll` juste avant, parce que SA carte incline). Ne
#    rien appeler ici, c'est tout le sens de « without exhausting him ».
#  - `bl006` Vampiric Reflexes : `GainUntilRoundEnd(effect, retaliate=N)`.
#
# TEXTE CONTRE CODE
#  ⚠ Sentry est DEJA EN JEU quand l'interruption se declenche, contrairement a
#    Doombot qui se joue depuis la main. Donc pas de `SetPlay()`, pas de
#    `PlayCardsLikeInTurn` : on declare, point.
#  ⚠ « When an enemy attacks YOU » : `who_be_attacked="You"`, l'IDENTITE. Une
#    attaque dirigee contre un autre allie ne declenche rien.
#  ⚠ « GAIN retaliate X » sans sujet exprime : c'est SENTRY qui gagne, comme
#    « Sentry's ATK » juste apres le prouve — la phrase parle de lui a la
#    troisieme personne d'un bout a l'autre.
#  ⚠ X est lu AU MOMENT DE LA RESOLUTION (`this.attack`, valeur courante, pas
#    `printed_attack`) : `ip003` Absolute Power dans la pile de victoire donne
#    +1 ATQ a Sentry, donc riposte 5.
#  ⚠ Toughness et Vulnerable sont des BASES NATIVES lues dans `desc`. Aucun
#    module. Les deux etoiles d'ATQ (degats consecutifs 2) aussi.


def GetAbilities() -> Sequence['Ability']:

    def defendre_sans_incliner(effect: 'Effect',
                               message: 'Message.WhenUnitBeingAttack') -> None:
        this = effect.this.CastTo(Ally)
        if not this.IsInPlay():
            return
        message.DeclareDefender(this, effect)

    def colere_du_vide(effect: 'Effect', message: 'Message.WhenResolveSpecialAbility') -> None:
        this = effect.this.CastTo(Ally)
        Unused(message)
        this.GainUntilRoundEnd(effect, retaliate=this.attack)

    return [
        AbilityFactory.CanPlayThisAllyCard(),
        AbilityFactory.WhenUnitBeingAttack(
            AbilityType.Interrupt,
            "You",
            Enemy,
            defendre_sans_incliner,
        ).SetLabel('defense'),
        SpecialRegistered("Void's Wrath", colere_du_vide),
    ]
