from . import *

# * Puddlegulp (face alter-ego) — ASGARD. CREATURE. PV 12, REC 4, main 6.
# Worthy — Action: Find Frogjolnir and add it to your hand.
#   (Limit once per round.)
#
# ⚠ LE ZIP NUMEROTE LES DEUX FACES A L'ENVERS : « 0.1 » est l'ALTER-EGO
# (Puddlegulp), « 0.2 » le HEROS (Throg). Verifie sur les libelles imprimes
# ALTER-EGO / HERO et sur les statistiques (REC 4 d'un cote, ATQ/CTR/DEF de
# l'autre), pas sur le nom de fichier. Meme piege que `br001a/b`.
#
# ⚠ ET CONTRAIREMENT A BETA RAY BILL, les deux faces ont des noms DIFFERENTS.
# L'obligation tg011 dit « Give to the PUDDLEGULP player », donc `desc.GiveTo`
# vaut « Puddlegulp » et non « Throg ».
#
# CARTES DE REFERENCE
#  - `br001b` * Beta Ray Bill (alter-ego) : meme structure « <nom d'aptitude>
#    — Action: Find <carte nommee> and add it to your hand. (Limit once per
#    round.) », meme auteur.
#  - `04001b` Clint Barton : « search your deck and discard pile for Hawkeye's
#    Bow and add it to your hand », le rappel d'arme nommee.
#  - `bk008` Blink's Quiver : ⚠ `Search.PlayerCard` rend UNE FACE OU None
#    (`-> TC|None`, search.py:146), PAS une liste. L'indexer levait
#    « 'Upgrade' object is not subscriptable », que le moteur AVALE.
#
# TEXTE CONTRE CODE
#  « FIND » n'est pas « search your deck » : le mot couvre le deck, la
#    defausse ET LE TERRAIN. Le corps partage (`ResoudreWorthy`, dans le
#    `__init__.py` du set) traite les trois, en commencant par le terrain.
#  ⚠ AUCUN effet secondaire, contrairement au `Worthy` de `br001a` qui frappe
#    pour 3 quand le marteau QUITTE LE JEU. Ici le texte s'arrete a « add it
#    to your hand ». Ne pas recopier la carte de reference sans la relire.
#  « ACTION » et non « Alter-Ego Action » : c'est deja une capacite de la face
#    civile, elle n'a pas besoin du prefixe. `WhenInYourPlayTurn` sur une face
#    `AlterEgo` ne se propose qu'en forme civile.
#  « (Limit once per ROUND.) » -> `.LimitOncePerRound()`. Contrairement a
#    tg001a, ce n'est PAS par phase.


def GetAbilities() -> Sequence['Ability']:

    def digne(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(AlterEgo)
        Unused(this, message)

        ResoudreWorthy(effect, JoueurDeCetteCarte(effect))

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            digne,
        ).LimitOncePerRound()
        .SetName("Worthy"),
    ]
