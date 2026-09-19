from cards.pack import *
# Le helper de paiement vit au niveau du PACK ; `from . import *` d'une carte
# ne remonte qu'a ce module, il faut le re-exporter ici.
from cards.pack.fne import PeutCouvrirLeCout

# Helpers du set Art Museum Heist (Fear No Evil, 60121-60127).
# Les quatre oeuvres (60122-60125) portent le trait ART.


def OeuvresSur(face: 'CardFace') -> List['Attachment']:
    """Les attachements ART accroches a `face`."""
    return [a for a in face.GetAttachedAttachments() if a.HasTrait("ART")]


def OeuvresSurLesIdentites(effect: 'Effect') -> List['Attachment']:
    oeuvres: List['Attachment'] = []
    for joueur in effect.world.const_players:
        identite = joueur.GetIdentity()
        if identite is not None:
            oeuvres.extend(OeuvresSur(identite))
    return oeuvres


def DeplacerUneOeuvreVersLeVilain(effect: 'Effect', joueur: 'Player') -> bool:
    """« move an ART attachment from an identity to the villain ».
    Le joueur choisit l'oeuvre quand il y en a plusieurs. Rend False si aucune
    oeuvre n'est accrochee a une identite."""
    vilain = Worlds.FindVillain(effect)
    oeuvres = OeuvresSurLesIdentites(effect)
    if vilain is None or not oeuvres:
        return False
    oeuvre = joueur.AskChooseFace(oeuvres, effect, prompt="Move an Art attachment to the villain") if len(oeuvres) > 1 else oeuvres[0]
    if oeuvre is None:
        return False
    return oeuvre.AttachTo2(vilain, effect)


def DeplacerUneOeuvreDuVilainVers(effect: 'Effect', joueur: 'Player', cible: 'CardFace') -> bool:
    """« move an ART attachment from the villain to your identity »."""
    vilain = Worlds.FindVillain(effect)
    if vilain is None:
        return False
    oeuvres = OeuvresSur(vilain)
    if not oeuvres:
        return False
    oeuvre = joueur.AskChooseFace(oeuvres, effect, prompt="Move an Art attachment to your identity") if len(oeuvres) > 1 else oeuvres[0]
    if oeuvre is None:
        return False
    return oeuvre.AttachTo2(cible, effect)


def CapacitesDUneOeuvre(cout: 'Cost', a_l_attache: Callable[['Effect', 'Unit2'], None]|None) -> Sequence['Ability']:
    """Le tronc commun des quatre oeuvres :
    - Attach to the villain (+1 SCH / +1 THW : cles desc "SCH+"/"THW+") ;
    - Forced Response: After this card attaches to a character, <effet> ;
    - Hero Action: Spend a <ressource> OR exhaust your hero -> attach this card
      to your hero. Deux couts alternatifs = deux capacites (RECETTES §5).
    Surge est une base automatique (desc.Surge).
    """
    def apres_attache(effect: 'Effect', message: 'Message.AfterCardAttachTo') -> None:
        if a_l_attache is not None and Unit2.IsType(message.to_face):
            a_l_attache(effect, message.to_face.CastTo(Unit2))

    def pas_deja_sur_mon_heros(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> bool:
        this = effect.this
        joueur = effect.GetInitiator()
        return this.GetBindFace() is not joueur.GetIdentity()

    def vers_mon_heros(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Attachment)
        joueur = effect.GetInitiator()
        this.AttachTo2(joueur.GetIdentity(), effect)

    capacites: List['Ability'] = [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(Villain),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            vers_mon_heros,
            conditions=[pas_deja_sur_mon_heros],
        ).SetName("Spend a resource: attach to your hero").SetCost(cout),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            vers_mon_heros,
            conditions=[pas_deja_sur_mon_heros],
        ).SetName("Exhaust your hero: attach to your hero").SetCostFunc(CostFunc.Exhaust("YourIdentity")),
    ]
    if a_l_attache is not None:
        capacites.append(
            AbilityFactory.AfterCardAttachTo(
                AbilityType.ForcedResponse,
                "This",
                Unit2,
                apres_attache,
            )
        )
    return capacites
