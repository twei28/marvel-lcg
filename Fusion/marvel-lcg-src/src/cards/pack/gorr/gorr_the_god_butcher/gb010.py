from . import *

# Necro-Raven — SBIRE NECROVERSE (×3 dans le set modulaire).
# MNG 1 / ATQ 0 — 3 PV, 1 icone de boost + une etoile.
#
# Incite 1. Surge.
# Forced Response: After Necro-Raven enters play, discard the top card of your
#   deck. Then, if there are 3 copies of Necro-Raven in play, discard them and
#   summon the Necro-Raven Gestalt minion and put it into play engaged with
#   you.
# [star] Boost: Put Necro-Raven into play engaged with you.
#
# ---------------------------------------------------------------------------
# MOTS-CLES (fiches lues avant d'ecrire)
#
# - `Incite` (mots-cles/incite.md) et `Surge` (mots-cles/surge.md) : BASES
#   AUTOMATIQUES, `desc.Incite = "1"` et `desc.Surge = "1"`. Aucun script.
# - `Boost` etoile (mots-cles/boost.md) : le texte ne suffit pas, il faut la
#   capacite `WhenCardBecomeBoost`, sinon le moteur ne voit aucune etoile.
#
# ---------------------------------------------------------------------------
# CARTES DE REFERENCE
#
# - « [star] Boost: Put X into play engaged with you » : 01121 (Weapons
#   Runner), 02023, 02024 — tous `WhenCardBecomeBoost("This", PutThisIntoPlay)`.
#   Le helper existe deja, il n'y a rien a ecrire.
# - « After X enters play » : `AfterCardEnterPlay`, le declencheur employe par
#   al014 (Lurking) pour un sbire qui arrive.
# - Fusion de trois copies en une carte mise de cote : aucune carte du depot
#   ne le fait. Le montage se ramene a trois briques connues : compter les
#   copies en jeu (`Worlds.FindCardsOnField(name=...)`), les defausser
#   (`Faces.DiscardAll`), puis sortir le Gestalt de la reserve
#   (`SetupCards.PutIntoPlay`, modele 50087a).
#
# ---------------------------------------------------------------------------
# TEXTE CONTRE CODE
#
# « discard the top card of YOUR deck » -> le deck du joueur engage avec ce
#   sbire, pas le premier joueur : `this.GetEngagedPlayer()`.
# « 3 COPIES of Necro-Raven IN PLAY » -> les copies EN JEU, chez tous les
#   joueurs (le texte ne dit pas « engaged with you »), celle-ci comprise.
# « DISCARD THEM » -> les trois copies partent a la defausse de rencontre ;
#   la carte qui declenche se defausse donc elle-meme.
# « SUMMON the Necro-Raven Gestalt » -> il vient de la RESERVE, ou le Setup
#   du complot 1A l'a mis et ou son propre Forced Interrupt le renvoie a
#   chaque fois qu'il est vaincu. Ce n'est pas une copie neuve.
# « engaged with YOU » -> le joueur du sbire declencheur.


def GetAbilities() -> Sequence['Ability']:

    def le_vol_se_rassemble(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        this = effect.this.CastTo(Minion)
        Unused(message)

        joueur = this.GetEngagedPlayer()
        if isinstance(joueur, Player):
            joueur.DiscardDeckTopCards(1, effect)

        copies = Worlds.FindCardsOnField(effect, CardFinder(name="Necro-Raven"))
        if len(copies) >= 3:
            Faces.DiscardAll(copies, effect)
            SetupCards.PutIntoPlay(
                effect,
                for_player=joueur if isinstance(joueur, Player) else "FirstPlayer",
                name="Necro-Raven Gestalt",
                card_type=Minion,
            )

    return [
        AbilityFactory.AfterCardEnterPlay(
            AbilityType.ForcedResponse,
            "This",
            le_vol_se_rassemble,
        ),
        AbilityFactory.WhenCardBecomeBoost(
            "This",
            PutThisIntoPlay,
        ),
    ]
