from . import *

# * Paibok — ALLIE de campagne (Basic / Campaign, n° 265). Cout 3. THW 2** / ATK 2**, 4 PV.
# S.W.O.R.D. SKRULL. Toughness.
# Toughness.
# [star] Paibok gets +1 THW and +1 ATK for each treachery card attached to him.
# Response: After a treachery card is discarded, take 1 damage -> attach it facedown here
#   (to a maximum of 2).
#
# Cartes de reference :
#  - **`sk066`** * Paibok (sbire nemesis de Lyja, MEME mecanique cote ennemi) : « +1 .. for each TREACHERY card
#    attached » = `ThisGainKeyword(nb, ..., change_on_event=OnEvent.PlacedCard("Here"))` sur la pile
#    `GetPlacedCardArea()` ; « attach facedown » = `PlaceCardHere(carte, False, effect)` (carte glissee).
#  - **`bk007`** Crystal Palace : « Response: After a X card is discarded, ... -> attach it facedown here » =
#    `AfterCardDiscard(Response, finder, op, conditions=[...])` + rangement dans la zone des cartes POSEES.
#  - **`sw014`** (spider_woman_kajislav) : « take 1 damage -> » d'un allie en COUT = `CostFunc.TakeDamage(1, "This")`.
#  - **fiche `toughness.md`** : Toughness lu dans `desc`, aucun script.
#
# ⚠ Mots-pieges :
#  - « a TREACHERY card » = type Treachery OU trait TREACHERY (decision utilisateur du 15/10/2026 sur sk066,
#    reprise ici), de n'importe quelle defausse (celle de Lyja comprise) ;
#  - « AFTER ... is discarded » : la carte est DEJA en defausse, elle en sort pour se glisser sous Paibok
#    (pas un remplacement : voir sk066, qui est une Interruption forcee) ;
#  - « take 1 damage -> » est un COUT : sans la PV disponible la Reponse n'est pas offerte ;
#  - « to a MAXIMUM of 2 » : la capacite n'est offerte que tant que la pile compte moins de 2 cartes ;
#  - « for EACH treachery card attached » : seules les traitrises de la pile comptent ;
#  - ★ sans « expert » : toujours actif ; le badge etoile a cote de THW / ATK n'a pas de valeur chiffree.


def GetAbilities() -> Sequence['Ability']:

    def nb_traitrises_attachees(effect: 'Effect', ui: List['CardFace']) -> int:
        pile = [f for f in effect.this.GetPlacedCardArea().Get(True) if EstTraitrise(f)]
        ui.extend(pile)
        return len(pile)

    def pile_pas_pleine(effect: 'Effect', message: 'Message.AfterCardDiscard') -> bool:
        return len(effect.this.GetPlacedCardArea().Get(True)) < 2

    def attacher_face_cachee(effect: 'Effect', message: 'Message.AfterCardDiscard') -> None:
        this = effect.this.CastTo(Ally)
        this.PlaceCardHere(message.trigger, False, effect)

    return [
        AbilityFactory.ThisGainKeyword(
            nb_traitrises_attachees,
            thwart=1,
            attack=1,
            change_on_event=OnEvent.PlacedCard("Here"),
        ),
        AbilityFactory.AfterCardDiscard(
            AbilityType.Response,
            FinderTraitrise(),
            attacher_face_cachee,
            conditions=[pile_pas_pleine],
        ).SetCostFunc(CostFunc.TakeDamage(1, "This")),
    ]
