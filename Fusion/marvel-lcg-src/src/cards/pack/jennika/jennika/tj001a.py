from . import *

# * Jennika (face heros) — NINJA. TURTLE. ATQ 1 / CTR 1 / DEF 2 / PV 12 / main 4.
# Ninja Senpai — Interrupt: When you play a Shinobi card, Jennika gets +1 THW,
#   +1 ATK, and +1 DEF until the end of the round. (Limit once per round for each
#   Shinobi.)
#
# Mot-cle : aucun mot-cle officiel ; « Shinobi » est une notion du pack (classes
# Bushido / Ninjutsu / Kuji-Kiri / Taijutsu, voir l'en-tete du pack).
#
# Cartes de reference :
#  - declencheur « When you play a <filtre> card » : `WhenPlayerPlayCard(
#    Interrupt, "You", CardFinder(...), op)` — modele ho006 (RECETTES §1) ;
#  - +N jusqu'a la fin du round : `ls004` / `tm011` —
#    `face.GainUntilRoundEnd(effect, attack=1, ...)` ;
#  - limite par round : `Ability.LimitOncePerRound()` (once_per.py).
#
# ⚠ Mots-pieges :
#  - « Jennika gets » : un NOM PROPRE ne designe que la face HEROS (l'alter-ego
#    s'appelle Jenny, la capacite n'existe qu'en forme heros) : `this`, pas
#    l'identite ;
#  - « Limit once per round FOR EACH SHINOBI » : lecture retenue = une fois par
#    round POUR CHACUN des quatre Shinobi (Bushido, Ninjutsu, Kuji-Kiri,
#    Taijutsu), d'ou QUATRE capacites identiques, une par classe, chacune avec
#    sa propre limite (DECISION UTILISATEUR (16/10/2026, Q1), .planning/tmnt/jennika-questions.md) ;
#  - « Interrupt » (sans « Hero ») : capacite de la face, optionnelle ;
#  - le bonus part AVANT la resolution de la carte jouee (Interrupt) ;
#  - « a Shinobi card » : une carte portant l'une des quatre classes ; les cartes
#    de Jennika sans classe Shinobi (Composure, Crib, Bow, Tekko-Kagi) ne
#    declenchent rien.


# DECISION UTILISATEUR (16/10/2026, Q1) (.planning/tmnt/jennika-questions.md) : « for each Shinobi » = par classe (lecture
# retenue), par carte, ou une seule fois par round ?
def GetAbilities() -> Sequence['Ability']:

    def ninja_senpai(effect: 'Effect', message: 'Message.WhenPlayerPlayCard') -> None:
        this = effect.this.CastTo(Hero)
        Unused(message)

        this.GainUntilRoundEnd(effect, thwart=1, attack=1, defense=1)

    return [
        AbilityFactory.WhenPlayerPlayCard(
            AbilityType.Interrupt,
            "You",
            CardFinder(card_class=classe),  # type: ignore
            ninja_senpai,
        ).LimitOncePerRound()
        for classe in CLASSES_SHINOBI
    ]
