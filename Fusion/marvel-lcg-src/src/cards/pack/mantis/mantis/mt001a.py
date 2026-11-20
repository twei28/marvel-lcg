from . import *

# * Mantis (face heros) : GUARDIAN. PSIONIC. THW 2 / ATQ 2 / DEF 2, main 5, PV 9.
# Empathetic Advantage — Resource: Discard a confused status card from an enemy or character you control → generate a [mental] resource. (Generate [wild][mental] resources instead if you
# discarded a confused status card from an enemy. Limit once per round.)
#
# CARTES DE REFERENCE
#  - `hc001a` Hellcat « Empowered » : `CanGenerateResources(AbilityType.Resource, Resources("B"), conditions=[dispo]).SetCostFunc(CostFunc.Custom(None, fn))` ; `conditions` OBLIGATOIRE sinon la ressource est
#    offerte meme impayable et le moteur annule toute la carte (RECETTES §ressources a cout Custom). `AskChooseFaces` dans le cout pour que le joueur CHOISISSE la carte.
#  - `sq001a` Spider-Punisher : `world.stat.AddRoundCounter / GetRoundCounter` (compteur par joueur remis a zero en fin de round).
#
# TEXTE CONTRE CODE
#  « a confused status card FROM an enemy OR character you control » : deux origines, donc DEUX moyens de paiement sur l'identite (le moteur fige le montant a l'annonce, avant le choix de la carte, et une
#    identite ne porte qu'UNE `CanGenerateResources`, `identity.py:19`) : « Empathetic Advantage » (origine ENNEMI, [wild][mental], `CanGenerateResources`) et « Empathetic Advantage (character) » (origine personnage
#    ami, [mental], `CheckThisCanPayCost` ecrit a la main avec son propre `DoGenerateResources` et un `bind_ability` par nom). Le joueur choisit l'origine en choisissant le moyen : aucun ecart de regle
#    (decision de l'utilisateur du 01/11/2026 : « pas d'ecart »). Chaque moyen n'est offert que s'il a une carte a defausser.
#  « Limit once per round » : UN seul emploi par round (compteur de round du joueur, `world.stat.AddRoundCounter`, car `LimitOncePerRound` compte par capacite et n'est pas relancable par The Celestial Madonna).
#  « discard » = la carte Desoriente est retiree du personnage choisi par le joueur ; l'emploi n'a lieu que si elle a REELLEMENT ete retiree.
#  Chiffres : THW 2, ATQ 2, DEF 2, main 5, PV 9 ; 1 ressource mentale, ou 2 (sauvage + mentale) depuis un ennemi.
#  The Celestial Madonna (mt010) peut annuler le decompte d'un emploi (voir ce fichier).


def GetAbilities() -> Sequence['Ability']:

    # DEUX moyens de paiement, un par origine (le moteur fige le montant a l'annonce, avant le choix de la carte : le joueur choisit donc l'ORIGINE en choisissant le moyen).
    # Le premier est la `CanGenerateResources` unique de l'identite ; le second est un `CheckPay` ecrit a la main (`bind_ability` sur SON `DoGenerateResources`).
    def montant_ennemi(effect: 'Effect', message: 'Message.CheckPlayerCanPayCost') -> 'Resources|None':
        if not EmpatheticAdvantageDisponible(effect) or not EnnemisConfus(effect):
            return None
        return Resources("GB")

    def montant_personnage(effect: 'Effect', message: 'Message.CheckPlayerCanPayCost') -> 'Resources|None':
        joueur = effect.GetInitiator()
        if joueur is None or not EmpatheticAdvantageDisponible(effect) or not PersonnagesConfusDuJoueur(joueur):
            return None
        return Resources("B")

    def defausser_ennemi(cibles: Sequence['CardFace'], effect: 'Effect') -> bool:
        Unused(cibles)
        return DefausserUnConfus(effect, EnnemisConfus(effect))

    def defausser_personnage(cibles: Sequence['CardFace'], effect: 'Effect') -> bool:
        Unused(cibles)
        joueur = effect.GetInitiator()
        return joueur is not None and DefausserUnConfus(effect, PersonnagesConfusDuJoueur(joueur))

    def moyen_personnage() -> 'Ability':
        ability = AbilityFactory.CheckThisCanPayCost(
            montant_personnage,
            bind_ability=lambda face: [e for e in face.effect.Find(func_name="DoGenerateResources")
                                       if e.ability.name == NOM_EA_PERSONNAGE][0],
            conditions=[lambda effect, message: effect.this.IsInPlay() and message.GetToPlayer() == effect.this.GetControlBy()],
        ).SetFuncName("CheckPay").SetSecondType(AbilityType.Resource)
        return ability.SetCostFunc(CostFunc.Custom(None, defausser_personnage)).SetName(NOM_EA_PERSONNAGE)

    return [
        AbilityFactory.CanGenerateResources(
            AbilityType.Resource,
            resources_fn=montant_ennemi,
        ).SetCostFunc(CostFunc.Custom(None, defausser_ennemi))
        .SetName(NOM_EMPATHETIC_ADVANTAGE),
        AbilityFactory.DoGenerateResources(AbilityType.Resource, "This").SetName(NOM_EMPATHETIC_ADVANTAGE),
        moyen_personnage(),
        AbilityFactory.DoGenerateResources(AbilityType.Resource, "This").SetName(NOM_EA_PERSONNAGE),
    ]
