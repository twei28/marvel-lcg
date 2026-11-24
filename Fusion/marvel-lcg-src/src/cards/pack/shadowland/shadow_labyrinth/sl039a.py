from . import *

# Chamber of Vile Secrets (2A) — MANIGANCE PRINCIPALE, stade 2.
# When Revealed : Do each of the following : 1. Set Shifting Corridors aside. 2. Find the chosen Dark Protege villain. Discard each status card, token, and attached card
#   from it. 3. Reveal the chosen villain's side A (side B instead in expert mode).
#
# Cartes de reference : shadowland/shadows_in_the_night/sl001a (`Reveal(None, effect)` d'un vilain de cote), skrull_menace/skrull_empire/__init__ (`Faces.MoveAllTo` du vilain
# sortant, vilain suivant revele), gmw/collector_2/16083a (`Worlds.AsideDeck`), punisher_mcdc_2026/capo_of_the_past/pu139 (le sbire cree).
# ⚠ Mots-pieges : « set aside » (de cote, PAS defaussee ni retiree de la partie) ; « Find the chosen villain » : s'il combattait comme sbire (Whisper in the Dark, sl040),
#  le sosie est retire de la table avec TOUT ce qui lui est attache (Whisper va dans la defausse piege) : la vraie carte, elle, est restee de cote, intacte ; « each status
#  card, token, and attached card » ; « side B instead in expert mode » : en expert on montre la face B (le vilain Dark Protege est alors a sa seconde face).


def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        Unused(message)
        premier = Worlds.GetFirstPlayer(effect)
        # 1. Shifting Corridors de cote
        corridors = Corridors(effect)
        if corridors is not None:
            Faces.MoveAllTo([corridors], Worlds.AsideDeck(effect), effect)
        # 2. le vilain choisi : un sosie (sbire) encore en jeu est retire avec ses attachements, ses statuts et ses jetons
        for sosie in SbiresSosies(effect):
            Faces.DiscardAll(list(sosie.GetAttachedAttachments()), effect)
            Faces.RemoveAllFromGame([sosie], effect)
        carte = VilainChoisi(effect)
        if carte is None:
            return
        # 3. sa face A (B en expert)
        if Worlds.IsExpert(effect):
            carte.card.Flip(effect)
            carte = carte.card.face            # ⚠ la face B est une AUTRE face : reveler l'ancienne laisserait la B sans deck de rencontre (plantage a la defaite)
        carte.Reveal(premier, effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
    ]
