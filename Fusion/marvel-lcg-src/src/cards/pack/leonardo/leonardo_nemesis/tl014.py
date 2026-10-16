from . import *

# Foot Patrol — COMPLOT ANNEXE nemesis, x1 (1/5). Crisis, StartingThreat 2*,
# Boost 2.
# When Defeated: Search the encounter deck and discard pile for a [[FOOT CLAN]]
#   minion and put it into play engaged with the first player.
#
# Cartes de reference :
#  - `40059` Superpower Training : `WhenSchemeBeDefeated(WhenDefeated, "This",
#    op)` sur un complot annexe ;
#  - `sm/27129` City in Chaos / `brawn/bw021` : `Search.EncounterCard(effect,
#    <joueur>, include_discard_pile=True, trait=..., card_type=Minion)` puis
#    `face.PutIntoPlay(joueur, effect)` (un sbire mis en jeu s'engage toujours,
#    minion.py:61) ;
#  - `Search.EncounterCard(..., who_perform="FirstPlayer")` et
#    `Worlds.GetFirstPlayer(effect)` pour « the first player ».
#
# ⚠ BASES AUTOMATIQUES (desc, aucun script) : `Crisis 1` (icone « ! » verifiee
# par comparaison d'image avec 01108 Crowd Control), `StartingThreat 2*`
# (menace PAR JOUEUR), `Boost 2` (deux icones, meme glyphe que l'obligation
# ls012).
#
# Mots-pieges :
#  - « search the encounter deck AND discard pile » : include_discard_pile=True ;
#  - « a [[FOOT CLAN]] minion » : trait FOOT CLAN ET type Minion ;
#  - « engaged with the FIRST player » : pas le joueur qui a vaincu le complot ;
#  - « (Shuffle) » non imprime, mais la fouille du deck rencontre melange par
#    defaut ;
#  - DECISION UTILISATEUR (15/10/2026) : si aucun sbire FOOT CLAN n'est trouve, rien ne se
#    passe (lecture litterale, pas de repli).


def GetAbilities() -> Sequence['Ability']:

    def foot_patrol(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        this = effect.this.CastTo(EncounterSideScheme)
        Unused(this, message)

        premier = Worlds.GetFirstPlayer(effect)
        if premier is None:
            return
        face = Search.EncounterCard(
            effect,
            premier,
            include_discard_pile=True,
            trait="FOOT CLAN",
            card_type=Minion,
        )
        if face:
            face.PutIntoPlay(premier, effect)

    return [
        AbilityFactory.WhenSchemeBeDefeated(
            AbilityType.WhenDefeated,
            "This",
            foot_patrol,
        ),
    ]
