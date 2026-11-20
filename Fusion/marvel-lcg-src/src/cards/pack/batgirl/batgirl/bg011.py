from . import *

# Grapple Line — amelioration, cout 1, [energy]. « Interrupt (lue en Reponse : le compteur est reinitialise a l'entree en jeu): If you paid for this card using a [physical] resource, place a recon
# counter on Grapple Line. Action: Discard Grapple Line → ready a friendly character. If there is a recon counter on Grapple Line,
# draw a card. »
# Cartes de reference : `06012` Valkyrie (`paid_resources` a l'entree en jeu), `53009` Aerial Recon (compteur `recon`, `PlaceCountersInternal`).
# ⚠ Le compteur se LIT avant la defausse : la carte n'est donc pas payee en cout, elle se defausse en fin d'operation.


def GetAbilities() -> Sequence['Ability']:

    def marquer_payee(effect: 'Effect', message: 'Message.WhenPlayerPlayCard') -> None:
        # La fenetre du JEU de la carte porte le paiement (`paid_resources`, comme pour les soutiens bg008/bg009).
        message.played_face.bg_payee_physique = Compter(effect, message.paid_resources, "R") > 0

    # Le compteur est remis a zero quand la carte s'attache au heros : on retient « payee en [physical] » (marquer_payee) et on le pose
    # APRES l'attachement (AfterCardAttachTo).
    def pose_apres_attache(effect: 'Effect', message: 'Message.AfterCardAttachTo') -> None:
        if getattr(effect.this, "bg_payee_physique", False):
            effect.this.bg_payee_physique = False
            Faces.PlaceCountersOn([effect.this], 1, 'recon', effect)

    def grapple_line(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this
        joueur = JoueurDeCetteCarte(effect)
        avec_recon = this.GetCounters('recon') > 0
        Faces.ReadyAll(effect.targets, effect)
        if avec_recon and joueur is not None:
            joueur.DrawUp(1, effect)
        Faces.DiscardAll([this], effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.WhenPlayerPlayCard(
            AbilityType.Interrupt, "You", CardFinder(name="Grapple Line"), marquer_payee,
        ).NoOutOfPlayLimit(),
        AbilityFactory.AfterCardAttachTo(AbilityType.Response, "This", None, pose_apres_attache),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            grapple_line,
        ).SetTarget(check_fn=lambda effect, face: Identity.IsType(face) or Ally.IsType(face), from_where=["YouControlCards"]),
    ]
