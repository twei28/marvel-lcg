from . import *

# * Raphael « Raph » — ALLIE 3 [physical], 1*/2*, 3 PV, aspect Basic (TMNT Aspects). NINJA. TURTLE. VIGILANTE.
# [star] Raphael gets +1 ATK for each damage token here (to a maximum of +2 ATK).
#
# NOUVELLE. Carte de reference : 10013 She-Hulk (allie) « [star] She-Hulk gets +1 ATK for each damage token
# here » = `ThisGainKeyword(lambda: this.sustained, attack=1, change_on_event=OnEvent.Health("This"))`.
# Difference : plafond imprime « to a maximum of +2 ATK » -> `min(degats, 2)`.
# [star] = icone etoile (fiche special.md), zero code ; le « 2★ » de l'ATK sur le scan est la meme etoile.
# TEXTE CONTRE CODE : « damage token HERE » (sur Raphael) ; « maximum of +2 » (3 degats -> +2, pas +3).


def GetAbilities() -> Sequence['Ability']:

    return [
        AbilityFactory.ThisGainKeyword(
            lambda effect, ui:
                min(effect.this.CastTo(Ally).sustained, 2),
            attack=1,
            change_on_event=OnEvent.Health("This")
        )
    ]
