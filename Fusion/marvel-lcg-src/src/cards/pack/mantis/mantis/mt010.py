from . import *

# * The Celestial Madonna : AMELIORATION (TITLE), cout 2, [energy]. Unique. Hero Class.
# Hero Resource: Exhaust The Celestial Madonna → Use Mantis' "Empathetic Advantage" ability. This use does not count against that ability's limit.
# (Version du 04/03/2024 de l'auteur, relevee sur son Drive le 24/11/2026, et celle des scans FRANCAIS depuis le debut : « Ressource de heros », pas « Interruption de heros ». L'ancienne lecture
#  « Hero Interrupt: When you resolve Empathetic Advantage, exhaust ... → this use does not count » est abandonnee ; rapport nicodede62 #167.)
#
# CARTES DE REFERENCE
#  - `mt001a` (meme pack) : Empathetic Advantage, ses DEUX moyens de paiement (origine ENNEMI en `CanGenerateResources`, origine PERSONNAGE en `CheckThisCanPayCost` + `bind_ability` sur son
#    `DoGenerateResources`) et son cout `DefausserUnConfus`. La Madone en est une COPIE, sous son propre nom, avec un cout de plus (s'incliner) et sans le compteur de round.
#  - `ho009` : `CanGenerateResources(AbilityType.HeroResource, resources_fn=..)` + `.SetCostFunc(CostFunc.Exhaust("This"))` + `.SetCostFunc(CostFunc.Custom(None, fn))` (amelioration qui paie en s'inclinant ET en payant un second cout).
#
# TEXTE CONTRE CODE
#  « Hero RESOURCE » : une capacite qui PAIE une carte (comme une carte de la main), forme heros seulement : plus de fenetre d'interruption apres le paiement. « EXHAUST The Celestial Madonna → » = COUT,
#    paye avec l'autre cout (la carte Desoriente a defausser). « USE Mantis' Empathetic Advantage ability » : tout ce que fait Empathetic Advantage, y compris SES DEUX ORIGINES (ennemi : [wild][mental] ;
#    personnage que vous controlez : [mental]) que le joueur choisit en choisissant le moyen, comme sur l'identite. « This use does NOT COUNT against that ability's limit » : ni elle ne lit le
#    compteur du round (la Madone sert justement quand l'emploi imprime est deja pris), ni elle ne l'incremente. La Madone, l'identite et un autre payeur peuvent donc payer UNE MEME carte ensemble.
#  Chiffres : cout 2.


def GetAbilities() -> Sequence['Ability']:

    def madone_prete(effect: 'Effect') -> bool:
        this = effect.this.CastTo(Upgrade)
        return this.IsInPlay() and not this.IsExhaust()

    def montant_ennemi(effect: 'Effect', message: 'Message.CheckPlayerCanPayCost') -> 'Resources|None':
        Unused(message)
        if not madone_prete(effect) or not EnnemisConfus(effect):
            return None
        return Resources("GB")

    def montant_personnage(effect: 'Effect', message: 'Message.CheckPlayerCanPayCost') -> 'Resources|None':
        joueur = effect.GetInitiator()
        # ⚠ « HERO Resource » : forme heros SEULEMENT. `CanGenerateResources(HeroResource)` le sait seul (moyen ennemi), mais `CheckThisCanPayCost` ne lit pas la forme :
        #   sans ce garde le moyen « personnage » etait offert en ALTER-EGO (vu a l'ecran le 24/11/2026, `/get_ask` : l'effet 18 de la Madone au paiement d'une carte).
        if joueur is None or not joueur.IsInHeroForm() or not madone_prete(effect) or not PersonnagesConfusDuJoueur(joueur):
            return None
        return Resources("B")

    def defausser_ennemi(cibles: Sequence['CardFace'], effect: 'Effect') -> bool:
        Unused(cibles)
        return DefausserUnConfus(effect, EnnemisConfus(effect), compter=False)

    def defausser_personnage(cibles: Sequence['CardFace'], effect: 'Effect') -> bool:
        Unused(cibles)
        joueur = effect.GetInitiator()
        return joueur is not None and DefausserUnConfus(effect, PersonnagesConfusDuJoueur(joueur), compter=False)

    def moyen_personnage() -> 'Ability':
        ability = AbilityFactory.CheckThisCanPayCost(
            montant_personnage,
            bind_ability=lambda face: [e for e in face.effect.Find(func_name="DoGenerateResources")
                                       if e.ability.name == NOM_MADONNA_PERSONNAGE][0],
            conditions=[lambda effect, message: effect.this.IsInPlay() and message.GetToPlayer() == effect.this.GetControlBy()],
        ).SetFuncName("CheckPay").SetSecondType(AbilityType.HeroResource)
        return ability.SetCostFunc(CostFunc.Exhaust("This")).SetCostFunc(CostFunc.Custom(None, defausser_personnage)).SetName(NOM_MADONNA_PERSONNAGE)

    return [
        AbilityFactory.CanGenerateResources(
            AbilityType.HeroResource,
            resources_fn=montant_ennemi,
        ).SetCostFunc(CostFunc.Exhaust("This")).SetCostFunc(CostFunc.Custom(None, defausser_ennemi))
        .SetName(NOM_MADONNA_ENNEMI),
        ReserveConfus(AbilityFactory.DoGenerateResources(AbilityType.HeroResource, "This").SetName(NOM_MADONNA_ENNEMI), "enemy"),
        moyen_personnage(),
        ReserveConfus(AbilityFactory.DoGenerateResources(AbilityType.HeroResource, "This").SetName(NOM_MADONNA_PERSONNAGE), "character"),
    ]
