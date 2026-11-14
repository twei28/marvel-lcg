from . import *

# Advanced Arsenal — TRAITRISE (Hala Ultimatum). 1 icone de boost. 2 exemplaires.
# When Revealed: Give the villain a tough status card. If the villain already has a tough status card,
#   discard cards from the encounter deck until you discard an attachment or a minion and reveal it.
#
# Cartes de reference :
#  - « Give the villain a tough status card. If ... already ... » : `DonnerTenaceAuVillainOuSinon`
#    (hala_ultimatum/__init__.py, partagee avec gs154/gs155).
#  - « discard cards from the encounter deck until you discard an attachment OR a minion and reveal it » :
#    `Worlds.DiscardEncounterCardsUntil` avec `check_face_fn=...` EN KWARG DIRECT (il n'a pas de parametre
#    `finder` -- seulement `**kwargs: Unpack[CardFinder.KWArgs]` transmis tel quel au `CardFinder` final ;
#    `finder=CardFinder(...)` levait `TypeError` a l'execution, constate le 20/10/2026, corrige ici) pour
#    l'alternative « OR » (aucun `card_type` simple ne couvre deux types a la fois), modele
#    `skrull_menace/paibok/__init__.py` (`RevelerPouvoirDuDeck`) pour le motif general.
#
# ⚠ Mots-pieges : « an attachment OR a minion » (deux types valides, pas un seul) ; « reveal it » = la
# carte qui a stoppe la defausse, pas une autre ; « ALREADY has » = l'etat au moment ou cette carte se
# revele, avant que CETTE carte ne pose son propre tenace.


def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()

        def sinon(villain: 'Villain') -> None:
            Unused(villain)
            face = Worlds.DiscardEncounterCardsUntil(
                effect,
                check_face_fn=lambda f: Attachment.IsType(f) or Minion.IsType(f),
            )
            if face is not None and joueur is not None:
                face.Reveal(joueur, effect)

        DonnerTenaceAuVillainOuSinon(effect, sinon)

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
    ]
