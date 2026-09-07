from . import *

# Embraced — ATTACHEMENT nemesis (N 6/8 et 7/8). CONDITION. 2 boost.
# Attached minion gains the VAMPIRE trait and gets +X hit points where X is
#   equal to their printed hit points. Attacks with piercing deal double damage
#   to attached minion.
# When Revealed: Seek a non-VAMPIRE minion from the encounter deck, reveal it
#   and attach Embraced to it.
#
# CARTES DE REFERENCE
#  - `an008` / `dd010` : `GiveKeywordToAttached(<type>, trait=..., health=...)`,
#    `health` accepte un `Callable[[Effect], int]` (asset.py:13).
#  - `39051` : le doublement, cible `"AttachedMinion"` (condition/card_type.py:39).
#  - `hood/ransacked_armory` `SearchEncounterDeckForMinionAndAttachTo` et
#    `01190` : `Search.EncounterCard(...)` puis `face.Reveal(joueur, effect,
#    if_entered_play=...)` + `AttachTo2`.
#  - fiche seek.md : chercher dans la zone nommee, le DECK rencontre seulement.
#
# TEXTE CONTRE CODE
#  ⚠ « +X hit points where X = their PRINTED hit points » -> `printed_health`
#    de l'hote, lu a chaque application (un Hydra Bomber 2 PV passe a 4).
#  ⚠ « Seek a NON-VAMPIRE minion » -> `CardFinder(card_type=Minion,
#    non_trait="VAMPIRE")`. Un Vampire ne peut pas etre etreint.
#  ⚠ « reveal it AND attach » -> `Reveal` (le When Revealed du sbire part, il
#    entre en jeu engage avec le joueur), puis attache SI il est entre en jeu.
#    Rien a etreindre -> Embraced est defausse (le texte ne dit rien d'autre).
#  ⚠ Sous Blood Hunt (bl012), un sbire Embraced cumule DEUX textes de
#    doublement (x4) : lecture litterale, assumee (voir bl012).


def GetAbilities() -> Sequence['Ability']:

    def pv_imprimes_de_l_hote(effect: 'Effect') -> int:
        hote = Hote(getattr(effect, "this", None))
        if hote is None:
            return 0
        return int(getattr(hote, "printed_health", 0) or 0)

    def etreindre(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Attachment)
        joueur = message.GetToPlayer()
        face = Search.EncounterCard(
            effect,
            joueur,
            include_discard_pile=False,
            finder=CardFinder(card_type=Minion, non_trait=TRAIT_VAMPIRE),
        )
        if not face:
            Faces.DiscardAll([this], effect)
            return

        def attacher() -> None:
            this.AttachTo2(face, effect)

        face.Reveal(joueur, effect, if_entered_play=attacher)
        if Hote(this) is None:
            Faces.DiscardAll([this], effect)

    return [
        *AbilityFactory.GiveKeywordToAttached(
            Minion,
            trait=TRAIT_VAMPIRE,
            health=pv_imprimes_de_l_hote,
        ),
        DoubleDegatsPercants("AttachedMinion"),
        AbilityFactory.WhenThisRevealed(
            None,
            etreindre,
        ),
    ]
