from cards.pack import *

# ===========================================================================
# SENTINEL (T-Wrecks, set 173, prefixe `st`) — helpers partages du pack.
#
# Le pack tourne autour de QUATRE AMELIORATIONS RECTO-VERSO, les COMPONENT :
# Head (st002), Arms (st003), Torso (st004) et Legs (st005). Elles arrivent en
# jeu a la mise en place (`desc.Setup` sur la face INTACT, modele nt003a Battle
# Board) et ne quittent plus la table : leur face INTACT donne une action de
# heros a inclinaison, leur face DESTROYED impose un malus permanent.
#
# Deux mots-cles maison, fiches lues avant d'ecrire une ligne :
#  - **DESTROY** (docs/reference/mots-cles/destroy.md) : 2 degats IMBLOCABLES a
#    Sentinel, puis on retourne le Component sur sa face DESTROYED. Un
#    Component deja detruit ne peut pas l'etre. Neuf cartes l'emploient : elles
#    passent TOUTES par `Detruire()` ci-dessous, pour qu'aucune ne diverge.
#  - **EXPOSED** (docs/reference/mots-cles/exposed.md) : la quatrieme carte
#    d'etat du moteur, posee par `Exposer()`.
#
# ⚠ LES TRAITS INTACT ET DESTROYED N'EXISTENT QUE DANS CE PACK. C'est ce qui
# autorise `trait="INTACT"` comme filtre suffisant : inutile d'exiger AUSSI
# COMPONENT, aucune autre carte du jeu ne porte ces deux traits. Le jour ou un
# autre pack les reprend, il faudra passer par `traits=` et un `check_fn`.
# ===========================================================================

# ⚠ PAS de constante pour « Sentinel ». Le nom est partage avec les trois
# vilains 32084-32086 du set Project Wideawake : aucun script du pack ne doit
# chercher par ce nom, tout passe par `YourIdentity`.
NOM_JUSTON = "Juston Seyfert"

TRAIT_COMPONENT: 'CardFace.TRAITS' = "COMPONENT"
TRAIT_INTACT: 'CardFace.TRAITS' = "INTACT"
TRAIT_DESTROYED: 'CardFace.TRAITS' = "DESTROYED"
TRAIT_HACKED: 'CardFace.TRAITS' = "HACKED"

NOM_HEAD = "Head (Intact)"
NOM_ARMS = "Arms (Intact)"
NOM_TORSO = "Torso (Intact)"
NOM_LEGS = "Legs (Intact)"
NOM_ROGUE_ASSET = "Rogue Asset"

DEGATS_DESTRUCTION = 2


def ComposantsDuJoueur(effect: 'Effect', trait: "CardFace.TRAITS") -> List['CardFace']:
    """Les ameliorations COMPONENT du joueur qui agit, sur la face demandee."""
    joueur = effect.GetInitiator()
    trouves = Worlds.FindCardsOnField(effect, card_type=Upgrade, trait=trait)
    return [f for f in trouves if f.GetControlBy() == joueur]


def ComposantsIntacts(effect: 'Effect') -> List['CardFace']:
    return ComposantsDuJoueur(effect, TRAIT_INTACT)


def ComposantsDetruits(effect: 'Effect') -> List['CardFace']:
    return ComposantsDuJoueur(effect, TRAIT_DESTROYED)


def Detruire(faces: Sequence['CardFace'], effect: 'Effect') -> List['CardFace']:
    """Le mot-cle maison DESTROY, en un seul endroit.

    Pour CHAQUE Component vise : 2 degats imblocables a Sentinel, puis on
    retourne la carte sur sa face DESTROYED. Rend la liste reellement
    retournee.

    ⚠ FILTRE OBLIGATOIRE : « un Component deja sur sa face Destroyed ne peut
    pas etre detruit ». Le moteur ne le deduit pas, chaque appel filtre ici.

    ⚠ « IMBLOCABLES » : `DamageProperty.unpreventable`, drapeau AJOUTE AU MOTEUR
    pour ce pack le 12/09/2026. Il n'existait pas : les deux cartes officielles
    qui emploient le mot (62001a Luke Cage, 62028 Internal Injury) se
    contentaient d'`ignore_tough`, qui ne ferme qu'une porte sur trois. Ici cela
    ne suffisait pas du tout — `st001a` remplace des degats par une destruction,
    dont les 2 degats relancaient l'interruption : une attaque a 2 demontait les
    QUATRE pieces d'un coup (cas st015, mesure du 12/09/2026). Les deux drapeaux
    sont poses ensemble : `unpreventable` ferme la prevention et le
    remplacement, `ignore_tough` ferme la carte Coriace.
    """
    detruits = [f for f in faces
                if f is not None
                and f.HasTrait(TRAIT_COMPONENT) and f.HasTrait(TRAIT_INTACT)]
    if not detruits:
        return []

    this = effect.this
    identite = effect.GetInitiator().GetIdentity()

    retournes: List['CardFace'] = []
    for composant in detruits:
        # ⚠ ON RETOURNE AVANT DE BLESSER, alors que l'insert enonce l'inverse.
        # C'est le seul ordre qui termine. Les 2 degats sont, eux aussi, des
        # degats « que vous alliez subir » : ils relancent l'interruption
        # *Ablative Protocol* de `st001a`. Degats d'abord, le Component vise
        # est encore INTACT quand la relance demande une cible, et la meme
        # piece reste eligible a l'infini — constate le 12/09/2026, trois
        # parties d'autoplay bloquees sur « Ablative_Protocol, cibles legales
        # [11, 10, 9, 8] » repetee a l'identique. Retournement d'abord, chaque
        # tour de boucle consomme une piece : quatre au plus, puis plus aucune
        # cible legale et les degats tombent pour de bon.
        # Aucune difference observable par ailleurs : rien, dans le pack, ne
        # lit l'etat d'un Component entre les deux instructions.
        retournes += Faces.FlipAllTo([composant], None, effect)
        identite.CastTo(Unit2).TakeDamage(
            this,
            DamageProperty(damage=DEGATS_DESTRUCTION, ignore_tough=True,
                           unpreventable=True),
            effect,
        )
    return retournes


def Exposer(faces: Sequence['CardFace'], effect: 'Effect') -> int:
    """Pose une carte d'etat Exposed sur chaque personnage vise.

    Rend le nombre de cartes reellement posees : « expose 2 enemies » ne
    trouve pas toujours deux ennemis.
    """
    return Faces.GiveStatus([f for f in faces if f is not None], "Exposed", effect)


def ExposedEnJeu(effect: 'Effect') -> int:
    """Combien de cartes d'etat Exposed sont en jeu, TOUS personnages confondus.

    ⚠ « in play », pas « sur la cible » : `st007` Hardwire Access et `st013`
    Targeting Protocol lisent le plateau entier, allies compris.
    """
    total = 0
    for personnage in Worlds.GetOnFieldCharacters(effect):
        total += personnage.components.status.exposed
    return total


def VosCartesCoutentUnDePlus(card_type: 'Type[CardFace]|None'=None,
                             trait: "CardFace.TRAITS|None"=None) -> 'Ability':
    """Les trois malus de cout des faces DESTROYED (st002b, st003b, st004b).

    `AbilityFactory.EachCardYouPlayCostAdditionalResource` ne sait filtrer que
    par TYPE de carte : elle appelle `IsType()` sur son argument. Head et Arms
    ont besoin d'un filtre par TRAIT en plus, d'ou cette version maison, posee
    sur la meme fenetre moteur.

    ⚠ `IsThisFaceUp()` EST LA CONDITION CENTRALE, et le defaut qu'elle repare a
    coute la moitie de la batterie du pack (12/09/2026 : dix-neuf cas sur
    trente-neuf, tous des cartes soudain plus cheres d'un cran). Trois raisons
    se conjuguent :
     - `NoOutOfPlayLimit()`, repris de la fabrique d'origine, leve la garde
       « la carte doit etre en jeu » — le calcul du cout se fait dans un
       contexte ou le moteur considere la carte hors jeu ;
     - `IsInPlay()` NE SUFFIT PAS a la remettre : par defaut il accepte
       n'importe quelle face du meme NOM (card_face.py:1007), et
       `ModelName.SetName` coupe la parenthese finale — « Arms (Intact) » et
       « Arms (Destroyed) » portent TOUTES DEUX le nom court « Arms » ;
     - la face DESTROYED d'un Component intact est donc « en jeu » au sens du
       moteur, et son malus s'appliquait pendant que la face INTACT etait
       visible.
    """
    def augmenter(effect: 'Effect', message: 'Message.WhenCalculateEffectCost') -> None:
        message.UpdateCost(+1, effect)

    def bonne_carte(effect: 'Effect', message: 'Message.WhenCalculateEffectCost') -> bool:
        face = message.check_effect.this
        if face is None:
            return False
        if card_type is not None and not card_type.IsType(face):
            return False
        if trait is not None and not face.HasTrait(trait):
            return False
        return True

    return AbilityFactory.WhenCalculateEffectCost(
        AbilityType.NonKeyword,
        augmenter,
        conditions=[
            lambda effect, message:
                effect.this.IsThisFaceUp() and
                effect.this.card.IsOnField() and
                message.is_play and
                effect.this.GetControlBy() == message.GetToPlayer(),
            bonne_carte,
        ],
    ).NoOutOfPlayLimit()


def VosEvenementsDeTraitCoutentUnDePlus(trait: "CardFace.TRAITS") -> 'Ability':
    """« Your [[TRAIT]] events cost 1 additional resource. » (st002b, st003b)"""
    return VosCartesCoutentUnDePlus(card_type=Event, trait=trait)


def ComposantIntactNomme(effect: 'Effect', nom: str) -> 'CardFace|None':
    """Le Component INTACT du joueur qui porte ce nom imprime.

    ⚠ Le NOM COURT ne suffit pas. `ModelName.SetName` (face_name.py:13) coupe
    la parenthese finale : « Head (Intact) » et « Head (Destroyed) » portent
    donc TOUTES DEUX le nom court « Head ». Il faut le nom IMPRIME entier, et
    on double la garde avec le trait INTACT.
    """
    for face in ComposantsIntacts(effect):
        if face.IsName(nom):
            return face
    return None


def SelecteurComposantIntact(nom: str|None=None,
                             exclure: str|None=None,
                             range: 'SELECT.RANGE_TYPE'=(1, 1)):
    """Le selecteur de cout des cartes a cout additionnel (st006 a st012).

    Il sert DEUX choses a la fois : il demande au joueur quel Component payer,
    et il rend la carte INJOUABLE quand aucun Component intact ne reste. Sans
    lui, le cout echouerait apres coup, la carte deja partie de la main.
    """
    return Select.From(
        None,
        finder=CardFinder(
            name=nom,
            non_name=exclure,
            trait=TRAIT_INTACT,
            card_type=Upgrade,
        ),
        from_where=["YouControlCards"],
        range=range,
    )


def InclinerOuDetruire(faces: Sequence['CardFace'], effect: 'Effect') -> bool:
    """Le cout additionnel « exhaust OR destroy », composant par composant.

    ⚠ C'est un choix DANS LE COUT, pas dans l'effet (fiche destroy.md). Deux
    consequences que le moteur ne devine pas :
     - un Component DEJA INCLINE reste payable : « detruire » est encore
       ouvert. C'est ce qui permet de rejouer un evenement dans le meme tour,
       en payant de sa carrosserie. D'ou `CanExhaust()` qui n'ouvre QUE la
       branche inclinaison, jamais la branche destruction.
     - le choix se pose pour CHAQUE Component paye (Exterminate en demande
       deux), pas une fois pour toutes.

    Le montage `ChooseAbilities` dans un `CostFunc.Custom` est celui que le
    moteur avait lui-meme esquisse : voir la classe `CostFunc.Or`, laissee en
    commentaire dans cost_func.py.
    """
    joueur = effect.GetInitiator()

    for face in faces:
        def incliner(cibles: Sequence['CardFace'], e: 'Effect', f: 'CardFace'=face) -> None:
            Unused(cibles)
            Faces.ExhaustAll([f], e)

        def detruire(cibles: Sequence['CardFace'], e: 'Effect', f: 'CardFace'=face) -> None:
            Unused(cibles)
            Detruire([f], e)

        choix: List['Ability'] = []
        if face.CanExhaust():
            choix.append(AbilityFactory.ForChoiceAbility3(
                f"Exhaust {face.printed_name}", incliner))
        choix.append(AbilityFactory.ForChoiceAbility3(
            f"Destroy {face.printed_name}", detruire))

        joueur.ChooseAbilities(effect, *choix)

    return True
