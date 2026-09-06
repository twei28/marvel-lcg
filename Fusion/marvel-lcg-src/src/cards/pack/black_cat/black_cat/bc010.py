from . import *

# Ill Gotten Gains — AMELIORATION, cout 2, [wild]. ITEM. x2.
# Resource: Exhaust this card -> generate a [wild] resource ([wild][wild]
#   resources instead for an attachment).
# Response: After you discard an attachment with the text "Hero Action" or
#   "Hero Response" from play, tuck it under your identity.
#
# ⚠ CE QUE LA CARTE VEUT DIRE, ET QU'IL FAUT AVOIR COMPRIS AVANT DE LA CODER.
# On ne JOUE pas un attachement : c'est une carte de RENCONTRE. « Payer pour un
# attachement », c'est payer le cout imprime SUR lui — 132 attachements du
# depot portent « <b>Hero Action</b>: Spend X resources -> discard this card »
# (`01100` Enhanced Ivory Horn, `04072` Laser Rifle...). Ill Gotten Gains paie
# donc DOUBLE quand on nettoie l'equipement du vilain, et la Response ramasse
# ensuite la carte defaussee. Les deux moities sont la meme idee : Black Cat
# vole le materiel de l'ennemi.
#
# CARTES DE REFERENCE
#  - `tg008` Frog of Thunder / `54002` * Cybernetic Arm : le montage
#    « `CanGenerateResources` a cout d'inclinaison + comportement conditionne
#    par la carte payee », lue sur `message.paying_for_effect`.
#  - `58008` Ionic Belt (pack wonder_man) : le meme `paying_for_effect.this`
#    employe dans une CONDITION.
#  - `AbilityFactory.AfterCardDiscard` (factory/discard.py:103) pour la
#    Response.
#
# TEXTE CONTRE CODE
#  ⚠ « generate A [wild] resource ([wild][wild] INSTEAD for an attachment) » ->
#    la quantite DEPEND de ce qu'on paie : `resources_fn`, pas `resources`.
#    Un `for_card=` serait FAUX — il RESTREINDRAIT ce que la carte peut payer,
#    alors que le texte dit qu'elle paie tout, en donnant seulement plus pour
#    un attachement. Meme piege que `tg008`, ou `for_card` avait ete ecarte
#    pour la meme raison.
#  ⚠ « RESOURCE » et non « Hero Resource » : la ressource marche AUSSI en
#    forme civile. Contre-intuitif sur une carte de heros, mais imprime.
#  ⚠ « after you DISCARD an attachment ... FROM PLAY » -> depuis le TERRAIN,
#    pas depuis une main ni un deck. `message.from_area.flags.is_in_play` le
#    verifie plutot que de le supposer.
#  ⚠⚠ LE FILTRE EST UNE `conditions`, PAS UN `return` EN TETE D'OPERATION.
#    Ecrite d'abord avec les trois tests dans le corps, la carte etait
#    fonctionnellement juste ET INJOUABLE : `AfterCardDiscard(..., None, ...)`
#    se declenche sur CHAQUE defausse de la partie, et une Response est une
#    capacite OPTIONNELLE — le moteur pose donc la question a chaque fois,
#    meme quand l'operation va sortir aussitot. Mesure de l'autoplay du
#    05/09/2026, 8 parties : **250 questions « Response »**, dont 243 pour
#    cette seule carte. Deplacer les tests dans `conditions` ne change RIEN au
#    resultat et supprime la question. Defaut d'ERGONOMIE, invisible pour
#    toutes les gates statiques et pour les cas de test : seule une partie
#    reellement jouee le montre.
#  ⚠ « with the text "Hero Action" or "Hero Response" » -> le filtre est le
#    TEXTE IMPRIME, lu sur `face.paper.text`. C'est la brique 3 du plan de
#    portage (« selection d'une carte par son TEXTE ») : aucune primitive
#    moteur, une lecture de chaine.
#  « tuck it under YOUR IDENTITY » -> la meme pile que « under Black Cat »
#    ailleurs dans le set (card_face.py:1017).


def GetAbilities() -> Sequence['Ability']:

    def porte_une_action_de_heros(face: 'CardFace') -> bool:
        texte = getattr(face.paper, "text", "") or ""
        return "Hero Action" in texte or "Hero Response" in texte

    def combien_de_ressources(effect: 'Effect',
                              message: 'Message.CheckPlayerCanPayCost') -> 'Resources|None':
        Unused(effect)
        payee = getattr(getattr(message, "paying_for_effect", None), "this", None)
        if payee is not None and Attachment.IsType(payee):
            return Resources("GG")
        return Resources("G")

    def cest_bien_un_attachement_vole(effect: 'Effect',
                                      message: 'Message.AfterCardDiscard') -> bool:
        Unused(effect)
        carte = message.trigger
        return (carte is not None
                and Attachment.IsType(carte)
                and message.from_area.flags.is_in_play
                and porte_une_action_de_heros(carte))

    def butin(effect: 'Effect', message: 'Message.AfterCardDiscard') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)
        GlisserSousIdentite(effect, [message.trigger], JoueurDeCetteCarte(effect))

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.CanGenerateResources(
            AbilityType.Resource,
            resources_fn=combien_de_ressources,
        ).SetCostFunc(CostFunc.Exhaust("This")),
        AbilityFactory.AfterCardDiscard(
            AbilityType.Response,
            None,
            butin,
            conditions=[cest_bien_un_attachement_vole],
        ),
    ]
