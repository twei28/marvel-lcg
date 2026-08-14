from . import *

# "He's Mine!"

def GetAbilities() -> Sequence['Ability']:

    def cest_le_mien(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)

        joueur = message.GetToPlayer()

        # ⚠ DEUX CARTES DE CE PACK S'APPELLENT « Bodyguard » : l'attachement
        # (wd026) et le sbire (wd028). Sans le filtre de type, le SBIRE en jeu
        # faisait croire que l'attachement l'etait — la traitrise deferlait au
        # lieu de balayer les sbires et de chercher l'attachement. Le texte, lui,
        # ne parle que de « the Bodyguard ATTACHMENT ».
        if Worlds.FindCardOnField(effect, name="Bodyguard", card_type=Attachment):
            # « Otherwise, this card gains surge. »
            ThisCardGainSurge(effect)
            return

        # « Discard each non-ELITE minion engaged with you. Place 1 threat on
        # the main scheme for each minion discarded this way. »
        sbires = [x for x in joueur.GetEngagedMinions() if not x.HasTrait("ELITE")]
        if sbires:
            Faces.DiscardAll(sbires, effect)
            this.PlaceThreatOnSchemes("MainScheme", len(sbires), effect)

        ChercherEtReveler(effect, name="Bodyguard", card_type=Attachment)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            cest_le_mien
        ),
    ]
