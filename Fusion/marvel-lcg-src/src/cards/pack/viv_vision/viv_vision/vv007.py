from . import *

# * Sparky the Dog — SOUTIEN signature, x1 (n/15 = 12). ANDROID. GOOD BOY.
# Cout 1, ressource [wild] (etoile VERTE sur le scan, PAS un poing physique).
# Hero Interrupt: When a minion initiates an attack, exhaust Sparky the Dog ->
#   deal 2 damage to that minion.
# Alter-Ego Action: Exhaust Sparky the Dog -> heal 1 damage from your
#   identity.
#
# Cartes de reference :
#  - 18015 First Hit (pack gam) : meme declencheur exact « when a minion
#    initiates an attack », rendu par `WhenUnitWouldAttack(<type>, Minion,
#    ...)` et 2 degats sur le sbire attaquant. First Hit vise l'attaquant par
#    `.SetTarget("Trigger")` ; on prefere ici lire `message.attacker`, qui dit
#    la meme chose sans poser de selecteur au joueur pour une cible unique
#    deja designee par le texte ;
#  - sr010 Spider-Sense (meme auteur, Rainy) pour la lecture de
#    `message.attacker` dans une Interruption sur `WhenUnitWouldAttack` ;
#  - aa003 Ebony (pack agatha_harkness) pour le couple
#    `WhenInYourPlayTurn(AbilityType.AlterEgoAction, ...)
#    .SetCostFunc(CostFunc.Exhaust("This"))` ;
#  - sd013 Mother's Protection (pack speed) pour la declaration explicite de
#    `CanPlayThisSupportCard()` sur un soutien signature.
#
# ⚠ RESSOURCE IMPRIMEE : le dossier de preparation annonçait une etoile
# « physique ». Verification faite sur le scan le 02/09/2026, en comparant le
# coin inferieur gauche aux autres cartes du MEME pack (leçon Lockjaw,
# PROCESSUS-CARTE etape 3) : c'est une ETOILE VERTE, donc `RES = "G"` (wild).
# vv006 Superdense Strike porte, elle, le poing rouge (`RES = "R"`), et
# vv004/vv005/vv009/vv010 l'eclair jaune (`RES = "Y"`).
# Consequence concrete : Sparky n'est PAS repechable par le Recharge de
# vv001b, qui exige une ressource ENERGIE imprimee (le moteur compare sans
# conversion du wild, cf. checker.py:436).
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « a MINION initiates an attack » : les sbires seulement, jamais le
#    vilain. `WhenUnitWouldAttack(..., Minion, ...)`, comme 18015.
#  - Pas de « against you » imprime : l'interruption joue aussi quand le sbire
#    attaque un AUTRE joueur. On ne pose donc PAS `against_player="You"`,
#    contrairement a sr010 qui, elle, l'imprime.
#  - « deal 2 damage to THAT minion » : le sbire qui attaque, pas un choix.
#  - « exhaust Sparky the Dog -> » : la fleche fait de l'epuisement un COUT,
#    donc l'interruption ne se propose pas si Sparky est deja incline.
#  - « heal 1 damage from YOUR IDENTITY » : l'identite, pas « your hero » —
#    et de toute facon la capacite est une Alter-Ego Action, donc la face en
#    jeu est l'alter-ego. `joueur.GetIdentity()` rend la face courante.
#  - Les deux capacites sont mutuellement exclusives par leur type (Hero
#    Interrupt / Alter-Ego Action), mais partagent le meme epuisement : une
#    seule des deux par round sans redressement.


def GetAbilities() -> Sequence['Ability']:

    def mordre_le_sbire(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        this = effect.this.CastTo(Support)

        sbire = message.attacker
        if sbire is None:
            return
        this.DealDamage([sbire], 2, effect)

    def soigner(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Support)
        Unused(message)

        joueur = effect.GetInitiator()
        if joueur is None:
            return
        identite = joueur.GetIdentity()
        if identite is None:
            return
        this.HealthUnits([identite], 1, effect)

    return [
        AbilityFactory.CanPlayThisSupportCard(),
        AbilityFactory.WhenUnitWouldAttack(
            AbilityType.HeroInterrupt,
            Minion,
            mordre_le_sbire,
        ).SetCostFunc(CostFunc.Exhaust("This")),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.AlterEgoAction,
            soigner,
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
