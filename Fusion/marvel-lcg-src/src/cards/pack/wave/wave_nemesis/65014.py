from . import *

# Alontech Seawolf — ATTACHEMENT, WAVE NEMESIS 5/5. VEHICLE.
# Attach to the main scheme.
# Forced Interrupt: When the player phase begins, deal 1 damage to each
# player.
# Hero Action: Place 1 threat on the main scheme and discard an
# identity-specific card from your hand -> discard this card.
#
# « Attach to the main scheme » SANS verbe « When Revealed » : propriete
# imprimee passive, meme forme que l'officiel `04135` Twisted Reality
# (attache a une manigance annexe) -> `AbilityFactory.
# AttachToFaceWhenPutIntoPlay(MainScheme)` (attachment.py:47), qui accepte
# directement un `Type['CardFace']` comme cible.
# « When the player phase begins » -> `AbilityFactory.WhenPlayerPhaseBegin`
# (turn_phase.py:163), un declencheur de PARTIE (pas par joueur).
# « deal 1 damage to each player » -> `Players.ForEachPlayer` + degat direct
# sur `joueur.GetIdentity()` -- PAS `Utility.DealDamageToCharacterYouControl`
# (game/operate/utility.py:33), qui OFFRE UN CHOIX parmi tous les personnages
# controles (allies compris) : un degat « to a player » ne vise jamais un
# allie. Meme correctif que 65012 The Reyna Sirena, trouve le 22/9/2026 en
# testant cette carte-ci (le choix interactif ne repond pas correctement
# quand le declencheur de phase est envoye hors du fil de jeu normal, mais le
# vrai probleme est le CHOIX lui-meme, absent du texte imprime).
# Le cout double (« place threat AND discard ») empile deux `CostFunc` sur
# UNE capacite qui se defausse elle-meme -- modele
# `AbilityFactory.PlayerActionToDiscardThis` (attachment.py:8, utilise par
# ar010 Ire of Athena) + `CostFunc.PlaceThreatOn(1, "MainScheme")` +
# `CostFunc.Discard(card_class="IdentitySpecific", from_where=
# ["YourHandCards"], range=(1, 1))` -- « identity-specific » est un
# CARD_CLASS natif (`card_player.py:48`, `face.IsClass("IdentitySpecific")`),
# PLUS LARGE qu'un nom de heros precis (lecon dr003 : ne pas restreindre a un
# seul heros la ou le texte dit juste « identity-specific »).

def GetAbilities() -> Sequence['Ability']:

    def degats_debut_de_phase(effect: 'Effect', message: 'Message.WhenPhaseBegin') -> None:
        this = effect.this.CastTo(Attachment)
        Unused(message)

        Players.ForEachPlayer(
            effect,
            lambda joueur: this.DealDamage([joueur.GetIdentity()], 1, effect),
        )

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(
            MainScheme,
        ),
        AbilityFactory.WhenPlayerPhaseBegin(
            AbilityType.ForcedInterrupt,
            degats_debut_de_phase,
        ),
        AbilityFactory.PlayerActionToDiscardThis(
            AbilityType.HeroAction,
        ).SetCostFunc(CostFunc.PlaceThreatOn(1, "MainScheme"))
        .SetCostFunc(CostFunc.Discard(
            card_class="IdentitySpecific",
            from_where=["YourHandCards"],
            range=(1, 1),
        )),
    ]
