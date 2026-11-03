from . import *

# * Essential Bloodlust : OBLIGATION, boost 2. A donner au joueur d'Eddie Brock.
# You may flip to alter-ego form. Choose:
# • Exhaust Eddie Brock -> remove Essential Bloodlust from the game.
# • Take indirect damage equal to your ATK. Discard this obligation.
#
# CARTES DE REFERENCE
#  - `dy013` (Seizure) / `my015` (My Love) / `mt011` : meme gabarit (`WhenThisObligationGiveToYou` + `YouMayFlipToYourAlterEgoForm` + `ChooseAbilities`, branche 1 `condition=joueur.IsAlterEgo()` + `Exhaust("YourIdentity")`).
#  - Degats indirects : `ch021` : `this.DealIndirectDamage(identite, N, effect)` (le joueur repartit entre son identite et ses allies).
#
# TEXTE CONTRE CODE
#  « You may flip to alter-ego form » : bascule facultative avant le choix. « Exhaust EDDIE BROCK → remove from the game » : l'alter-ego (donc seulement en forme alter-ego, apres l'eventuelle bascule) doit etre PRET ; la carte quitte la partie.
#  « Take indirect damage equal to YOUR ATK. Discard this obligation » : DECISION UTILISATEUR du 03/11 (lecture B) : l'ATK COURANTE de l'identite (bonus de cartes compris : Frenzied Violence +1...). En forme ALTER-EGO l'identite n'a PAS d'ATK : 0 degat indirect
#    (basculer en alter-ego avant de choisir la seconde branche l'annule donc). « Discard this obligation » appartient a la SECONDE branche (la premiere la retire de la partie). Aucun surge (le texte n'en parle pas).
#  Chiffres : boost 2, degats = ATK.


def GetAbilities() -> Sequence['Ability']:

    def essential_bloodlust(effect: 'Effect', message: 'Message.WhenObligationGiveToPlayer') -> None:
        this = effect.this.CastTo(Obligation)
        joueur = message.GetGaveToPlayer()

        YouMayFlipToYourAlterEgoForm(joueur, effect)

        def degats_indirects_puis_defausser(cibles: Sequence['CardFace']) -> None:
            Unused(cibles)
            identite = joueur.GetIdentity()
            attaque = int(identite.attack or 0) if Hero.IsType(identite) else 0
            if attaque > 0:
                this.DealIndirectDamage(identite, attaque, effect)
            Faces.DiscardAll([this], effect)

        premiere = AbilityFactory.ForChoiceAbility(
            "Exhaust Eddie Brock → remove Essential Bloodlust from the game",
            lambda cibles:
                Faces.RemoveAllFromGame([this], effect),
            condition=joueur.IsAlterEgo() and joueur.GetIdentity().IsReady(),
        ).SetCostFunc(CostFunc.Exhaust("YourIdentity"))

        seconde = AbilityFactory.ForChoiceAbility(
            "Take indirect damage equal to your ATK. Discard this obligation",
            degats_indirects_puis_defausser,
        ).SetHasNoTargetEffect()

        joueur.ChooseAbilities(effect, premiere, seconde)

    return [
        AbilityFactory.WhenThisObligationGiveToYou(
            essential_bloodlust,
        ),
    ]
