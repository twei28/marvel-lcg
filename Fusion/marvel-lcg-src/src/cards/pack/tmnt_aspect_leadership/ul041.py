from . import *

# * Mushroom — ALLIE Leadership a DOS DE RENCONTRE (TMNT Aspects, Inkwire), sans cout, [physical].
# NINJA. WEASEL. THW 1* / ATQ 1* / PV 2.
# Linked (Weasel In).
# Musroom [sic] does not count against your ally limit.
# When Revealed: Heal 2 damage from a friendly character and put Mushroom into play under your control.
#   This card gains surge. This effect cannot be canceled.
#
# MOTS-CLES : Linked (linked.md, `desc.Linked = "ul040"`), Surge (surge.md, `ThisCardGainSurge`).
# Montage commun aux trois belettes : `AbilitiesBelette` (__init__ du pack ; modele `39071` Longshot).
#
# TEXTE CONTRE CODE
#  ⚠ « a FRIENDLY character » : identite ou allie de N'IMPORTE quel joueur, choisi par le joueur qui revele.
#  ⚠ « Heal 2 » AVANT la mise en jeu (ordre imprime) : Mushroom ne peut pas se soigner lui-meme.
#  ⚠ « under YOUR control » : le joueur qui revele la carte. « Musroom » : coquille sans effet de regle.


def GetAbilities() -> Sequence['Ability']:

    def soigner(effect: 'Effect', joueur: 'Player') -> None:
        this = effect.this.CastTo(Ally)
        amis = [f for f in Worlds.GetOnFieldFriendlyCharacters(effect) if f is not None]
        if not amis:
            return
        cible = joueur.AskChooseFace(amis, effect, prompt="Heal 2 damage from a friendly character")
        if cible is not None:
            this.HealthUnits([cible], 2, effect)

    return AbilitiesBelette(soigner)
