from . import *

# * Jasper Barlow — SBIRE nemesis de Venus. GENIUS. RAT. PV 2, MNG 2, ATQ 0, boost etoile seul.
# When Revealed: Place a tough status card on each minion engaged with you.
#   (Venus' nemesis minion.)
# [star] Boost: Deal this card to the first player as a facedown encounter card.
#
# CARTES DE REFERENCE
#  - `tl015` Karai (pack leonardo) : `WhenThisRevealed(None, op)` + boost « deal this card to
#    the first player » (fabrique `BoostDonnerAuPremierJoueur`).
#  - `tm016` / `tr017` : joueur de la revelation = `message.GetToPlayer()`.
#  - `19001a` / `tg010` : `Faces.GiveStatus(faces, "Tough", effect)`.
#
# TEXTE CONTRE CODE
#  ⚠ « each minion engaged WITH YOU » -> les sbires engages avec le joueur a qui la carte est
#    distribuee (pas un autre joueur, pas les sbires non engages). Jasper lui-meme en fait
#    partie des qu'il est engage (un sbire revele s'engage avec le joueur AVANT sa capacite
#    « When Revealed ») : cas de test.
#  ⚠ « tough status card » : `Tough` (un sbire deja Tough n'en recoit pas un second).
#  ⚠ « (Venus' nemesis minion.) » : `desc.Nemesis = "Venus"`, lu par le moteur.
#  ⚠ Boost etoile, valeur de boost numerique 0 (aucune icone rouge sur le scan).


def GetAbilities() -> Sequence['Ability']:

    def jasper(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Minion)
        Unused(this)
        joueur = message.GetToPlayer()
        if joueur is None:
            return
        sbires = [m for m in joueur.GetEngagedMinions() if m is not None]
        if sbires:
            Faces.GiveStatus(sbires, "Tough", effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            jasper,
        ),
        BoostDonnerAuPremierJoueur(),
    ]
