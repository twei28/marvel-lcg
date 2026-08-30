from . import *

# * Star Flight — AMELIORATION signature, custom « jakxin »
# Cout 2, [energy], trait SUPERPOWER.
#
# Ms. America gets +1 THW and gains the [[AERIAL]] trait.
# Hero Interrupt: When you play an event card, exhaust Star Flight → that
#   event gains the [[SUPERPOWER]] trait.
#
# La seconde capacite est le SEUL moyen, dans tout le catalogue, de faire
# declencher Star-Gaze sur une carte d'ASPECT : le trait SUPERPOWER n'existe
# que sur des cartes de heros (mesure du 30/08/2026, voir le
# ms_america/__init__.py).
#
# ---------------------------------------------------------------------------
# AUCUNE CAPACITE « PLAY » DECLAREE
#
# `Upgrade.GetAbilities` (upgrade.py:12-19) en pose une d'office,
# `CanPlayThisUpgradeCard()`, qui attache la carte a l'identite du joueur. Le
# texte n'imprime aucun « Attach to... » : rien a cibler. Meme montage que
# `wc016` Wiccan's Cloak et `ag008` Agent 13's Pistol.
#
# ---------------------------------------------------------------------------
# CAPACITE 1 — DEUX CHOSES DISTINCTES DANS LA MEME PHRASE
#
# « +1 THW » ET « gains the [[AERIAL]] trait » : un BONUS CONTINU et un TRAIT
# ACCORDE. `GiveKeywordToAttached` (asset.py:6-38) sait faire les deux dans
# le meme appel (`thwart=` et `trait=`), et c'est bien UN SEUL effet continu
# porte par l'amelioration attachee.
#
# Carte de reference : `01065` Heroic Intuition, « Your hero gets +1 THW »,
# ecrite `*AbilityFactory.GiveKeywordToAttached(Hero, thwart=1)`. Pour le
# trait, `dt079` Borrowed Gear emploie le meme `trait=` sur la meme fabrique.
#
# ⚠ `Hero` et non `Identity` : le texte dit « **Ms. America** gets », le nom
# de la FACE HEROS. En identite civile le bonus ne s'applique pas (et de
# toute facon l'alter-ego n'a pas de CTR). La fabrique rend une LISTE :
# deballage `*` obligatoire.
#
# ---------------------------------------------------------------------------
# CAPACITE 2 — LE TRAIT DONNE A L'EVENEMENT
#
# « WHEN you play an event card » -> `WhenPlayerPlayCard` (play.py:225), qui
#   resout AVANT que la carte soit jouee. C'est indispensable : Star-Gaze est
#   un `AfterPlayerPlayedCard`, elle regarde APRES — le trait doit donc etre
#   pose entre les deux.
# « YOU play » -> `"You"`. « an EVENT card » -> `CardFinder(card_type=Event)`.
# « Hero Interrupt » -> `AbilityType.HeroInterrupt` (sous-type dedie).
#   ⚠ AUCUN `.SetLabel(...)` ici : `Ability.Initialize` (ability.py:196)
#   n'autorise que 'defense' et 'thwart' sur une interruption, et la carte
#   n'imprime aucun libelle. Piege paye sur `pt015`.
# « that event GAINS the [[SUPERPOWER]] trait » -> `GainUntilPhaseEnd(effect,
#   trait=...)` sur la face jouee (face_action.py:440-464), idiome de `01039`
#   Pym Particles et `30011`. La portee n'est pas imprimee sur la carte : le
#   trait sert a Star-Gaze, qui resout dans la meme fenetre, et il disparait
#   a la fin de la phase. `GainUntilRoundEnd` aurait laisse le trait sur la
#   carte defaussee jusqu'a la fin du round — plus permissif, donc ecarte.
#
# LA FLECHE EST UN COUT : `CostFunc.Exhaust("This")`. Star Flight inclinee,
# l'interruption n'est plus proposee (cost_func.py:49).


BONUS_THW = 1


def GetAbilities() -> Sequence['Ability']:

    def star_flight(effect: 'Effect', message: 'Message.WhenPlayerPlayCard') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)

        face = message.played_face
        if face is None:
            return
        face.GainUntilPhaseEnd(effect, trait=TRAIT_SUPERPOWER)

    return [
        *AbilityFactory.GiveKeywordToAttached(
            Hero,
            thwart=BONUS_THW,
            trait=TRAIT_AERIAL,
        ),
        AbilityFactory.WhenPlayerPlayCard(
            AbilityType.HeroInterrupt,
            "You",
            CardFinder(card_type=Event),
            star_flight,
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
