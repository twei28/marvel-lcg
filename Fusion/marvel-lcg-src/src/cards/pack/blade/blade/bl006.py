from . import *

# Vampiric Reflexes — EVENEMENT, cout 0, [energy]. DEFENSE. SUPERPOWER. x2.
# Hero Interrupt (defense): When you would take any amount of damage from an
#   attack, prevent all of that damage. You may exhaust a WEAPON upgrade you
#   control to gain retaliate 1 until the end of the round.
#
# CARTES DE REFERENCE
#  - `03005` EM Shield : `WhenUnitWouldTakeDamage(Interrupt, "You", op,
#    is_from_attack=True).SetLabel('defense')` + `message.PreventDamage("All")`.
#  - `12016` Moxie : `hero.GainUntilRoundEnd(effect, ...)`, qui accepte
#    `retaliate=` (correctif du 04/08/2026).
#  - `bl003` : l'option facultative « exhaust a WEAPON upgrade ».
#
# TEXTE CONTRE CODE
#  ⚠ « When YOU would take ... from an ATTACK » -> l'identite, degats d'attaque
#    seulement (`is_from_attack=True`) : une traitrise passe.
#  ⚠ « prevent ALL of that damage » -> `PreventDamage("All")`.
#  ⚠ « gain retaliate 1 until the END OF THE ROUND » -> le heros, pas la carte
#    (`GainUntilRoundEnd`). Une riposte qui part pendant la MEME attaque n'est
#    pas garantie (la riposte se lit quand l'attaquant frappe ; ici le gain se
#    fait pendant l'interruption, avant la frappe : le cas de test tranche).


def GetAbilities() -> Sequence['Ability']:

    def reflexes(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)
        message.PreventDamage("All", effect)

        joueur = JoueurDeCetteCarte(effect)
        heros = HerosDuJoueur(effect, joueur)
        if joueur is None or heros is None or not ArmesPretes(joueur):
            return

        def riposter(armes: Sequence['CardFace']) -> None:
            outils = [a for a in armes if a is not None]
            if not outils:
                return
            Faces.ExhaustAll(outils, effect)
            heros.GainUntilRoundEnd(effect, retaliate=1)

        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Exhaust a WEAPON upgrade you control to gain retaliate 1 until the end of the round",
                riposter,
            ).SetTarget(CardFinder(card_type=Upgrade, trait=TRAIT_WEAPON),
                        from_where=["YouControlCards"], canbe_exhaust=True),
            forced=False,
        )

    return [
        AbilityFactory.WhenUnitWouldTakeDamage(
            AbilityType.HeroInterrupt,
            "You",
            reflexes,
            is_from_attack=True,
        ).SetPlay().SetLabel('defense'),
    ]
