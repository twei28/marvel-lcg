from . import *

# Solid Sound Body
# SIDE SCHEME. Hinder 1[per_hero].
# Klaw gets +10 hit points. (When this scheme is defeated, Klaw loses those hit
#   points.)
# When Defeated: Give Klaw a facedown boost card.
#
# « Hinder 1[per_hero] » est porte par le desc (`"Hinder": "1*"`), pas par le
# code.
#
# Les +10 PV sont un effet CONTINU tant que la machination est en jeu :
# `GiveKeywordToInPlayWhenApplyThis` (modele 40195b, ou un environnement
# accorde un mot-cle a ce qui est en jeu). La parenthese « quand cette
# machination est vaincue, Klaw perd ces PV » est donc automatique, c'est le
# propre d'un effet continu : rien a coder pour elle.


def GetAbilities() -> Sequence['Ability']:

    def quand_vaincue(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        # `SideScheme` n'existe pas dans l'espace de noms des packs : le type
        # d'une machination secondaire du deck rencontre est
        # `EncounterSideScheme` (modele ag011, av014, 42026). Avec le mauvais
        # nom, le `When Defeated` levait un NameError AVALE par le moteur : la
        # carte boost n'etait jamais donnee, et rien ne le signalait.
        this = effect.this.CastTo(EncounterSideScheme)
        Unused(this)
        klaw = Worlds.FindCardOnField(effect, name="Klaw")
        if klaw is None:
            return
        klaw.GiveFacedownBoostCardsInternal(1, effect, None)

    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            CardFinder(name="Klaw"),
            health=10,
        ),
        # La fabrique s'appelle `WhenSchemeBeDefeated` et prend la machination
        # visee en 2e argument ; « This » suffit ici.
        AbilityFactory.WhenSchemeBeDefeated(
            AbilityType.WhenDefeated,
            "This",
            quand_vaincue,
        ),
    ]
