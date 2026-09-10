from . import *

# * Molecule Man — SBIRE du set rencontre MOLECULE MAN (1/6). 10 PV, ATQ 4,
# MNG 2, boost 3. ELITE.
# Toughness. Steady.
# [star] Character cannot defend against Molecule Man's attacks.
# When Revealed: Search the encounter deck and discard pile for Master of
#   Molecules and reveal it.
#
# ⚠ 10 PV ET ATQ 4 SUR UN SBIRE, QU'ON NE PEUT PAS BLOQUER. Molecule Man est
# concu pour etre tue vite ou pas du tout. Son attachement `ip036` Master of
# Molecules le rend pire a chaque attaque : le set entier tourne autour de lui.
#
# CARTES DE REFERENCE
#  - `27152` Tracking Display : `*AbilityFactory.UnitCannotDefend(Unit2,
#    <attaquant>, cannot_trigger_defense_ability=True)`.
#  - `04077` * Absorbing Man / `56027` * Madame Masque : `Search.EncounterCard`
#    puis `face.Reveal(...)`.
#
# TEXTE CONTRE CODE
#  ⚠ « CHARACTER cannot defend » : aucun personnage, ni allie ni identite.
#    `Unit2` cote defenseur, `"This"` cote attaquant.
#  ⚠ « Search the encounter deck AND DISCARD PILE » : les deux zones, d'ou
#    `include_discard_pile=True`. C'est plus large que `ip016` Doctor Doom, qui
#    fouille tout par `Find` — ici le texte borne lui-meme la fouille, on s'y
#    tient.
#  ⚠ La carte cherchee peut deja etre en jeu : le texte ne le prevoit pas, et
#    `Search.EncounterCard` ne la trouvera pas la. Rien ne se passe alors, ce
#    qui est le comportement voulu (elle est deja attachee).
#  ⚠ Toughness et Steady sont des BASES NATIVES lues dans `desc`.


def GetAbilities() -> Sequence['Ability']:

    def molecule_man_revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Minion)
        Unused(this)
        joueur = message.GetToPlayer()
        face = Search.EncounterCard(
            effect,
            joueur,
            include_discard_pile=True,
            name="Master of Molecules",
        )
        if face is not None:
            face.Reveal(joueur, effect)

    return [
        *AbilityFactory.UnitCannotDefend(
            Unit2,
            "This",
            cannot_trigger_defense_ability=True,
        ),
        AbilityFactory.WhenThisRevealed(
            None,
            molecule_man_revele,
        ),
    ]
