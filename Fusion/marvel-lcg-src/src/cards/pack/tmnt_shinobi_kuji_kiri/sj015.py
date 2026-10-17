from . import *

# Morphic Charm (sj015), Kuji-Kiri, evenement SPELL (Inkwire, TMNT Shinobi).
# Hero Action: Choose a minion or ally with a status card. Replace that status card with a different status card
# → draw 1 card.
#
# Carte de reference : `drs/invocation/09035` Vapors of Valtorr (« Choose a status card in play. Replace that
# status card with a different status card » : `DeclareStatusCard` puis `Faces.GiveStatus` et defausse de
# l'ancienne carte d'etat). Mots-cles (fiches lues AVANT le code) : Cloaked, Dazed, Intensified, Exposed.
#
# EXTENSION MOTEUR : `Player.DeclareStatusCard` (`game/player/model/player_ask.py`) ne proposait que Confused /
# Stunned / Tough. Quatre parametres optionnels de plus (`exposed`, `cloaked`, `dazed`, `intensified`, defaut
# False : 09035, 15004, 50020 inchanges) pour offrir les SEPT cartes d'etat du moteur.
#
# TEXTE CONTRE CODE
#  ⚠ « a MINION or ALLY with a status card » : sbire ou allie en jeu (pas un heros, pas un vilain) qui porte
#    au moins une carte d'etat, de n'importe quel joueur.
#  ⚠ « THAT status card » : celle que le joueur designe si le personnage en porte plusieurs genres.
#  ⚠ « a DIFFERENT status card » : un AUTRE genre que celui remplace (jamais le meme), parmi les genres que le
#    personnage peut recevoir (plafonds : un seul Dazed, un seul Cloaked, pas de Sonne/Desoriente sur un
#    Stalwart, Coriace limite, Intensified exige une carte d'etat).
#  ⚠ « Replace » : la nouvelle carte est posee PUIS l'ancienne defaussee ; si la nouvelle ne peut pas etre
#    posee, rien n'est remplace.
#  ⚠ « → draw 1 card » : la pioche est la suite du remplacement (elle n'a lieu que si le remplacement a eu lieu).

GENRES = ["Confused", "Stunned", "Tough", "Exposed", "Cloaked", "Dazed", "Intensified"]


def GetAbilities() -> Sequence['Ability']:

    def morphic_charm(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this, message)

        joueur = effect.GetInitiator()
        if joueur is None:
            return
        for cible in effect.targets:
            statut = cible.CastTo(CanStatus)
            presents = [g for g in GENRES if statut.HasStatus(g)]
            if not presents:
                continue
            ancien = presents[0] if len(presents) == 1 else joueur.AskChooseOneText(
                presents, [g for g in presents], "Status card to replace")

            def peut(genre: str) -> bool:
                if genre == ancien:
                    return False
                if genre == "Confused":
                    return statut.CanbeConfused()
                if genre == "Stunned":
                    return statut.CanbeStunned()
                if genre == "Tough":
                    return statut.CanGainTough()
                if genre == "Cloaked":
                    return statut.cloaked < statut.cloaked_max
                if genre == "Dazed":
                    return statut.CanbeDazed()
                if genre == "Intensified":
                    return statut.CanbeIntensified()
                return True  # Exposed : aucun plafond (exposed.md, « s'empile »)

            nouveau = joueur.DeclareStatusCard(
                confused=peut("Confused"), stunned=peut("Stunned"), tough=peut("Tough"),
                exposed=peut("Exposed"), cloaked=peut("Cloaked"), dazed=peut("Dazed"),
                intensified=peut("Intensified"),
            )
            if nouveau is None:
                continue
            anciennes = statut.components.status.deck.FindCards(name=ancien, card_type=StatusCard, max=1)
            if Faces.GiveStatus([cible], nouveau, effect):
                Faces.DiscardAll(anciennes, effect)
                joueur.DrawUp(1, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            morphic_charm,
        ).SetPlay()
        .SetTarget("Ally|Minion", has_status="Any"),
    ]
