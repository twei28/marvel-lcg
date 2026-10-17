from . import *

# Yin (sj004), Kuji-Kiri, evenement SPELL (Inkwire, TMNT Shinobi).
# Hero Action: Heal 2 damage from a friendly character. Choose:
#  • Cloak a friendly character.
#  • Confuse an enemy.
#
# Mots-cles (fiches lues AVANT le code) : Cloak (`cloak.md`), Cloaked (`cloaked.md`).
# Cartes de reference : `lockjaw/lj024` et `cloak_dagger/cd004` (soin de N sur « un personnage ami » :
# `HealthUnits(cibles, N)`, cible `Friend`) ; `donatello/td005` (choix modal, Cloak par `Faces.GiveStatus`) ;
# `ShinobiCloak` (helper du socle Shinobi).
#
# TEXTE CONTRE CODE
#  ⚠ « Heal 2 damage FROM A FRIENDLY CHARACTER » : la cible est choisie a la mise en jeu (n'importe quel
#    personnage ami, avec ou sans degats : le « Choose » qui suit reste faisable) ; soigne jusqu'a 2.
#  ⚠ « Choose: » : UNE seule option, apres le soin ; « Cloak A friendly character » : un seul personnage
#    ami (jamais deux, contrairement a td005) ; une seule carte Cloaked par personnage (`cloak.md`).
#  ⚠ « Confuse AN enemy » : n'importe quel ennemi (un Stalwart ne peut pas etre desoriente).


def GetAbilities() -> Sequence['Ability']:

    def yin(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)

        joueur = effect.GetInitiator()
        if joueur is None:
            return
        this.HealthUnits(effect.targets, 2, effect)

        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Cloak a friendly character",
                lambda cibles: ShinobiCloak(effect, cibles),
            ).SetTarget(Friend),
            AbilityFactory.ForChoiceAbility(
                "Confuse an enemy",
                lambda cibles: Faces.GiveStatus(cibles, "Confused", effect),
            ).SetTarget(Enemy, canbe_confused=True),
        )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            yin,
        ).SetPlay()
        .SetTarget(Friend),
    ]
