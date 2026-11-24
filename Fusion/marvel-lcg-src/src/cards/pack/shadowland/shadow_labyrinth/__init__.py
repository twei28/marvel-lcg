from cards.pack.shadowland import *
from game.message.message_type import CheckIfMessage, TriggerPlayerMessage
from cards.database import CardsDB
from cards.pack.fne import PeutCouvrirLeCout
from cards.pack.hunting_season.trap import LimiteParJoueurEtParRound

# ===========================================================================
# Helpers partages du scenario SHADOW LABYRINTH (sets Shadow Labyrinth sl037-sl045 et Deadly Contraptions sl046-sl056).
# Decisions de mecanique (le livret p. 12 est introuvable) : docs/packs/shadowland/DECISIONS-b.md.
#
#  - le PAQUET PIEGE (« trap deck ») : scenario deck « TrapDeck » + sa defausse (« trap discard pile »), cree a la mise en place de sl038a avec les 8 cartes TRAP!
#    mises de cote (Whisper in the Dark + les 7 pieges de Deadly Contraptions) ; on y MELANGE aussi des cartes du deck de rencontre (sl041, sl045) ;
#  - « reveal the top card of the trap deck » : la carte est revelee au joueur concerne (ses When Revealed partent) ; paquet vide -> on remelange la defausse ;
#  - un piege (traitrise TRAP!) propose « Avoid / Disarm / Trip » : `ChoixDePiege` ;
#  - « When you choose the "Avoid"/"Disarm"/"Trip" effect on a TRAP! card » : message maison `QuandOnChoisitUnEffetDePiege` (le moteur n'envoie rien apres le choix
#    d'une option nommee) ; « you cannot choose the "Avoid" effect » (Iron Monk) : message maison `PeutChoisirUnEffetDePiege`.
# ===========================================================================

CORRIDORS = "sl037"
PIEGE_AVOID, PIEGE_DISARM, PIEGE_TRIP = "Avoid", "Disarm", "Trip"
CLE_VILAIN_CHOISI = "sl_vilain_choisi"          # attribut du monde : « sl014 » (le vilain Dark Protege tire a la mise en place)
_ID_VILAIN = re.compile(r'^(sl\d{3})[ab]?$')


################################################################################
# MESSAGES MAISON
################################################################################
class QuandOnChoisitUnEffetDePiege(TriggerPlayerMessage):
    """« When you choose the "Avoid" effect (or "Disarm", "Trip") on a TRAP! card » : envoye par `ChoixDePiege` APRES le choix du joueur, AVANT que l'effet ne se resolve
    (les Forced Interrupt de sl046, sl048 et sl049 s'y accrochent)."""

    def __init__(self, joueur: 'Player', piege: 'CardFace', effet: str) -> None:
        self.piege = piege
        self.effet = effet
        super().__init__(player=joueur)
        self.AddRelatedFace(piege)


class PeutChoisirUnEffetDePiege(CheckIfMessage):
    """« you cannot choose the "Avoid" effect on TRAP! cards » : question posee par `ChoixDePiege` avant d'offrir une option (sl047 Iron Monk y repond)."""

    def __init__(self, joueur: 'Player', piege: 'CardFace', effet: str) -> None:
        self.piege = piege
        self.joueur = joueur
        self.effet = effet
        self.peut_choisir = True
        super().__init__(piege)

    def Interdire(self, par_effet: 'Effect') -> None:
        self.peut_choisir = False
        self.SetCauseBy(par_effet)


################################################################################
# VILAIN CHOISI ET SHIFTING CORRIDORS
################################################################################
def Corridors(effect: 'Effect') -> 'Villain|None':
    """Shifting Corridors s'il est EN JEU (« If Shifting Corridors is in play »), sinon None."""
    for vilain in Worlds.GetAllVillains(effect):
        if vilain.IsCardId(CORRIDORS) and vilain.IsInPlay():
            return vilain
    return None


def MemoriserVilainChoisi(effect: 'Effect', face: 'CardFace') -> None:
    setattr(effect.world, CLE_VILAIN_CHOISI, _ID_VILAIN.match(str(face.paper.card_id)).group(1))


def VilainChoisi(effect: 'Effect') -> 'CardFace|None':
    """La carte du vilain Dark Protege tire a la mise en place, TELLE QU'ELLE EST mise de cote (None s'il est deja en jeu ou si rien n'a ete tire)."""
    base = getattr(effect.world, CLE_VILAIN_CHOISI, None)
    if base is None:
        return None
    for face in Worlds.GetSetAsideAreaCards(effect):
        if Villain.IsType(face) and str(face.paper.card_id).startswith(base):
            return face
    return None


################################################################################
# PAQUET PIEGE
################################################################################
def PaquetPiege(effect: 'Effect') -> 'SetAsideDeck':
    return Worlds.ScenarioDeck(effect, "TrapDeck")


def CreerPaquetPiege(effect: 'Effect') -> None:
    """« Create the trap deck » : les cartes TRAP! mises de cote, melangees, faces cachees ; leur defausse est la « trap discard pile »."""
    support = Worlds.FindVillain(effect) or effect.this
    paquet = PaquetPiege(effect)
    paquet.Create(effect, support, type=DeckType.AdditionalDeck)
    pieges = [f for f in Worlds.AsideDeck(effect).Get(True) if f.HasTrait("TRAP!")]
    # AJOUT (23/10/2026, livret FR p. 12) : « si les joueurs personnalisent ce scenario avec d'autres sets modulaires comprenant des cartes PIEGE !,
    # integrez-les egalement au deck Piege ». Le deck de rencontre est cree avant la mise en place du complot : ces cartes y sont deja, on les en retire.
    pieges += [f for f in Worlds.GetEncounterDeckCards(effect) if f.HasTrait("TRAP!") and f not in pieges]
    Faces.ShuffleAllTo(pieges, paquet.deck, effect)
    Faces.BindDiscardPile(pieges, paquet.discard_pile)


def PaquetPiegeCree(effect: 'Effect') -> bool:
    return PaquetPiege(effect).initialize


def MelangerDansPaquetPiege(effect: 'Effect', *, du_deck_rencontre: int=0, avec_defausse: bool=False) -> None:
    """« Shuffle [the trap discard pile and] the top N cards of the encounter deck into the trap deck. »"""
    if not PaquetPiegeCree(effect):
        return
    paquet = PaquetPiege(effect)
    if du_deck_rencontre:
        Faces.MoveAllTo(list(Worlds.GetEncounterDeckCards(effect)[:du_deck_rencontre]), paquet.deck, effect)
    if avec_defausse:
        paquet.deck.ShuffleWithDiscardPile(False, effect)
    else:
        paquet.deck.Shuffle(effect)


def ReveleDuPaquetPiege(effect: 'Effect', joueur: 'Player') -> 'CardFace|None':
    """« Reveal the top card of the trap deck. » Paquet vide : la defausse est remelangee (regle habituelle d'un deck qui s'epuise) ; rien si les deux sont vides."""
    if not PaquetPiegeCree(effect):
        return None
    paquet = PaquetPiege(effect)
    if paquet.deck.GetSize() == 0 and paquet.discard_pile.GetSize() > 0:
        paquet.deck.ShuffleWithDiscardPile(False, effect)
    face = paquet.GetTopCard()
    if face is None:
        return None
    face.Reveal(joueur, effect)
    return face


################################################################################
# « CHOOSE : AVOID / DISARM / TRIP »
################################################################################
def PeutChoisir(effect: 'Effect', joueur: 'Player', piege: 'CardFace', option: str) -> bool:
    """Faux si une carte interdit ce choix (Iron Monk interdit Avoid)."""
    question = PeutChoisirUnEffetDePiege(joueur, piege, option)
    question.Send()
    return question.peut_choisir


def OptionDePiege(effect: 'Effect', joueur: 'Player', option: str, libelle: str, operation: Callable[[], None], *, faisable: bool=True,
                  cout: 'str|None'=None, cible: 'Callable[[Ability], Ability]|None'=None) -> 'Ability|None':
    """UNE option « Avoid / Disarm / Trip » d'un piege. `faisable` : l'option n'est offerte que si ce qu'elle exige (carte a defausser, ressources) existe -- comme sl004a,
    le moteur reduirait sinon un choix impayable au plus gros morceau payable et l'Avoid deviendrait gratuit. `cout` : « Spend [energy][energy] resources » (Cost("YY")).
    Les Forced Interrupt « When you choose the X effect » (sl046, sl048, sl049) passent AVANT l'effet."""
    piege = effect.this
    if not faisable or not PeutChoisir(effect, joueur, piege, option):
        return None

    def resolution(*_: Any) -> None:
        QuandOnChoisitUnEffetDePiege(joueur, piege, option).Send()
        operation()

    nom = f"{option}: {libelle}"
    if cout is not None:
        if not PeutCouvrirLeCout(joueur, effect, Cost(cout)):
            return None
        return AbilityFactory.ForChoiceAbilityWithCost(Cost(cout), nom, lambda targets, res: resolution())
    ability = AbilityFactory.ForChoiceAbility(nom, lambda targets: resolution())
    return cible(ability) if cible is not None else ability


def ChoixDePiege(effect: 'Effect', joueur: 'Player', evite: 'Ability|None', desarme: 'Ability|None', declenche: 'Ability|None') -> None:
    """« Choose: Avoid / Disarm / Trip » : Trip est toujours faisable (des degats), les deux autres selon ce que le joueur peut fournir."""
    joueur.ChooseAbilities(effect, *[a for a in (evite, desarme, declenche) if a is not None])


def DefausserUneCarteDeLaMain(effect: 'Effect', joueur: 'Player', candidates: Sequence['CardFace']) -> 'CardFace|None':
    """Defausse UNE carte de la main parmi `candidates` (le joueur choisit s'il y en a plusieurs)."""
    if not candidates:
        return None
    choisie = joueur.AskChooseFace(candidates, effect, not_move=True)
    if choisie is not None:
        Faces.DiscardAll([choisie], effect)
    return choisie


def EvenementsDeLaMain(joueur: 'Player', trait: str) -> List['CardFace']:
    """Les evenements de la main portant un trait (THWART, DEFENSE, ATTACK...)."""
    return [f for f in joueur.hand_cards.Get() if Event.IsType(f) and f.HasTrait(trait)]


def AlliesDeLaMain(joueur: 'Player') -> List['CardFace']:
    return [f for f in joueur.hand_cards.Get() if Ally.IsType(f)]


def AmeliorationsDeLaMain(joueur: 'Player') -> List['CardFace']:
    return [f for f in joueur.hand_cards.Get() if Upgrade.IsType(f)]


################################################################################
# WHISPER IN THE DARK : le vilain traite comme un sbire ELITE
################################################################################
def CreerLeSbireDuVilain(effect: 'Effect', card_id: str, pv: int) -> 'Minion':
    """« Treat attached villain as an ELITE minion with N printed hit points » : un sbire (gabarit « Minion ») qui garde le nom, la devise, le visuel, les stats (ATK, SCH)
    et le texte de la face du vilain, mais N PV imprimes. Meme technique que punisher_mcdc_2026/pu139 (`TreatAsMinion` du moteur ne gere que les allies et les heros).
    La vraie carte du vilain reste de cote, intacte : c'est elle que sl039a revelera."""
    paper = CardsDB.FindCardPaper(card_id)
    vilain = CardFactory.CreateFace(paper, effect.world)
    sbire = CardFactory.GenerateCard("Minion", None, effect.world).face.CastTo(Minion)
    sbire.pic_id = card_id
    sbire.SetName(vilain.printed_name)
    sbire.SetSubtitle(vilain.printed_subtitle)
    sbire.printed_attack = vilain.printed_attack
    sbire.printed_scheme = vilain.printed_scheme
    sbire.printed_health = pv
    sbire.printed_health_numeral = pv
    sbire.starting_health = pv
    sbire.ability.Add(*CardsDB.FindAbilities(paper.card_id, paper.pack, paper.set_name))
    sbire.effect.face = sbire
    CardFactory.FaceRegisterEffects(sbire)
    sbire.sl_traits = [t for t in vilain.traits_internal]
    sbire.sl_sosie_du_vilain = True
    return sbire


def SbiresSosies(effect: 'Effect') -> List['CardFace']:
    """Les sbires nes de Whisper in the Dark (le vilain traite comme un sbire) encore en jeu."""
    return [f for f in Worlds.GetOnFieldMinions(effect) if getattr(f, 'sl_sosie_du_vilain', False)]


def ChoisirUneCarte(effect: 'Effect', joueur: 'Player', candidates: Sequence['CardFace']) -> 'CardFace|None':
    """Le joueur choisit UNE carte parmi `candidates` (aucune question s'il n'y en a qu'une)."""
    if not candidates:
        return None
    return joueur.AskChooseFace(candidates, effect, not_move=True)


def DefausserUneCarteEnJeu(effect: 'Effect', joueur: 'Player', candidates: Sequence['CardFace']) -> 'CardFace|None':
    """« Discard an ally / an upgrade / a support you control » : une carte EN JEU parmi `candidates`."""
    choisie = ChoisirUneCarte(effect, joueur, candidates)
    if choisie is not None:
        Faces.DiscardAll([choisie], effect)
    return choisie


def DegatsEtStatut(effect: 'Effect', joueur: 'Player', degats: int, statut: 'str|None') -> None:
    """« Deal N damage to your identity and confuse / stun / exhaust it. » (le piege est la source des degats)"""
    identite = joueur.GetIdentity()
    effect.this.DealDamage([identite], degats, effect)
    if statut == "Exhausted":
        Faces.ExhaustAll([identite], effect)
    elif statut is not None:
        Faces.GiveStatus([identite], statut, effect)
