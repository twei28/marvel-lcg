from cards.pack import *
import re


def AttacheAuSbireLePlusSolide() -> 'Ability':
    """« Attach to the minion with the highest base hit points and give that
    minion a tough status card. Otherwise, this card gains surge. »
    highest_printed_hp = PV imprimes (« base »), when_attach_operation pose la
    robustesse au moment de l'accrochage."""
    return AbilityFactory.AttachToFaceWhenPutIntoPlay(
        Minion,
        highest_printed_hp=True,
        if_cannot_gain_surge=True,
        when_attach_operation=lambda face, effect: Faces.GiveStatus([face], "Tough", effect),
    )


def PeutSAccrocherAUnSbire(face: 'CardFace', sbire: 'CardFace') -> bool:
    """« an attachment that can attach to a minion » (60197 Beetle).
    La regle moteur `Asset2.CanAttachTo` (asset.py:69) ne connait que MaxPerUnit
    et `CheckIfFaceCanAttachTo` : elle acceptait Energy Gatling Gun (« Attach to
    the villain ») sur un sbire (harnais du 18/09/2026). La VRAIE cible
    imprimee vit dans le selecteur de `AttachToFaceWhenPutIntoPlayInternal`,
    expose depuis le 18/09/2026 (coordinateur) en `ability.attach_selector`
    sur l'ability `func_name="AttachToWhenEnterPlay"`.
    On interroge `selector_filter.CheckFinder(sbire, effet)` : le finder
    (Villain / Minion / Enemy, `non_trait`, `not_with_attach`...) et ses
    conditions (`CanAttachTo`, MaxPerUnit), SANS `selector_rule.Process`
    (le tri highest_printed_hp / highest_atk de `GetAllLegalTargets`), sinon
    « peut s'accrocher a un sbire » dependrait des AUTRES sbires en jeu.
    Repli, seulement si aucune ability n'expose de selecteur (attachement
    ecrit sans cette fabrique) : relecture de la phrase imprimee
    « Attach to ... » du texte de la carte."""
    if not Attachment.IsType(face) or not face.CastTo(Attachment).CanAttachTo(sbire):
        return False
    selecteurs = [getattr(a, "attach_selector", None)
                  for a in face.ability.Find(func_name="AttachToWhenEnterPlay")]
    selecteurs = [x for x in selecteurs if x is not None]
    if selecteurs:
        from game.effect.rule import GameRule   # pas re-exporte par cards.pack
        effet = GameRule(face)
        return any(sel.selector_filter.CheckFinder(sbire, effet) for sel in selecteurs)
    # Repli texte (aucun selecteur expose).
    texte = getattr(face.paper, "text", "") or ""
    m = re.search(r"\battach(?:es)? (?:this card )?to (?:the |a |an |each )?([^.\n]*)", texte, re.I)
    if not m:
        return True
    phrase = m.group(1).lower()
    if not re.search(r"\b(minion|enemy|character)\b", phrase):
        return False
    for trait in re.findall(r"non-\[\[([^\]]+)\]\]", phrase):
        if sbire.HasTrait(trait.upper()):
            return False
    for trait in re.findall(r"(?<!non-)\[\[([^\]]+)\]\] (?:minion|enemy|character)", phrase):
        if not sbire.HasTrait(trait.upper()):
            return False
    return True
