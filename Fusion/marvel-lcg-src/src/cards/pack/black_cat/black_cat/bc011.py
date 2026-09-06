from . import *

# Nine Lives — AMELIORATION, cout 2, [energy]. CONDITION. SUPERPOWER. x2.
# Hero Interrupt: When Black Cat would take any amount of damage, exhaust Nine
#   Lives and discard the top card of the encounter deck -> prevent 1 of that
#   damage for each icon ([star] and [boost]) in that card's boost area.
#
# ⚠ NEUF PV SEULEMENT. Black Cat est la plus fragile du set : cette carte est
# sa seule prevention, et elle est ALEATOIRE — une carte sans icone ne prevent
# rien, et l'inclinaison est perdue. C'est le pari imprime.
#
# CARTES DE REFERENCE
#  - `Message.WhenUnitWouldTakeDamage.PreventDamage` (sender_damage.py:133) :
#    la primitive de prevention chiffree.
#  - `ho009` : `CostFunc.Custom(None, fn)`.
#  - `bc008` : le meme cout « defausser le dessus du deck » et la meme
#    condition d'offre.
#
# TEXTE CONTRE CODE
#  ⚠ « When BLACK CAT would take damage » -> l'IDENTITE en forme heros, pas un
#    allie, pas Felicia Hardy. Le filtre est `"YourHero"` : le nom serait faux,
#    trois cartes du depot s'appellent « * Black Cat ». Et « Hero Interrupt »
#    confirme la forme.
#  ⚠ « ANY amount of damage » -> toute source : attaque, degat indirect,
#    consecutif, carte de rencontre. Aucun filtre `is_from_attack`.
#  ⚠ DEUX COUTS devant la fleche : incliner ET defausser le dessus du deck de
#    rencontre. Deck vide, la capacite n'est pas offerte (`CostFunc.Custom` ne
#    sait pas se rendre indisponible seul, RECETTES §5) — sinon l'amelioration
#    s'inclinerait sans rien prevenir.
#  ⚠ « each icon ([star] AND [boost]) » -> `IconesEtEtoiles`.
#  ⚠ ON COMPTE APRES LA DEFAUSSE, faute de choix : `DiscardEncounterTopCard`
#    defausse et rend la carte d'un seul geste. Comme pour `bc006`, cela passe
#    par `WhenBoostIconsWouldBeCount` et ouvre donc la porte a `bc001a`
#    Tychokinesis. Combinaison voulue, pas defaut.


def GetAbilities() -> Sequence['Ability']:

    def cout_defausser_le_dessus(cibles: Sequence['CardFace'], effect: 'Effect') -> bool:
        Unused(cibles)
        face = Worlds.DiscardEncounterTopCard(effect)
        if face is None:
            return False
        setattr(effect, "_bc011_carte_defaussee", face)
        return True

    def deck_de_rencontre_non_vide(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> bool:
        Unused(message)
        return Worlds.GetEncounterDeckCards(effect) != []

    def neuf_vies(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)

        defaussee = getattr(effect, "_bc011_carte_defaussee", None)
        prevenus = IconesEtEtoiles([defaussee]) if defaussee is not None else 0
        if prevenus > 0:
            message.PreventDamage(prevenus, effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.WhenUnitWouldTakeDamage(
            AbilityType.HeroInterrupt,
            "YourHero",
            neuf_vies,
            conditions=[deck_de_rencontre_non_vide],
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetCostFunc(CostFunc.Custom(None, cout_defausser_le_dessus)),
    ]
