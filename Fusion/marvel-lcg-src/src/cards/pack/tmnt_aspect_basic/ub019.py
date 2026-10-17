from . import *

# Honorable Blades — EVENEMENT Basic (TMNT Aspects, Inkwire), cout 2, [energy]. Aucun trait imprime.
# Team-Up (Leonardo and Usagi Yōjimbō). Max 1 per deck.
# Hero Action: Ready Leonardo and Usagi Yōjimbō. Cloak Leonardo. Place a tough status card on Usagi
#   Yōjimbō.
#
# NOUVELLE. Usagi Yōjimbō = l'allie `up041` (Protection, unique, RABBIT RONIN) : le scan imprime
# « Yōjimō » a la derniere ligne (coquille) ; le nom EXACT est celui de up041.
#
# MOT-CLE Team-Up : fiche mots-cles/teamup.md. `desc.TeamUp = "Leonardo;Usagi Yōjimbō"` + `.SetTarget("TeamUp")`
# (obligatoire) : la carte n'est jouable que si les DEUX personnages (identite OU allie) sont en jeu ;
# `effect.targets` = les deux personnages (ordre non garanti : on les distingue par leur nom).
#
# CARTES DE REFERENCE
#  - `34035` Soul Sisters (Phoenix) : « Ready A and B » = `Faces.ReadyAll(effect.targets, effect)`, meme
#    declencheur Hero Action + TeamUp.
#  - `uj021` Mondo Gecko : « cloak X » = `Faces.GiveStatus([face], "Cloaked", effect)` ; une seule Cloaked
#    par personnage (deja camoufle : rien ne se pose).
#  - `up016` Herman : « place a tough status card » = `Faces.GiveStatus([face], "Tough", effect)`.
#
# TEXTE CONTRE CODE : « Ready Leonardo AND Usagi » (les deux) ; « Cloak LEONARDO » seulement ; « tough
# on USAGI » seulement ; « Max 1 per deck » = `desc.MaxPerDeck` (lu par le moteur). Aucune limite par tour.


def GetAbilities() -> Sequence['Ability']:

    def honorable_blades(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)

        personnages = list(effect.targets)
        Faces.ReadyAll(personnages, effect)
        for perso in personnages:
            if perso.IsName("Usagi Yōjimbō"):
                Faces.GiveStatus([perso], "Tough", effect)
            else:
                Faces.GiveStatus([perso], "Cloaked", effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            honorable_blades
        ).SetPlay().SetLabel()
        .SetTarget("TeamUp"),
    ]
