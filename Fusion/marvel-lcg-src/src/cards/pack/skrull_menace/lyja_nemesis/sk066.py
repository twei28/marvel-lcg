from . import *

# * Paibok — SBIRE NEMESIS de Lyja (n° 66, 1/5). ELITE. SKRULL. SCH 2★, ATK 2★, 4 PV, 2 icones boost.
# Toughness.
# ★ Paibok gets +1 SCH and +1 ATK for each TREACHERY card attached to him.
# Forced Interrupt: When a TREACHERY card would be discarded, attach it facedown to Paibok
#   instead.
# (Lyja's nemesis minion.)
#
# Cartes de reference :
#  - **`sn001a`** Spider-Man Noir : « +X ATK and THW where X = cartes glissees sous lui » =
#    `ThisGainKeyword(<compte de GetPlacedCardArea()>, attack=1, thwart=1,
#    change_on_event=OnEvent.PlacedCard("Here"))`. « Attached facedown » est la meme chose
#    que « tucked » : `PlaceCardHere(carte, False, effect)` (pile `GetPlacedCardArea`).
#  - **`43031`** Cybermods / **`27087b`** : `WhenCardWouldDiscard(ForcedInterrupt, ...)` +
#    `message.SetBeInstead(effect)` : la defausse n'a pas lieu, la carte part ailleurs.
#  - **fiche `toughness.md`** : Toughness lu dans `desc`, aucun script.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « WOULD be discarded ... attach it facedown INSTEAD » : la carte ne va PAS en defausse
#    (Interruption, `SetBeInstead`) ; elle quitte sa zone pour la pile de Paibok.
#  - « a TREACHERY card » : type Treachery OU trait TREACHERY (decision du 15/10/2026) ;
#    n'importe quelle traitrise, d'ou qu'elle soit defaussee (lecture LITTERALE, voir
#    defs/lyja_questions.md).
#  - « for EACH TREACHERY card attached » : seules les traitrises de la pile comptent.
#  - ★ sans « expert » : toujours actif (convention du moteur, RECETTES §3).
#  - ATK « 2★ » : desc « 2* », SCH « 2 » (un « * » sur SCH multiplierait par le nombre de joueurs).


def GetAbilities() -> Sequence['Ability']:

    def nb_traitrises_attachees(effect: 'Effect', ui: List['CardFace']) -> int:
        pile = [f for f in effect.this.GetPlacedCardArea().Get(True) if EstTraitrise(f)]
        ui.extend(pile)
        return len(pile)

    def attacher_a_la_place(effect: 'Effect', message: 'Message.WhenCardWouldDiscard') -> None:
        this = effect.this.CastTo(Minion)
        message.SetBeInstead(effect)
        this.PlaceCardHere(message.trigger, False, effect)

    return [
        AbilityFactory.ThisGainKeyword(
            nb_traitrises_attachees,
            scheme=1,
            attack=1,
            change_on_event=OnEvent.PlacedCard("Here"),
        ),
        AbilityFactory.WhenCardWouldDiscard(
            AbilityType.ForcedInterrupt,
            FinderTraitrise(),
            attacher_a_la_place,
        ),
    ]
