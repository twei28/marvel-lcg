from . import *

# Make Ready the Bomb 2B — COMPLOT PRINCIPAL, face jouable. Seuil 9 par
# joueur, acceleration +1 par joueur, menace de depart 2 par joueur.
#
# Forced Response: After step 1 of the villain phase, place 1[per_hero] timer
#   counters on the Godbomb environment.
# Forced Response: After an enemy attacks and defeats an ally, place 1 timer
#   counter on the Godbomb environment.
# If this stage is completed, the players lose the game.
#
# ---------------------------------------------------------------------------
# CARTES DE REFERENCE
#
# - Etape 1 de la phase du vilain : 04113b (The Mad Doctor), meme fabrique
#   `AfterResolveVillainPhaseStep(ForcedResponse, 1, ...)` qu'en gb004b.
# - « After an enemy attacks and defeats an ally » : `AfterUnitDefeatedUnit`
#   avec `is_from_attack=True` (defeated.py:231) — c'est la difference avec
#   gb004b, ou le texte ne dit pas « attacks and ».
# - Defaite : la phrase exacte « <b>If this stage is completed, the players
#   lose the game. » suffit, le moteur ajoute l'ability tout seul
#   (scheme_main.py:28-35). On l'ecrit QUAND MEME ici, comme 50089b et wd055b,
#   pour que le module dise ce que la carte fait.
#
# ---------------------------------------------------------------------------
# TEXTE CONTRE CODE
#
# « 1[per_hero] timer counterS » -> « 1* », par joueur : c'est la seule des
#   deux reponses qui porte l'icone joueur.
# « an ENEMY » -> n'importe quel ennemi (vilain OU sbire), contrairement a
#   gb004b qui nomme Gorr.
# « ATTACKS AND defeats » -> uniquement par une attaque, pas par un degat
#   collateral : `is_from_attack=True`.
# « on the GODBOMB environment » -> l'helper `PoserTimer` du pack, qui ne
#   trouve rien si la carte a deja ete retournee sur sa face Necroverse. Le
#   texte ne prevoit pas ce cas : a l'etape 3, ce complot n'est plus en jeu.


def GetAbilities() -> Sequence['Ability']:

    def la_bombe_avance(effect: 'Effect', message: 'Message.AfterResolveVillainPhaseStep') -> None:
        this = effect.this.CastTo(MainScheme)
        Unused(this, message)

        PoserTimer(effect, "1*")

    def un_allie_tombe(effect: 'Effect', message: 'Message.AfterUnitDefeatedUnit') -> None:
        this = effect.this.CastTo(MainScheme)
        Unused(this, message)

        PoserTimer(effect, 1)

    return [
        AbilityFactory.AfterResolveVillainPhaseStep(
            AbilityType.ForcedResponse,
            1,
            la_bombe_avance,
        ),
        AbilityFactory.AfterUnitDefeatedUnit(
            AbilityType.ForcedResponse,
            Enemy,
            Ally,
            un_allie_tombe,
            is_from_attack=True,
        ),
        AbilityFactory.IfThisSchemeStageIsCompletedPlayersLoseTheGame(),
    ]
