from . import *

# * Shiro Yoshida (face alter-ego) — MUTANT. PV 11, REC 4, main 6.
# Shiro Yoshida begins the game with 6 Burning upgrades set aside.
# Hot-Headed — Action: Discard the top 5 cards of your deck. Choose one card
#   discarded this way and add it to your hand. (Limit once per round.)
#
# CARTES DE REFERENCE
#  - `09001b` Stephen Strange / `bt001b` / `al001b` :
#    `AbilityFactory.BeginGameWithSetAside([...])`, qui FABRIQUE les cartes
#    dans `initiator.additional_discard_pile` (setup.py:68) — la reserve, que
#    le harnais appelle `set_aside_deck`.
#  - `aa001a` * Agatha Harkness : `player.DiscardDeckTopCards(n, effect)`
#    REND la liste des cartes defaussees, seule facon de rendre « one card
#    discarded THIS WAY ».
#
# TEXTE CONTRE CODE
#  ⚠ « begins the game with 6 Burning upgrades SET ASIDE » -> ce n'est PAS le
#    champ `set_aside` du deck de depart, que le moteur NE LIT PAS en vraie
#    partie (§3 de PROCESSUS-HEROS). Les six exemplaires doivent etre crees
#    par l'identite elle-meme, et c'est ce que fait cette fabrique.
#  ⚠ PAS DE FLECHE dans Hot-Headed : defausser cinq cartes n'est pas un cout,
#    c'est la premiere moitie de l'effet. Deck de moins de 5 cartes, l'Action
#    reste jouable et defausse ce qu'elle peut.
#  « CHOOSE ONE CARD DISCARDED THIS WAY » -> parmi les cinq, pas dans toute la
#    defausse. On garde la liste rendue par la defausse, on ne repeche pas.
#  « (Limit once per ROUND.) » -> `.LimitOncePerRound()`.


def GetAbilities() -> Sequence['Ability']:

    def tete_brulee(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(AlterEgo)
        Unused(this, message)

        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return

        # ⚠ `Player.DiscardDeckTopCards` REND la liste des cartes defaussees
        # (modele `aa001a`, pack agatha_harkness) : c'est elle, et elle seule,
        # que « one card discarded this way » designe.
        dessus = list(joueur.DiscardDeckTopCards(5, effect) or [])
        if not dessus:
            return

        # « Choose ONE CARD DISCARDED THIS WAY » : parmi ces cinq-la.
        choisie = joueur.AskChooseFaces(
            dessus, (1, 1), effect,
            prompt="Add one of the discarded cards to your hand")
        if choisie:
            Faces.AddToHand(list(choisie), joueur, effect)

    return [
        AbilityFactory.BeginGameWithSetAside(["sf009"] * BRULURES_MISES_DE_COTE),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            tete_brulee,
        ).LimitOncePerRound()
        .SetName("Hot-Headed"),
    ]
