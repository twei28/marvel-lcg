from . import *

# * Stormbreaker — AMELIORATION, cout 1, [wild]. ASGARD. WEAPON. UNIQUE.
# Restricted.
# Your hero gains the [[AERIAL]] trait.
# Hero Resource: Discard Stormbreaker from play -> generate [wild][wild]
#   resources for an event.
#
# ⚠ LA CARTE AUTOUR DE LAQUELLE TOUT LE PACK TOURNE. Sept des treize cartes
# la citent nommement (voir l'en-tete du `__init__.py` du set).
#
# MOT-CLE : RESTRICTED — fiche `docs/reference/mots-cles/restricted.md`. Base
# automatique : la cle `desc.Restricted` vaut `"1"` et le moteur la lit seul
# (modele `06009` Mjolnir, l'equivalent de Thor). AUCUN script.
#
# CARTES DE REFERENCE
#  - `06009` Mjolnir : `GiveKeywordToAttached(CardFinder(name=...), trait=...)`,
#    l'idiome du trait accorde par une amelioration de heros.
#  - `ab007` / `ma005` : `CanGenerateResources` a cout de defausse.
#
# TEXTE CONTRE CODE
#  « YOUR HERO gains the AERIAL trait » -> ⚠ le filtre par NOM ne distingue
#    PAS les deux faces, qui s'appellent toutes deux « Beta Ray Bill ». Mais
#    l'amelioration est ATTACHEE a l'identite, donc `GiveKeywordToAttached`
#    sans filtre vise deja la bonne carte, quelle que soit sa face. C'est plus
#    sur qu'un `CardFinder(name=...)` ici.
#  « DISCARD Stormbreaker FROM PLAY » est le COUT, pas l'effet : la carte se
#    sacrifie. C'est ce qui permet a br001a `Worthy` de la rappeler ensuite
#    depuis la defausse — l'aller-retour est le moteur economique du heros.
#  « for AN EVENT » -> la ressource ne sert qu'a payer un EVENEMENT. Sans ce
#    filtre, le marteau paierait n'importe quoi et le kit perdrait sa tension.
#  ⚠ DEUX ressources [wild] pour un cout de 1 : la carte se rentabilise des
#    qu'elle paie un evenement a 2, et br002 comme br004 lisent ensuite
#    QU'ELLE a paye.


def GetAbilities() -> Sequence['Ability']:

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        *AbilityFactory.GiveKeywordToAttached(
            trait="AERIAL",
        ),
        AbilityFactory.CanGenerateResources(
            AbilityType.HeroResource,
            Resources("GG"),
            # ⚠ LE PARAMETRE S'APPELLE `for_card` ET PREND UN `CardFinder`
            # (resources.py:279), pas `for_card_type=Event` — invente et sorti
            # par `test_cards`. C'est lui qui rend « for an EVENT ».
            CardFinder(card_type=Event),
        ).SetCostFunc(CostFunc.Discard("This")),
    ]
