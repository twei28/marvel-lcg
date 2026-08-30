from . import *

# * Mr. Hyde — SBIRE nemesis, custom « CptScorp »
# PV 5, ATQ 2, MNG 2, 3 icones de bonus, `Toughness "1"`,
# `Nemesis "Elijah Bradley"`, trait ELITE.
#
# Toughness.
# When Revealed: Search encounter deck, encounter discard pile and set aside
#   cards for the MGH Drug attachment and attach it to Mr. Hyde.
#
# ---------------------------------------------------------------------------
# ⚠ `Toughness` ET `Nemesis` SONT LUS NATIVEMENT DANS `desc`
#
# `Toughness` : le sbire entre en jeu avec un jeton Robuste. C'est une base
# automatique du moteur (PROCESSUS-CARTE §5, « bases automatiques a ne pas
# recoder ») — coder une capacite fantome serait une faute. Fiche :
# docs/reference/mots-cles/toughness.md.
# `Nemesis "Elijah Bradley"` designe le heros dont ce sbire est le nemesis :
# lu par le moteur pour composer le set nemesis, aucun module.
#
# Le trait ELITE n'est pas decoratif : il met le sbire hors de portee des
# effets `CardFinder(non_trait="ELITE")` (Vivian `29024`, entre autres).
#
# ---------------------------------------------------------------------------
# LE WHEN REVEALED : **TROIS** ZONES
#
# « Search encounter deck, encounter discard pile AND SET ASIDE CARDS » : les
# trois, pas deux (mot-piege « and remove » du PROCESSUS-CARTE §5, celui du
# cout a plusieurs parties, applique ici a une recherche). Rendu par
# `Search.EncounterCard(..., include_discard_pile=True,
# include_set_aside=True)` (operate/search.py:47-77).
#
# ⚠ pt018 Mr. Hyde's Lab, elle, ne cite QUE deux zones. Ne pas recopier une
# carte sur l'autre.
#
# Modeles exacts du couple recherche + attache : `21177` Seduced (pack mts,
# Enchantress) et `57001` (pack synthezoid, She-Hulk), tous deux en
# `Search.EncounterCard(..., include_discard_pile=..., include_set_aside=True,
# name=..., card_type=Attachment)` puis `face.AttachTo2(cible, effect)`.
#
# « attach it to Mr. Hyde » : a CE sbire (`effect.this`), pas au premier
# « Mr. Hyde » trouve sur le terrain — la carte parle d'elle-meme.
# `AttachTo2` (attribute/can_attach.py:49) refuse si la cible n'est pas sur
# le terrain, ce qui est deja garanti ici : le sbire vient d'etre revele.
#
# Le nom cherche est ecrit SANS l'etoile d'unicite (`NOM_MGH_DRUG`).
#
# Si `pt020` est deja en jeu (attachee au vilain, par exemple), la recherche
# ne la trouve pas — elle n'est ni dans le deck, ni dans la defausse, ni mise
# de cote — et rien ne se passe. C'est la lettre de la carte.


def GetAbilities() -> Sequence['Ability']:

    def mr_hyde_revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Minion)

        joueur = message.GetToPlayer()

        face = Search.EncounterCard(
            effect,
            joueur,
            include_discard_pile=True,
            include_set_aside=True,
            name=NOM_MGH_DRUG,
            card_type=Attachment,
        )
        if face:
            face.CastTo(Attachment).AttachTo2(this, effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            mr_hyde_revele,
        ),
    ]
