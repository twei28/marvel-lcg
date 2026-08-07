from . import *

# Parting Shots — custom « Rainy »
# Hero Interrupt (attack): When an enemy would initiate an attack against
# you, deal 2 damage to that enemy. This attack gains ranged. You may flip
# to alter-ego form → that enemy schemes instead.
#
# Modele pour le declencheur : Camouflage (72008, meme projet, pack Venom
# Eddie Brock), meme structure « Hero Interrupt (attack), quand un ennemi
# initierait une attaque -> lui infliger des degats » sur
# `Message.WhenUnitWouldAttack`, cible = `message.attacker`,
# `.SetLabel('attack')`. Ici la version « contre toi » de ce declencheur :
# `AbilityFactory.WhenUnitAttackYou` (raccourci de
# `WhenUnitInitiatesAttackAgainst(attacker, "You", ...)`,
# src/game/ability/factory/do_attack.py:161), qui colle mot pour mot a
# « against you » du texte imprime. Carte jouee depuis la main : `.SetPlay()`,
# comme Aerial Agility (42004), autre Hero Interrupt (attack/defense) en
# Event.
#
# Modele pour « cette attaque gagne distance » : `message.GainRanged(effect)`
# sur le `WhenUnitWouldAttack` en cours (Paladin's Pistol 56118, Lockheed
# 78022, et notre propre Burst Fire 79003).
#
# Modele pour « bascule optionnelle en alter-ego » : le helper du projet
# `YouMayFlipToYourAlterEgoForm` (src/cards/pack/__init__.py:132), utilise
# par toutes les obligations « You may flip to alter-ego form » (Eviction
# Notice 01165 notamment). Non reutilise tel quel ici car il ne fait QUE
# retourner la forme : Parting Shots doit, dans le MEME choix, enchainer sur
# « cet ennemi manigance au lieu d'attaquer », donc le choix est reecrit en
# ligne avec les deux effets dans le meme lambda.
#
# Piege nomme du projet : la methode sur l'identite s'appelle bien
# `ChangeToForm` (verifie en lisant src/game/card/face/card_type/identity.py:77
# juste avant d'ecrire cette ligne) -- PAS `ChangeForm`, qui n'existe pas et
# ne serait attrape ni par test_cards ni par test_capacites tant que ce choix
# optionnel n'est pas explicitement exerce.
#
# Modele pour « cet ennemi manigance au lieu d'attaquer » : Invisibility Gear
# (51019, officiel), `message.DoSchemeInstead(effect)` sur le
# `WhenUnitWouldAttack` -- annule l'attaque (`SetBeInstead`) et fait manigancer
# l'ennemi contre le joueur cible a sa place.
#
# La bascule est un choix du joueur : chemin que le pilote (`verifier_api_cartes`)
# decline par defaut, donc `identity.ChangeToForm` et `message.DoSchemeInstead`
# ne seront exerces qu'en jeu reel derriere ce choix -- non couvert par
# test_cards/test_capacites en configuration par defaut.

def GetAbilities() -> Sequence['Ability']:

    def parting_shots(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        this = effect.this.CastTo(Event)
        cible = message.attacker

        this.DealDamage([cible], 2, effect)
        message.GainRanged(effect)

        joueur = effect.GetInitiator()

        def basculer(targets: Sequence['CardFace']) -> None:
            Unused(targets)
            joueur.GetIdentity().ChangeToForm(AlterEgo, effect)
            message.DoSchemeInstead(effect)

        joueur.MayChooseOneAbility(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Flip to alter-ego form → that enemy schemes instead",
                basculer,
            ),
        )

    return [
        AbilityFactory.WhenUnitAttackYou(
            AbilityType.HeroInterrupt,
            Enemy,
            parting_shots,
        ).SetPlay().SetLabel('attack'),
    ]
