from . import *

# Extermination! — COMPLOT ANNEXE nemesis (1/5). Menace 2 par joueur,
#   icone d'ACCELERATION, boost 2.
# When Defeated: Search the encounter deck and discard pile for a MOUSER or
#   FLYBORG minion and put it into play engaged with the first player.
#
# CARTES DE REFERENCE
#  - `27068` Dirt Trap / `47016` : `WhenSchemeBeDefeated(AbilityType.
#    WhenDefeated, "This", op)` pour « When Defeated » d'une manigance annexe.
#  - `01128` The Masters of Evil : « put that minion into play engaged with
#    the first player » = `Worlds.GetFirstPlayer(effect)` +
#    `face.PutIntoPlay(first_player, effect)` (le sbire s'engage tout seul).
#  - `search.py:47` `Search.EncounterCard(effect, "FirstPlayer",
#    include_discard_pile=True, finder=...)` : deck rencontre ET defausse.
#  - `01109` Bomb Scare : `desc.Acceleration = "1"`, icone comparee par IMAGE
#    sur le scan (maison soulignee marquee d'une croix) — lue nativement.
#
# TEXTE CONTRE CODE
#  « the encounter deck AND discard pile » -> `include_discard_pile=True`.
#  « a MOUSER OR FLYBORG minion » -> UN sbire portant l'un des deux traits
#    (OU), type Minion. Traits ecrits au PLURIEL (voir __init__).
#  « engaged with the FIRST player » -> pas le joueur qui a vaincu la manigance.
#  « Search » : melange du deck rencontre par defaut.
#  Nombres : menace 2 « par joueur » (icone) -> `StartingThreat "2*"`.
#
# Traits : le texte dit « MOUSER or FLYBORG » (singulier), les lignes de traits
# « MOUSERS » / « FLYBORGS ». Decision du 15/10/2026 : traits PLURIELS conserves.
# Aucun sbire trouve : rien ne se passe (meme decision).


def GetAbilities() -> Sequence['Ability']:

    def exterminer(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        this = effect.this.CastTo(EncounterSideScheme)
        Unused(this, message)
        premier = Worlds.GetFirstPlayer(effect)
        face = Search.EncounterCard(
            effect,
            "FirstPlayer",
            include_discard_pile=True,
            finder=CardFinder(traits=TRAITS_ESSAIM),
            card_type=Minion,
        )
        if face is not None:
            face.PutIntoPlay(premier, effect)

    return [
        AbilityFactory.WhenSchemeBeDefeated(
            AbilityType.WhenDefeated,
            "This",
            exterminer,
        ),
    ]
