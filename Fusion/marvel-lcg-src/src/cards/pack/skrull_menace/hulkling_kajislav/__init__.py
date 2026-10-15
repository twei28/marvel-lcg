from cards.pack import *

# Helpers partages du set « Hulkling (Kajislav) ».
#
# Tout le kit tourne autour de DEUX traits, KREE et SKRULL : la forme
# d'origine (sk002a/b) en donne un a Hulkling, et une dizaine de cartes
# demandent « si tu as / partages ce trait ».

TRAITS_ORIGINE = ("KREE", "SKRULL")


def IdentiteDe(effect: 'Effect') -> 'CardFace|None':
    """L'identite du joueur qui controle la carte qui agit.

    ⚠ Pas `effect.GetInitiator()` en premier : il leve un assert quand
    l'initiateur n'est pas un joueur, et le moteur avale l'exception (lecon
    lady_sif, voir armored_spidey/armored_spidey/__init__.py).
    """
    porteur = getattr(effect, "this", None)
    if porteur is not None:
        joueur = porteur.GetControlByOrOwner()
        if Player.IsType(joueur):
            return joueur.GetIdentity()
    initiateur = getattr(effect, "initiator", None)
    if initiateur is not None and Player.IsType(initiateur):
        return initiateur.GetIdentity()
    return None


def TraitsPartages(face: 'CardFace|None', identite: 'CardFace|None') -> List[str]:
    """Les traits KREE / SKRULL que `face` porte ET que l'identite porte aussi."""
    if face is None or identite is None:
        return []
    return [t for t in TRAITS_ORIGINE if face.HasTrait(t) and identite.HasTrait(t)]


NOMS_ORIGINE = ("Skrull Origin", "Kree Origin")


def ChangerDOrigine(effect: 'Effect', origine: 'CardFace') -> bool:
    """Retourne l'upgrade d'origine EN TANT QUE changement de forme.

    ⚠ Pas un simple `card.Flip` : le livret (p. 4, « Additional Forms ») dit
    qu'un changement de forme additionnelle « counts as changing forms for
    the purpose of triggering card effects such as Shift and Strike ».
    `Identity.ChangeAdditionalFrom` (identity.py) envoie justement
    `WhenUnitWouldChangeForm` (annulable : sk034 Inhibited) puis
    `AfterUnitChangeForm` avec `to_additional_form` renseigne, que lisent
    sk001b, sk004 et sk006. C'est le chemin des formes officielles
    (Form.ChangeFormInternal, Shadowcat/Vision/Nick Fury), sans passer par
    leur liste de noms en dur.
    Rend False si le changement a ete empeche.
    """
    joueur = origine.GetControlByOrOwner()
    if not Player.IsType(joueur):
        return False
    identite = joueur.GetIdentity()

    def retourner() -> 'CardFace':
        origine.card.Flip(effect)
        return origine.card.face

    return identite.ChangeAdditionalFrom(effect, retourner)


def PeutChangerDeForme(effect: 'Effect') -> bool:
    """Faux si un effet en jeu interdit de changer de forme (sk034 Inhibited).

    Lu par la CONDITION de l'Action d'origine : sans elle, l'action resterait
    proposee, l'upgrade s'inclinerait (cout paye) et rien ne se passerait.
    """
    identite = IdentiteDe(effect)
    if identite is None:
        return False
    # Le moteur n'a aucune requete « ce joueur peut-il changer de forme ? » :
    # l'interdiction (PlayersCannotChangeForms) n'agit qu'en ANNULANT le
    # changement au moment ou il part. On lit donc directement la seule carte
    # du coffret qui l'interdit : sk034 Inhibited, attachee a l'identite.
    return not any(a.paper.card_id == "sk034" for a in identite.GetAttachedAttachments())


def CarteDepenseeDeLaMain(face: 'CardFace') -> bool:
    """« spend a card » = une carte DEFAUSSEE DE LA MAIN pour payer.

    Decision de l'utilisateur (15/10/2026) : la capacite Resource d'une carte
    EN JEU (sk013 Excelsior, KREE+SKRULL) genere une ressource mais ne
    « depense » pas la carte. Au moment de `AfterCardsBeSpendAsResource`, une
    carte de main est en transit dans `area_resources` (player_action.py, la
    defausse vient juste apres) ; une carte en jeu est restee en jeu.
    """
    return face.card.area.flags.is_resources_area


def OrigineAbilities(trait_donne: str, trait_depense: str) -> List['Ability']:
    """Les trois capacites d'une face d'origine (sk002a / sk002b)."""

    def apres_depense(effect: 'Effect', message: 'Message.AfterCardsBeSpendAsResource') -> bool:
        joueur = effect.this.GetControlByOrOwner()
        if not Player.IsType(joueur) or message.to_player != joueur:
            return False
        return any(CarteDepenseeDeLaMain(f) and f.HasTrait(trait_depense) for f in message.faces)

    def piocher(effect: 'Effect', message: 'Message.AfterCardsBeSpendAsResource') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(message)
        joueur = this.GetControlByOrOwner()
        if Player.IsType(joueur):
            joueur.DrawUp(1, effect)

    def retourner(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(message)
        ChangerDOrigine(effect, this)

    return [
        *AbilityFactory.GiveKeywordToAttached(
            CardFinder(name="Hulkling"),
            trait=trait_donne,
        ),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            retourner,
            conditions=[lambda effect, message: PeutChangerDeForme(effect)],
        ).SetCostFunc(CostFunc.Exhaust("This")),
        Ability(
            AbilityType.Response,
            Message.AfterCardsBeSpendAsResource,
            [apres_depense],
            piocher,
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]


# Recalcul des bonus « while you have the KREE/SKRULL trait » (sk003, sk012).
# Modele cn002 Belit (pack conan, meme auteur) : `OnEvent.Form` couvre le
# changement de forme (heros <-> civil ET forme d'origine), `OnEvent.Faceup`
# le retournement de l'identite, et `OnEvent.Trait` le trait donne ou retire
# hors changement de forme (sk010 Ancestors, sk034 Inhibited...).
RECALCUL_TRAITS = [OnEvent.Form("YourIdentity"), OnEvent.Faceup("YourIdentity"),
                   OnEvent.Trait("YourIdentity")]


def IdentiteATrait(effect: 'Effect', trait: str) -> bool:
    """« While you have the X trait » : le trait de l'IDENTITE en jeu."""
    identite = IdentiteDe(effect)
    return identite is not None and identite.HasTrait(trait)
