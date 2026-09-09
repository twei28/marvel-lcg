from . import *

# Webbed Up — EVENEMENT, cout 2 [mental]. THWART. WEB.
# Hero Action (thwart): Remove 3 threat from a scheme. Stun a minion (stun an
#   enemy instead if you paid for this card using a [wild] resource).
#
# CARTES DE REFERENCE
#  - `an004`, `vp001a` : `RemoveThreatFromSchemes`.
#  - `05015` Tackle : `Faces.GiveStatus(cibles, "Stunned", effect)`.
#    ⚠ Son RETOUR est un COMPTE (int), pas une liste (`faces.py:180`) — lecon
#    payee sur `sm005` le 08/09/2026.
#  - `32047`, `54002`, `ah007` : lire CE QUI A ETE DEPENSE pour payer la carte
#    passe par les ressources du message de jeu.
#
# TEXTE CONTRE CODE
#  ⚠⚠ « IF YOU PAID FOR THIS CARD USING A [wild] RESOURCE » : la condition
#    porte sur le PAIEMENT, pas sur ce qu'on possede. C'est la seule carte du
#    pack dont l'effet depend de la COULEUR des ressources depensees, et c'est
#    `su011` Web-Shooters qui la sert (elle genere justement un [wild]).
#    ⚠ `convert_green_res=False` : une ressource wild est verte, mais une
#    ressource verte n'est pas « payee en wild » par accident — on lit ce qui a
#    ete REELLEMENT depense.
#  ⚠ « STUN A MINION » par defaut, « AN ENEMY INSTEAD » sous condition :
#    « instead » elargit la cible, il ne double pas l'effet.
#  ⚠ « Remove 3 threat from A SCHEME » : principal OU annexe, au choix.
#  ⚠ Aucune limite imprimee : etape 7 bis sans objet.


def GetAbilities() -> Sequence['Ability']:

    def paye_en_wild(effect: 'Effect') -> bool:
        res = getattr(getattr(effect, "context", None), "paid_this_resources", None)
        if res is None:
            return False
        lire = getattr(res, "GetColor", None)
        if lire is None:
            return False
        return int(lire("G", convert_green_res=False) or 0) > 0

    def toile(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)
        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return

        this.RemoveThreatFromSchemes(effect.targets, 3, effect)

        elargi = paye_en_wild(effect)
        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Stun an enemy" if elargi else "Stun a minion",
                lambda cibles: Faces.GiveStatus(
                    [c for c in cibles if c is not None], "Stunned", effect),
            ).SetTarget(Enemy if elargi else Minion, range=(1, 1)),
        )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            toile,
        ).SetPlay().SetLabel('thwart')
        .SetTarget(Scheme2, range=(1, 1)),
    ]
