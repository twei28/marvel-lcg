from . import *

# Triple the Heroics — EVENEMENT x2 (dm004/dm005... non, voir dm005 separe).
# SKILL. THWART. Cout 3, [mental].
# Hero Action (thwart): Remove 3 threat from a scheme. Remove 3 threat from
#   another scheme. If you reduced this card's cost, ready 3-D Man.
#
# CARTES DE REFERENCE : meme patron que dm003 Triple the Beatdown, cote
# manigance : `.SetTarget(Scheme2, range=(1, 2))` + un `RemoveThreatFromSchemes`
# SEPARE par cible. `CoutReduit` / `Faces.ReadyAll` : voir dm003.
#
# TEXTE CONTRE CODE : identique a dm003, en remplacant degats/ennemi par
# menace/manigance. « a scheme... ANOTHER scheme » : principale ou annexe,
# deux cartes distinctes choisies ensemble ; une seule manigance en jeu ->
# un seul retrait.
#  CORRECTIF (04/11/2026, meme trouvaille que dm003, confirmee par
#  TRACE_OPTIONS) : `.SetLabel('thwart')` SUR L'ABILITE force `SetTarget
#  (Scheme2, range=(1,2))` a n'offrir qu'UNE SEULE cible (`target_num_range`
#  = [1,1], pas [1,2]). Le label est retire de l'ability ; chaque cible
#  recoit son PROPRE contre PLEIN via `RemoveThreatFromSchemes([cible], 3,
#  effect, thwart_in_event=True)` -- parametre AJOUTE au moteur ce jour
#  (`card_face.py`), symetrique de `attack_in_event` sur `DealDamage` :
#  force un VRAI contre (`CanThwart.SpecialThwart`) sans dependre du label
#  de l'ability qui appelle, donc disponible UNE FOIS PAR CIBLE.


def GetAbilities() -> Sequence['Ability']:

    def triple_the_heroics(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)
        joueur = effect.GetInitiator()
        if joueur is None:
            return

        for cible in effect.targets:
            this.RemoveThreatFromSchemes([cible], 3, effect, thwart_in_event=True)

        if CoutReduit(effect):
            identite = joueur.GetIdentity()
            if identite is not None:
                Faces.ReadyAll([identite], effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            triple_the_heroics,
        ).SetPlay()
        .SetTarget(Scheme2, range=(1, 2)),
    ]
