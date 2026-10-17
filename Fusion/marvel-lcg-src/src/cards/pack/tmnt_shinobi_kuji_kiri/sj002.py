from . import *

# Imbued Weapons (sj002), Kuji-Kiri, amelioration SPELL (Inkwire, TMNT Shinobi).
# Attach to an ally. Max 1 per ally.
# Attached ally gets +1 THW and +1 ATK.
#
# Texte imprime IDENTIQUE a `core/01074` Inspired (Leadership, CONDITION) : seuls le nom, la classe et le
# trait changent, donc carte exclusive (pas un art alternatif). Meme script que 01074.
# « Max 1 per ally » = `desc.MaxPerUnit "1"` (base automatique lue par le moteur, aucun code).
#
# TEXTE CONTRE CODE : « an ally » (n'importe quel allie en jeu, pas seulement le sien) ; +1 THW ET +1 ATK.


def GetAbilities() -> Sequence['Ability']:

    return [
        AbilityFactory.CanPlayThisUpgradeCard(Ally),
        *AbilityFactory.GiveKeywordToAttached(
            Ally,
            thwart=1,
            attack=1,
        ),
    ]
