from . import *

# * Kitsune — ALLIE 3 [energy], ATK 1 (1), THW 1 (1), PV 3. FOX. THIEF.
# Response: After you play Kitsune from your hand, choose: • Cloak Kitsune. • Daze an enemy.
#
# MOTS-CLES (fiches lues AVANT le code) : cloak.md, daze.md.
# CARTES DE REFERENCE
#  - `04040` * Spider-Girl : « After you play Spider-Girl from your hand » = `AfterYouPlayThisFromHand(Response, ..)`.
#  - `ua002` / `20008` : « choose: • ... • ... » = `ChooseAbilities` de deux `ForChoiceAbility`.
#  - `ta014` : « Cloak <la carte elle-meme> » = `Faces.GiveStatus([this], "Cloaked", effect)`.
# TEXTE CONTRE CODE
#  ⚠ « play from your HAND » : pas une mise en jeu par un autre effet.
#  ⚠ « choose » : une seule branche. « an enemy » : vilain ou sbire.
#  ⚠ Homonyme du sbire nemesis d'Alopex `ta014` * Kitsune (aucun lien de regles).


def GetAbilities() -> Sequence['Ability']:

    def kitsune(effect: 'Effect', message: 'Message.AfterPlayerPlayedCard') -> None:
        this = effect.this.CastTo(Ally)
        Unused(message)
        effect.GetInitiator().ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Cloak Kitsune",
                lambda cibles: Faces.GiveStatus([this], "Cloaked", effect),
            ),
            AbilityFactory.ForChoiceAbility(
                "Daze an enemy",
                lambda cibles: Faces.GiveStatus(cibles, "Dazed", effect),
            ).SetTarget(Enemy),
        )

    return [
        AbilityFactory.AfterYouPlayThisFromHand(
            AbilityType.Response,
            kitsune,
        ),
    ]
