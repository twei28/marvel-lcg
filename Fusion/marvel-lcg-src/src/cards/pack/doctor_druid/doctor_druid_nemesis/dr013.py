from . import *

# Emotionally Overwhelmed (x2) — ATTACHEMENT NEMESIS. CONDITION. 1 boost.
# ⚠ NOM : les fichiers du zip disent « overcome by emotions ». LA CARTE et la
#   decklist disent EMOTIONALLY OVERWHELMED.
# Attach to your identity.
# Forced Interrupt: When your turn begins, discard an identity-specific event
#   from your hand.
# Alter-Ego Action: Stun your identity -> discard this card.
#
# CARTE DE REFERENCE
#  - `15026` (Scarlet Witch Nemesis) : attachement NEMESIS pose sur
#    l'identite, monte sur `AttachToFaceWhenPutIntoPlay("YourIdentity")`.
#  - `02048` pour `PlayerActionToDiscardThis`, la fabrique dediee a « action
#    -> defaussez cette carte ».
#
# TEXTE CONTRE CODE
#  « an identity-specific EVENT » -> EVENT ici, alors que `dr012` dit CARD.
#    Deux cartes du meme set, deux portees : ne pas recopier l'une sur l'autre.
#  « STUN your identity » -> DANS LE COUT (fleche), donc `CostFunc.Custom` :
#    le statut est le prix, pas l'effet. Le moteur n'a pas de cout « donner un
#    statut » tout fait.
#  « ALTER-EGO Action » -> sous-type dedie : on ne s'en debarrasse qu'en forme
#    civile, ce qui coute un tour de heros en plus du statut.


def GetAbilities() -> Sequence['Ability']:

    def au_debut_du_tour(effect: 'Effect', message: 'Message2') -> None:
        this = effect.this.CastTo(Attachment)
        Unused(this)
        joueur = message.GetToPlayer() if hasattr(message, "GetToPlayer") else None
        if joueur is None:
            joueur = Worlds.GetCurrentPlayer(effect)
        if joueur is None:
            return
        evenements = [f for f in joueur.hand_cards.Get()
                      if Event.IsType(f) and EstSpecifiqueIdentite(f)]
        if evenements:
            Faces.DiscardAll([evenements[0]], effect)

    def etourdir_l_identite(cibles: Sequence['CardFace'], effect: 'Effect') -> bool:
        Unused(cibles)
        joueur = Worlds.GetCurrentPlayer(effect)
        if joueur is None:
            return False
        identite = joueur.GetIdentity()
        if identite is None:
            return False
        Faces.GiveStatus([identite], "Stunned", effect)
        return True

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(
            "YourIdentity",
        ),
        AbilityFactory.WhenPlayerTurnBegin(
            AbilityType.ForcedInterrupt,
            "You",
            au_debut_du_tour,
        ),
        AbilityFactory.PlayerActionToDiscardThis(
            AbilityType.AlterEgoAction,
        ).SetCostFunc(CostFunc.Custom(None, etourdir_l_identite)),
    ]
