from . import *

# * Frogjolnir — AMELIORATION, cout 1, [energy]. ASGARD. WEAPON. UNIQUE.
# Restricted.
# Throg gains the [[AERIAL]] trait.
# Hero Interrupt: When Throg uses a basic power, exhaust Frogjolnir -> Throg
#   gets +1 to that power for this use.
#
# ⚠ LA CARTE AUTOUR DE LAQUELLE TOUT LE PACK TOURNE. Cinq des onze cartes du
# set heros la citent nommement (voir l'en-tete du `__init__.py` du set).
#
# MOT-CLE : RESTRICTED — fiche `docs/reference/mots-cles/restricted.md`. Base
# automatique : la cle `desc.Restricted` vaut `"1"` et le moteur la lit seul
# (modele `06009` Mjolnir, l'equivalent de Thor). AUCUN SCRIPT.
#
# CARTES DE REFERENCE
#  - `20010` Venom's Pistol : « Restricted. Hero Interrupt: When you use one of
#    Venom's basic powers, exhaust Venom's Pistol -> Venom gets +1 to that
#    power for this use. » MOT POUR MOT la meme carte, a l'arme pres.
#    Montage : `WhenUnitUseBasicPower(HeroInterrupt, CardFinder(name=...), op)`
#    + `CostFunc.Exhaust("This")` + `message.GainValue(+1, effect)`.
#  - `al012` Gator Aid : la meme mecanique ecrite a la main (trois fabriques),
#    et l'endroit ou le depot a note que `GainValue` couvre les trois pouvoirs
#    d'un coup (`sender_unit.py:21`, qui redirige vers `GainATKForThisAttack`,
#    `GainDEFForThisAttack` ou `GainTHWForThisThwart` selon le pouvoir).
#  - `06009` Mjolnir / `03009` * Captain America's Shield : le trait accorde
#    par une amelioration, `GiveKeywordToAttached(CardFinder(name=...), ...)`.
#
# TEXTE CONTRE CODE
#  ⚠ « THROG gains the AERIAL trait » -> UN NOM PROPRE, donc UNE SEULE FACE.
#    C'est la difference avec `br010` Stormbreaker, dont les deux faces
#    s'appellent pareil et qui pouvait donc se passer de filtre. Ici
#    l'alter-ego s'appelle PUDDLEGULP : un `GiveKeywordToAttached` sans filtre
#    donnerait AERIAL a la grenouille en civil, ce que la carte ne dit pas.
#    Piege `an002` Sera / `06007` Asgard, RECETTES-MOTEUR §3 : « LIRE LE MOT,
#    pas le modele ». Corollaire applique : un CONTRE-CAS en forme alter-ego
#    est ecrit pour prouver que le trait n'y est pas.
#  ⚠ Meme lecture pour l'Interruption : « When THROG uses a basic power »,
#    donc la face heros seule. La RECUPERATION de Puddlegulp n'est pas
#    couverte — et « HERO Interrupt » le confirme.
#  « uses a BASIC POWER » -> les trois, sans filtre `powers=` : `GainValue`
#    route lui-meme vers le bon pouvoir selon `message.would_message`.
#  « +1 to THAT power FOR THIS USE » -> pour cet usage seulement, pas pour le
#    round. C'est `GainValue`, pas un `GainUntilRoundEnd` (piege `tt001a`,
#    qui lui dit bien « until the end of the round »).
#  « exhaust Frogjolnir » est devant la fleche : un COUT. Une fois inclinee,
#    la carte ne se propose plus — et tg001a comme tg002 existent precisement
#    pour la renvoyer en main ou la redresser.


def GetAbilities() -> Sequence['Ability']:

    def frogjolnir(effect: 'Effect', message: 'Message.WhenUnitUseBasicPower') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)

        message.GainValue(+1, effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        *AbilityFactory.GiveKeywordToAttached(
            CardFinder(name=NOM_HEROS),
            trait="AERIAL",
        ),
        AbilityFactory.WhenUnitUseBasicPower(
            AbilityType.HeroInterrupt,
            CardFinder(name=NOM_HEROS),
            frogjolnir,
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetTarget("YourIdentity"),
    ]
