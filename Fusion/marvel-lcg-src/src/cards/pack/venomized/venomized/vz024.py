from . import *

# * In the Thick of It — MANIGANCE-JOUEUR, cout 1, RES [physical].
# Menace de depart 3 PAR JOUEUR. Victory 0.
# When Defeated: Each player may search their deck and discard pile for an
#   upgrade with the SYMBIOTE trait and put it into play. (Shuffle.)
#
# CARTE DE REFERENCE
#  - `40019` * Lock and Load (Agression, pack next_evol) : MEME PHRASE au
#    filtre pres — elle cherche une amelioration [[WEAPON]] de cout 3 ou
#    moins, celle-ci une amelioration [[SYMBIOTE]] sans limite de cout. Corps
#    repris, `cost_less_than` retire.
#
# TEXTE CONTRE CODE
#  ⚠ « MAY search » -> `may=True` : la recherche est facultative, une joueuse
#    peut refuser (pour ne pas melanger son deck, notamment).
#  ⚠ « EACH player » -> `Players.ForEachPlayer`, y compris celui qui n'a pas
#    contre la manigance.
#  ⚠ « Victory 0 » et « 3 menaces par joueur » sont dans `cards.json`
#    (`Victory`, `StartingThreat: "3*"`), pas ici : l'etoile est la notation
#    native du « par joueur ».
#
# ⚠⚠ CETTE CARTE A FAIT TOMBER UN DEFAUT DU MOTEUR, PAS L'INVERSE.
# Son « When Defeated » ne partait jamais sous le harnais, et la carte
# OFFICIELLE `40019` Lock and Load, montee dans la meme position, echouait a
# l'identique. Cause reelle, trouvee dans le journal du processus fils
# (`/tmp/capacites_*.log`) : `selector_end.py` portait un
# `assert deck.GetSize() != 0` qui rendait INATTEIGNABLE la branche ecrite
# juste en dessous, celle qui prevoit justement le deck vide. Toute recherche
# qui sort la derniere carte d'un deck faisait tomber le moteur, et les cartes
# cherchees disparaissaient de TOUTES les zones.
# Assert retire le 09/09/2026. Les deux cartes sont desormais testees, et le
# cas « 40019 Lock and Load » garde le correctif.

def GetAbilities() -> Sequence['Ability']:

    def in_the_thick_of_it(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        this = effect.this.CastTo(PlayerSideScheme)
        Unused(this, message)

        def pour_chaque_joueur(player: 'Player'):
            face = Search.PlayerCard(
                effect,
                player,
                include_player_deck=True,
                include_discard_pile=True,
                trait=SYMBIOTE,
                card_type=Upgrade,
                may=True,
            )
            if face:
                face.PutIntoPlay(player, effect)

        Players.ForEachPlayer(effect, pour_chaque_joueur)

    return [
        AbilityFactory.WhenSchemeBeDefeated(
            AbilityType.WhenDefeated,
            "This",
            in_the_thick_of_it,
        ),
    ]
