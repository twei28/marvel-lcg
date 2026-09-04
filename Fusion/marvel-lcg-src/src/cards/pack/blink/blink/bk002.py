from . import *

# * Sabretooth (Victor Creed) — ALLIE, cout 2, PV 3, ATQ 3** / CTR 1*. X-MEN.
# Response: After Sabretooth enters your hand, if there is a [[PORTAL]]
#   upgrade in play, put Sabretooth into play under your control.
#   (Limit once per round.)
#
# CARTE DE REFERENCE
#  - `21032` Pip the Troll : le moteur le cite NOMMEMENT dans son controle de
#    zone (effect_checker.py, « Fix 21032 »). C'est LE precedent d'une
#    capacite DECLENCHEE depuis la main, montee sur `CanWorkOnlyInHand()`.
#
# ⚠ CE CAS-LA FONCTIONNE, contrairement aux bonus CONTINUS depuis la main.
# Leçon du pack doctor_druid : `CanWorkOnlyInHand()` gouverne la RESOLUTION
# d'une capacite, donc il suffit pour un declencheur, mais PAS pour un
# modificateur permanent. Ici c'est bien un declencheur.
#
# TEXTE CONTRE CODE
#  « enters your HAND » -> `AfterCardEnterHand`, pas « after you draw » : une
#    carte rendue en main par bk001a compte aussi.
#  « if there is a PORTAL upgrade IN PLAY » -> condition lue au declenchement.
#  « (Limit once per round.) » -> `.LimitOncePerRound()`.


def GetAbilities() -> Sequence['Ability']:

    def un_portail_en_jeu(effect: 'Effect', message: 'Message2') -> bool:
        return bool(PortailsEnJeu(effect))

    def entrer_en_jeu(effect: 'Effect', message: 'Message.AfterCardEnterHand') -> None:
        this = effect.this.CastTo(Ally)
        Unused(message)
        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return
        this.PutIntoPlay(joueur, effect)

    return [
        AbilityFactory.CanPlayThisAllyCard(),
        AbilityFactory.AfterCardEnterHand(
            AbilityType.Response,
            "This",
            entrer_en_jeu,
            conditions=[un_portail_en_jeu],
        ).CanWorkOnlyInHand()
        .LimitOncePerRound(),
    ]
