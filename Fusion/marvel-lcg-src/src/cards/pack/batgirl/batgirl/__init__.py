from cards.pack import *

# Helpers partages du set « Batgirl ».
# ⚠ Les modules du set font `from . import *` : un helper defini dans le `__init__.py` du PACK leve un NameError avale
# par le moteur (lecon hk005). Tout ce que les cartes appellent vit donc ICI.

# Couleurs du moteur : R = [physical], B = [mental], Y = [energy], G = [wild].
NOMS_ICONES = {"R": "[physical]", "B": "[mental]", "Y": "[energy]", "G": "[wild]"}

# Les icones de ressource ECRITES DANS LE TEXTE de chaque carte du pack que The Oracle peut changer (une entree par emplacement,
# dans l'ordre du texte). Seules les cartes du pack sont connues : voir la question en attente du gabarit (portee de The Oracle).
ICONES_DU_TEXTE = {
    "bg002": ["B"],            # Black Canary : « for each [mental] resource used to pay »
    "bg004": ["R"],            # Applying Pressure : « using only [physical] resources »
    "bg005": ["Y", "R", "B"],  # Batarangs : [energy] stun, [physical] 2 degats, [mental] confuse
    "bg006": ["G"],            # Master Plan : « considered [wild] resources instead »
    "bg007": ["Y"],            # Calculated Counter : « using only [energy] resources »
}


def JoueurDeCetteCarte(effect: 'Effect') -> 'Player|None':
    """Le joueur a qui appartient la carte qui agit (jamais `GetInitiator()` en premier : il leve un assert quand
    l'initiateur n'est pas un joueur, et le moteur l'avale)."""
    porteur = getattr(effect, "this", None)
    if porteur is not None:
        controleur = porteur.GetControlByOrOwner()
        if Player.IsType(controleur):
            return controleur
    try:
        return effect.GetInitiator()
    except Exception:
        return None


def Icone(effect: 'Effect', couleur: str) -> str:
    """La couleur EFFECTIVE d'une icone du texte de la carte qui resout `effect`, apres The Oracle."""
    changement = getattr(effect, "bg_oracle", None)
    if changement:
        return changement.get(couleur, couleur)
    return couleur


def SansType(effect: 'Effect') -> bool:
    """Recalled Trauma (bg013) : « all cards you spend as resources are considered to have no resource type » jusqu'a la fin du
    PROCHAIN round. Le moteur n'a pas de ressource sans type : la regle ne vaut que pour les cartes du pack (qui lisent le paiement
    par ces helpers), pas pour les cartes officielles — limite documentee dans le gabarit."""
    joueur = JoueurDeCetteCarte(effect)
    if joueur is None:
        return False
    return getattr(joueur, "bg_sans_type", -1) >= joueur.world.round_id


def Compter(effect: 'Effect', res: 'Resources', couleur: str, **kw) -> int:
    """Nombre de ressources `couleur` payees (0 sous Recalled Trauma)."""
    if SansType(effect):
        return 0
    return res.GetColor(couleur, **kw)


def SeulementPaye(res: 'Resources', couleur: str, effect: 'Effect|None'=None) -> bool:
    """« If you paid for this card using ONLY <couleur> resources » : au moins une ressource, et rien d'autre."""
    if effect is not None and SansType(effect):
        return False
    if res.val <= 0:
        return False
    if couleur == "G":
        return res.GetColor("G", convert_green_res=False) == res.val
    return res.OnlyHasColor(couleur)


def CarteDuMessage(message) -> str:
    """Le card_id de la carte qui declenche (message.trigger)."""
    face = getattr(message, "trigger", None)
    return getattr(getattr(face, "paper", None), "card_id", None)


def AbiliteOracle() -> List['Ability']:
    """« The Oracle — Interrupt: When you resolve the effect of a card, change a resource icon in the text of that card to a
    resource icon of your choice. (Limit once per round.) » Le choix est memorise sur l'EFFET de la carte resolue
    (`effect.bg_oracle = {icone du texte: icone choisie}`) ; chaque carte du pack relit son icone par `Icone(effect, ...)`.
    DEUX fenetres : la resolution d'une capacite (allies, ameliorations...) et le JEU d'un evenement (le moteur n'envoie pas
    `WhenEffectWouldResolve` pour la capacite de jeu d'un evenement)."""

    def poser(cible: 'Effect', source: str, dest: str) -> None:
        changement = dict(getattr(cible, "bg_oracle", None) or {})
        changement[source] = dest
        cible.bg_oracle = changement

    def proposer(effect: 'Effect', cible: 'Effect', cid: str) -> None:
        joueur = JoueurDeCetteCarte(effect)
        icones = ICONES_DU_TEXTE.get(cid)
        if joueur is None or not icones:
            return
        # Premiere option = ne rien changer : la capacite est facultative, et c'est ce que prend le pilote du harnais par defaut.
        choix = [AbilityFactory.ForChoiceAbility("Keep the text as printed", lambda targets: None).SetHasNoTargetEffect()]
        for source in icones:
            for dest in ("R", "B", "Y", "G"):
                if dest == source:
                    continue
                choix.append(AbilityFactory.ForChoiceAbility(
                    f"Change {NOMS_ICONES[source]} to {NOMS_ICONES[dest]}",
                    (lambda s, d: (lambda targets: poser(cible, s, d)))(source, dest),
                ).SetHasNoTargetEffect())
        joueur.ChooseAbilities(effect, *choix)

    def oracle_resolution(effect: 'Effect', message: 'Message.WhenEffectWouldResolve') -> None:
        proposer(effect, message.effect, CarteDuMessage(message))

    def oracle_jeu(effect: 'Effect', message: 'Message.WhenPlayerPlayCard') -> None:
        proposer(effect, message.played_effect, getattr(getattr(message.played_face, "paper", None), "card_id", None))

    return [
        AbilityFactory.WhenCardWouldResolveAbility(
            AbilityType.Interrupt, None, None, oracle_resolution,
            card_control_by="You", trigger_player="You",
            conditions=[lambda e, m: CarteDuMessage(m) in ICONES_DU_TEXTE and not Event.IsType(m.trigger)],
        ).SetName("The Oracle").LimitOncePerRound(),
        AbilityFactory.WhenPlayerPlayCard(
            AbilityType.Interrupt, "You", None, oracle_jeu,
            conditions=[lambda e, m: Event.IsType(m.played_face)
                        and getattr(getattr(m.played_face, "paper", None), "card_id", None) in ICONES_DU_TEXTE],
        ).SetName("The Oracle").LimitOncePerRound(),
    ]


def SuivisDeLaManche() -> List['Ability']:
    """Alimente le registre « ce round » lu par Eidetic Memory : « If you defeated an enemy or removed the last threat from a
    scheme this round »."""

    def marquer(effect: 'Effect', message) -> None:
        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return
        effect.this.card.world.stat.AddRoundCounter(joueur, "bg_exploit")

    return [
        AbilityFactory.AfterUnitDefeatedUnit(AbilityType.NonKeyword, "You", Enemy, marquer),
        AbilityFactory.AfterSchemeRemoveThreat(
            AbilityType.NonKeyword, Scheme2, marquer, last_threat=True,
            conditions=[lambda e, m: getattr(m.would_remove_message, "by_face", None) is not None
                        and m.would_remove_message.by_face.GetControlByOrOwner() == JoueurDeCetteCarte(e)]),
    ]


def ExploitCeRound(joueur: 'Player', effect: 'Effect') -> bool:
    return joueur.world.stat.GetRoundCounter(joueur, "bg_exploit") > 0


def ChoisirUnEnnemi(joueur: 'Player', effect: 'Effect') -> 'CardFace|None':
    ennemis = Worlds.GetOnFieldEnemies(effect)
    if not ennemis:
        return None
    return joueur.AskChooseFace(ennemis, effect)


def FaceEstVaincue(face: 'CardFace') -> bool:
    return (not face.IsInPlay()) or face.IsDefeated()


def VersWild(res_message: 'Resources') -> 'Resources':
    return Resources("G") * res_message.val


def ConvertirEnWild(joueur_cible: 'Player', *, until_round: bool, once: bool, porteur: 'CardFace', origine: 'CardFace') -> None:
    """Nightwing : « the next resource you generate is considered a [wild] resource ». ⚠ La conversion doit rester ACTIVE tant que le
    paiement n'est pas fait : le moteur calcule les moyens de paiement une premiere fois (apercu) puis les relit au paiement ; un effet
    temporaire qui se detruit au premier calcul (`unregister_after_exec=True`) n'agit donc jamais sur ce qui est PAYE (vu : le journal
    montrait la conversion, `GetPaidResources` gardait le type imprime). On la garde jusqu'a la fin du tour et on ne convertit que la
    PREMIERE ressource de chaque generation."""

    def convertir(effect: 'Effect', message: 'Message.CheckEffectGeneratedResources') -> None:
        res = message.res
        if res.val <= 0:
            return
        for couleur in ("R", "B", "Y"):
            if res.GetColor(couleur, convert_green_res=False) > 0:
                message.SetResources(res - Resources(couleur) + Resources("G"), effect)
                return

    def est_a_moi(effect: 'Effect', message: 'Message.CheckEffectGeneratedResources') -> bool:
        return message.GetToPlayer() == joueur_cible

    porteur.effect.RegisterTemp(
        Ability(AbilityType.NonKeyword, Message.CheckEffectGeneratedResources, [est_a_moi], convertir),
        unregister_after_exec=False,
        until_turn_end=True,
    )
