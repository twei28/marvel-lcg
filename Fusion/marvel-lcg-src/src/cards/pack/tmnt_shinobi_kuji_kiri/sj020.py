from . import *

# Æthreal Shift (sj020), Kuji-Kiri, evenement DEFENSE SPELL THWART (Inkwire, TMNT Shinobi).
# Hero Action (defense/thwart): When your hero would take any amount of damage from an attack, prevent all of
# that damage. Remove threat from a scheme equal to the amount of damage prevented this way.
#
# ⚠ QUESTION Q-K1 RESOLUE le 17/10/2026 (`.planning/tmnt/shinobi-reponses.md`) : Hero INTERRUPT confirme ; le texte affiche garde le « Hero Action » imprime. Rappel : le scan imprime « Hero ACTION » devant
# un declencheur « When your hero WOULD take damage » (formulation d'une INTERRUPTION). Lecture retenue : Hero
# INTERRUPT (coquille de type confirmee par l'utilisateur).
#
# Cartes de reference : `tmnt_aspect_protection/up004` Autodefenestration (« Hero Interrupt (defense): When you
# would take any amount of damage from an attack, prevent all of that damage » : `WhenUnitWouldTakeDamage(...,
# "You", is_from_attack=True)` + `PreventDamage("All")`, label 'defense') ; `determination/dt046` (retirer de la
# menace en consequence : `RemoveThreatFromSchemes`, `ForChoiceAbility.SetTarget(Scheme2)`).
#
# TEXTE CONTRE CODE
#  ⚠ « would take ANY amount of damage FROM AN ATTACK » : seulement des degats d'attaque (`is_from_attack`) ;
#    « YOUR hero » : le heros du joueur (forme heros ; l'alter-ego n'est pas un heros).
#  ⚠ « prevent ALL of that damage » : toute la quantite ; « threat ... EQUAL TO the amount of damage prevented
#    THIS way » : la quantite reellement prevenue (lue AVANT la prevention), sur UNE manigance au choix.
#  ⚠ Labels 'defense' et 'thwart' (parenthese imprimee).


def GetAbilities() -> Sequence['Ability']:

    def aethreal_shift(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)

        joueur = effect.GetInitiator()
        prevenus = message.will_take_damage
        message.PreventDamage("All", effect)
        if joueur is None or prevenus <= 0:
            return
        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Remove threat from a scheme equal to the damage prevented",
                lambda cibles: this.RemoveThreatFromSchemes(cibles, prevenus, effect),
            ).SetTarget(Scheme2, has_threat=True),
        )

    return [
        AbilityFactory.WhenUnitWouldTakeDamage(
            AbilityType.HeroInterrupt,
            "You",
            aethreal_shift,
            is_from_attack=True,
        ).SetPlay().SetLabel('defense', 'thwart'),
    ]
