from . import *

# Triple the Beatdown — EVENEMENT x2 (dm003/dm004, meme texte). ATTACK. SKILL.
# Cout 3, [physical].
# Hero Action (attack): Deal 3 damage to an enemy. Deal 3 damage to another
#   enemy. If you reduced this card's cost, ready 3-D Man.
#
# CARTES DE REFERENCE
#  - « Deal X damage to an enemy. Deal X damage to another enemy » (deux
#    cibles distinctes, DEUX INSTANCES PLEINES de degats, pas un partage) :
#    `.SetTarget(Enemy, range=(1, 2))` + un `DealDamage` SEPARE par cible.
#  - « If you reduced this card's cost, ready <heros> » : helper `CoutReduit`
#    du pack (`three_d_man/__init__.py`), et `Faces.ReadyAll` modele
#    **`sk019`** Provoked! pour « ready your hero ».
#
# TEXTE CONTRE CODE
#  « an enemy... ANOTHER enemy » : deux cartes distinctes (le moteur
#  l'impose), choisies ENSEMBLE ; un seul ennemi en jeu -> un seul degat (pas
#  de second ennemi a toucher, pas d'echec de la carte pour autant).
#  CORRECTIF (04/11/2026, trouve par `tools/cas/three_d_man.py`, trace par
#  TRACE_OPTIONS) : `.SetLabel('attack')` POSE SUR L'ABILITE force le moteur
#  a n'offrir qu'UNE SEULE cible au `SetTarget(Enemy, range=(1,2))`
#  (`target_num_range` tombe a [1,1] au lieu de [1,2] des que l'ability
#  porte ce label -- verifie en retirant juste le label, sans toucher au
#  reste : range redevient [1,2]). Le label est donc retire de L'ABILITE ;
#  chaque cible recoit sa PROPRE attaque PLEINE via `DealDamage([cible], 3,
#  effect, attack_in_event=True)` -- le parametre explicite (deja prevu par
#  le moteur, voir `card_face.py:DealDamage`) donne la MEME vraie attaque
#  (Retaliate, Overkill, « if this attack defeats »...) que le label
#  aurait donnee, mais UNE FOIS PAR CIBLE au lieu d'une fois sur la liste
#  entiere (qui partageait l'attaque au lieu de la dupliquer). ARBITRAGE
#  UTILISATEUR : deux phrases imprimees = deux instances INDEPENDANTES,
#  chacune une vraie attaque a 3 degats.
#  « If you REDUCED this card's cost » : compare le cout FACTURE au cout
#  IMPRIME, pas un flag pose par 3-D Man/3-D Man's Suit/Triune
#  Understanding. « ready 3-D MAN » : l'identite du joueur (forme heros,
#  seule forme ou cette carte est jouable).


def GetAbilities() -> Sequence['Ability']:

    def triple_the_beatdown(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)
        joueur = effect.GetInitiator()
        if joueur is None:
            return

        for cible in effect.targets:
            this.DealDamage([cible], 3, effect, attack_in_event=True)

        if CoutReduit(effect):
            identite = joueur.GetIdentity()
            if identite is not None:
                Faces.ReadyAll([identite], effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            triple_the_beatdown,
        ).SetPlay()
        .SetTarget(Enemy, range=(1, 2)),
    ]
