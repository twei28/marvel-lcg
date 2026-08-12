from . import *

# Power Couple — custom « ekAugust » (carte basique du pack)
# Team-Up (Jessica Jones and Luke Cage). Max 1 per deck.
# Hero Action: Give Jessica Jones and Luke Cage a tough status card. Then, draw
#   an amount of cards equal to the amount of tough status cards among friendly
#   characters.
#
# ECART ASSUME : la cle `TeamUp` de cards.json suppose DEUX heros en jeu. Ici
# Luke Cage est l'allie signature de Jessica Jones (jj002), pas un heros : la
# restriction est donc portee par la condition de jeu ci-dessous plutot que par
# le mot-cle du moteur.

LUKE_CAGE = "Luke Cage"


def GetAbilities() -> Sequence['Ability']:

    def couple_present(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> bool:
        initiator = effect.GetInitiator()
        if initiator is None:
            return False
        identity = initiator.GetIdentity()
        if identity is None or "Jessica Jones" not in identity.name:
            return False
        return Worlds.FindCardOnField(effect, name=LUKE_CAGE) != None

    def power_couple(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)

        initiator = effect.GetInitiator()

        cibles: List['CardFace'] = []
        hero = initiator.GetHero()
        if hero:
            cibles.append(hero)
        luke = Worlds.FindCardOnField(effect, name=LUKE_CAGE)
        if luke:
            cibles.append(luke)
        Faces.GiveStatus(cibles, "Tough", effect)

        total = 0
        for face in Worlds.GetOnFieldFriendlyCharacters(effect):
            total += face.GetStatusSize("Tough")
        if total:
            initiator.DrawUp(total, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            power_couple,
            conditions=[couple_present],
        ).SetPlay(),
    ]
