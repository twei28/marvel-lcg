from . import *

# Red Herring — TRAITRISE x2. Boost 1.
# In expert mode, this card gains incite 1.
# When Revealed : Move to a location not mentioned on the LEAD card in your play area, if able. Choose to either stun or confuse your identity.
#
# Cartes de reference : `AbilityFactory.IfExpertModeThisGainKeyword(incite=1)` (game/ability/factory/expert.py), `Ville.Placer` (deplacement sans
# adjacence, ajoute le 22/10/2026), `joueur.AskChooseFace`, `ChooseAbilities` a deux branches (pu004 / Kang).
# ⚠ « a location NOT MENTIONED on the LEAD card » : le lieu de chacune des pistes de mon aire est exclu (`LieuDeLaPiste`) ; j'exclus aussi le
# lieu ou je suis deja (« move » = changer) ; le JOUEUR choisit parmi les autres ; « if able » : aucun lieu possible = pas de deplacement, mais
# l'identite est quand meme etourdie ou confuse ; « stun OR confuse » : au choix du joueur.

def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        etat = Ville.Etat(effect)
        if etat is not None and joueur is not None:
            interdits = {LieuDeLaPiste(f.paper.card_id) for f in joueur.obligations_area.Get() if f.HasTrait("LEAD")}
            ici = Ville.Lieu(effect, joueur)
            possibles = [etat.cases[c] for c in sorted(etat.cases)
                         if etat.cases[c].paper.card_id not in interdits and etat.cases[c] is not ici]
            if possibles:
                choisi = possibles[0] if len(possibles) == 1 else joueur.AskChooseFace(possibles, effect)
                case = Ville.CaseDe(effect, choisi) if choisi is not None else None
                if case is not None:
                    Ville.Placer(effect, joueur, case)
        identite = joueur.GetIdentity()
        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility("Stun your identity", lambda cibles: Faces.GiveStatus(cibles, "Stunned", effect)).SetTarget([identite], canbe_stunned=True),
            AbilityFactory.ForChoiceAbility("Confuse your identity", lambda cibles: Faces.GiveStatus(cibles, "Confused", effect)).SetTarget([identite], canbe_confused=True),
        )

    return [
        AbilityFactory.IfExpertModeThisGainKeyword(incite=1),
        AbilityFactory.WhenThisRevealed(None, revele),
    ]
