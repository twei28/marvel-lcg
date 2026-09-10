from . import *

# * Madame Masque — SBIRE du deck REGISTERED (13/20). 4 PV, ATQ 2, MNG 2,
# boost 3. CRIMINAL. ELITE.
# Guard. Steady.
# [star] Forced Response: After Madame Masque attacks and damages a character,
#   confuse that character.
# False Faces — Special: Draw X cards (to a maximum of 3), where X is equal to
#   the main scheme's stage number. If the main scheme has no stage number,
#   draw 1 card.
#
# CARTES DE REFERENCE
#  - `01118` * Sonic Converter (attachement de Klaw) : « After Klaw attacks and
#    damages a character, stun that character ». MEME FENETRE, MEME GESTE, au
#    statut pres — d'ou la meme fabrique, `AfterUnitAttackAndDamageUnit` avec
#    `target_in_play=True`, et la meme lecture de la cible,
#    `message.attacked`.
#  - `02029` Death from Above : `villain.printed_stage` pour lire le numero
#    d'etape de la manigance principale.
#
# TEXTE CONTRE CODE
#  ⚠ « attacks AND DAMAGES » : l'attaque doit avoir inflige des degats. Une
#    attaque entierement bloquee ne confond personne.
#  ⚠ « confuse THAT CHARACTER » : celui qui a pris les degats, pas le
#    defenseur ni le joueur.
#  ⚠⚠ « the MAIN SCHEME'S stage number » : le numero d'etape de la manigance
#    principale, pas celui du vilain. Une manigance principale sans numero
#    d'etape rend 0 (`printed_stage`, has_stage.py:7), et le texte prevoit
#    explicitement ce cas : on pioche alors 1.
#  ⚠ « to a MAXIMUM of 3 » : plafond dur, meme a l'etape 4 ou plus.
#  ⚠ Guard et Steady sont des BASES NATIVES de sbire.


def GetAbilities() -> Sequence['Ability']:

    def confondre(effect: 'Effect', message: 'Message.AfterUnitAttackUnit') -> None:
        if message.attacked is not None:
            Faces.GiveStatus([message.attacked], "Confused", effect)

    def faux_visages(effect: 'Effect', message: 'Message.WhenResolveSpecialAbility') -> None:
        Unused(message)
        joueur = effect.GetInitiator()
        if joueur is None:
            return
        principale = Worlds.FindMainScheme(effect)
        etape = principale.printed_stage if principale is not None else 0
        nombre = min(3, etape) if etape > 0 else 1
        joueur.DrawUp(nombre, effect)

    return [
        AbilityFactory.AfterUnitAttackAndDamageUnit(
            AbilityType.ForcedResponse,
            "This",
            "Character",
            confondre,
            target_in_play=True,
        ),
        SpecialRegistered("False Faces", faux_visages),
    ]
