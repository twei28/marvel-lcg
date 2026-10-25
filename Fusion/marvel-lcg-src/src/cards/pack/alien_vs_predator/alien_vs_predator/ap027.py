from . import *

# Killing Ground — TRAITRISE. Boost 2.
# When Revealed: Move all threat from the villain's side scheme with the most threat to the main scheme. If no threat was moved this way,
#   exhaust your identity. If you cannot, stun or confuse your identity.
#
# Cartes de reference : deplacer de la menace = la retirer puis la poser (`RemoveThreatFromSchemes` + `PlaceThreatOnSchemes`, regle des
#   « move » du moteur, 07042) ; « exhaust your identity » : `Faces.ExhaustAll` ; « If you cannot » : identite deja inclinee.
#
# ⚠ Mots-pieges :
#  - « the villain's side scheme with the MOST threat » : Expanding Hive ou Skulls ; egalite -> le joueur choisit ; 0 partout -> rien ;
#  - « If you cannot » : l'identite est deja inclinee -> le joueur choisit Sonne OU Desoriente.


def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this
        joueur = JoueurDuMessage(message, effect)
        manigances = [m for m in ManigancesPermanentes(effect) if m.threat > 0]
        if manigances:
            plus = max(m.threat for m in manigances)
            ex_aequo = [m for m in manigances if m.threat == plus]
            source = ex_aequo[0] if len(ex_aequo) == 1 else \
                (joueur.AskChooseFace(ex_aequo, effect, prompt="Move all threat from") or ex_aequo[0])
            n = source.threat
            this.RemoveThreatFromSchemes([source], n, effect)
            this.PlaceThreatOnSchemes("MainScheme", n, effect)
            return
        identite = joueur.GetIdentity()
        if identite.IsReady():
            Faces.ExhaustAll([identite], effect)
            return
        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility("Stun your identity", lambda targets: Faces.GiveStatus([identite], "Stunned", effect)),
            AbilityFactory.ForChoiceAbility("Confuse your identity", lambda targets: Faces.GiveStatus([identite], "Confused", effect)),
        )

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
    ]
