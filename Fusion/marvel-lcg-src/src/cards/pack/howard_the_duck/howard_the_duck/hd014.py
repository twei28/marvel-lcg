from . import *

# * Ducktective Agency — LOCATION — soutien, cout 2
# Resource: Exhaust Ducktective Agency → generate a [mental] resource for an
#   event.
# Hero Response: After you remove the last threat from a scheme, ready
#   Ducktective Agency.
#
# Capacite Resource FILTREE : modele exact ncrawler/nightcrawler/48005.py
# (Prehensile Tail), `AbilityFactory.CanGenerateResources(AbilityType.Resource,
# Resources(<icone>), for_card=CardFinder(card_type=Event))` +
# `.SetCostFunc(CostFunc.Exhaust("This"))`. Le filtre `for_card` est le seul
# mecanisme du moteur pour « pour un evenement » : une ressource non filtree
# se depenserait sur n'importe quoi. Ressource mentale imprimee -> `"B"`
# (resources.py, R physique / B mental / Y energie / G wild).
#
# PIEGE documente dans test_capacites.py : une capacite Resource ne s'exerce
# QUE par le chemin `jouer_carte` (paiement reel) ; `Puzzle.PutIntoPlay`
# court-circuite tout paiement et ne la declencherait jamais. Piege
# SUPPLEMENTAIRE trouve le 30/08/2026 en ecrivant le cas : le pilote generique
# de `test_capacites` ne compose pas un paiement a plusieurs sources quand la
# carte a financer coute 2 et qu'aucune source ne couvre le montant a elle
# seule (verifie avec un TEMOIN officiel, 40007 Graymalkin, pose a cote de
# l'Agence : lui non plus n'etait pas retenu par le pilote dans ce montage).
# Le cas vise donc un evenement a cout 1 (First Aid, 01086), finance par la
# SEULE Agence — preuve par insuffisance sans ambiguite.
#
# « After you remove the LAST threat from a scheme » = vous VAINQUEZ une
# manigance en retirant sa menace -> `AbilityFactory.AfterUnitDefeatedScheme
# (AbilityType.HeroResponse, "You", None, ...)` (scheme.py:203), la meme
# famille que Cable (40001a, qui l'utilise avec `who_make_thwart="This"`).
# Portee volontairement LARGE sur la manigance (`None`, « a scheme », pas
# seulement les annexes) et RESTREINTE sur l'auteur (`"You"`, « after YOU
# remove »). Redressement : `Faces.ReadyAll([this], effect)` (modele ok014).


def GetAbilities() -> Sequence['Ability']:

    def ducktective_agency(effect: 'Effect', message: 'Message.AfterUnitDefeatedScheme') -> None:
        this = effect.this.CastTo(Support)
        Unused(message)

        Faces.ReadyAll([this], effect)

    return [
        AbilityFactory.CanGenerateResources(
            AbilityType.Resource,
            Resources("B"),
            for_card=CardFinder(card_type=Event),
        ).SetCostFunc(CostFunc.Exhaust("This")),
        AbilityFactory.AfterUnitDefeatedScheme(
            AbilityType.HeroResponse,
            "You",
            None,
            ducktective_agency,
        ),
    ]
