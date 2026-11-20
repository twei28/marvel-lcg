from . import *

# * Faith — ALLIE (SLAYER), cout 3, [wild]. THW 1*, ATK 2*, PV 3. Unique. Linked (Faith minion).
# Interrupt: When Faith is defeated, choose a friendly SLAYER character → ready that character.
#
# CARTES DE REFERENCE
#  - `wt020` / `40024` : `WhenUnitWouldBeDefeated(Interrupt, "This", op)` pour « when X is defeated » en INTERRUPTION (avant la defaite).
#  - `Faces.ReadyAll([face], effect)` (an001a, 31009, ho011) pour redresser.
#  - `mv001a` / `mv003` : `CardFinder2(trait, Friend)` pour « a friendly TRAIT character » (identite ET allies).
#  - Linked : fiche `mots-cles/linked.md`. ⚠ `desc.Linked` n'est PAS pose : il vaudrait « Faith », le NOM de cette carte-ci, et la
#    ferait se lier a elle-meme. Le minion Faith n'est pas fourni par le Drive.
#
# TEXTE CONTRE CODE
#  « When Faith is defeated » -> `WhenUnitWouldBeDefeated` sur "This", `Interrupt` nu. « choose a friendly SLAYER character » ->
#    UN personnage allie portant le trait (Faith elle-meme y compte : elle est SLAYER). « ready » -> `ReadyAll`.
#  Chiffres : aucun (cout 3, THW 1*, ATK 2*, PV 3 dans cards.json).


def GetAbilities() -> Sequence['Ability']:

    def faith_defaite(effect: 'Effect', message: 'Message.WhenUnitWouldBeDefeated') -> None:
        this = effect.this.CastTo(Ally)
        Unused(this, message)
        Faces.ReadyAll(effect.targets, effect)

    return [
        AbilityFactory.WhenUnitWouldBeDefeated(
            AbilityType.Interrupt,
            "This",
            faith_defaite,
        ).SetTarget(CardFinder2(TRAIT_SLAYER, Friend)),
    ]
