from cards.pack import *

# ===========================================================================
# Set nemesis « Venus Nemesis » (Jasper Barlow, Groundchuck-Dirtbag, Inkwire, prefixe `tv`).
#
# ⚠ L'OBLIGATION `tv015` Faulty Creation N'EST PAS ICI : son bandeau imprime dit « VENUS »,
# pas « VENUS NEMESIS ». Son `set_name` est celui du set HEROS, son module vit donc dans
# `venus/venus/` (piege bt019 / sf010).
#
# ⚠ Le « [star] Boost : Deal this card to the first player as a facedown encounter card »
# est commun a `tv017` (Jasper Barlow) et `tv018` (Groundchuck-Dirtbag) : une seule fabrique
# ici, calquee sur `tl015` Karai (pack leonardo).
# ===========================================================================

NOM_JASPER = "Jasper Barlow"


def BoostDonnerAuPremierJoueur() -> 'Ability':
    """« [star] Boost: Deal this card to the first player as a facedown encounter card. »

    Modele `tl015` Karai : la carte retournee comme boost ne va pas a la defausse, elle est
    redirigee vers `dealt_encounter_cards` du PREMIER joueur (`WhenCardWouldDiscard` temporaire,
    jusqu'a la fin du round). L'etoile est une capacite de type `Boost` (fiche `mots-cles/boost.md`).
    """
    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        this = effect.this.CastTo(Minion)
        Unused(message)

        premier = Worlds.GetFirstPlayer(effect)
        if premier is None:
            return

        def rediriger(effet_temp: 'Effect', message2: 'Message.WhenCardWouldDiscard') -> None:
            message2.SetToArea(premier.dealt_encounter_cards)

        this.effect.RegisterTemp(
            AbilityFactory.WhenCardWouldDiscard(
                AbilityType.Temp0,
                "This",
                rediriger,
            ),
            unregister_after_exec=False,
            until_round_end=True,
        )

    return AbilityFactory.WhenCardBecomeBoost("This", boost)
