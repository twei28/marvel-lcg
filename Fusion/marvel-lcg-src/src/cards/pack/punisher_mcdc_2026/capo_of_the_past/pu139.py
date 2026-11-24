from . import *
from cards.database import CardsDB

# Capo of the Past — ATTACHEMENT du set modulaire du combat 2 (p277). Permanent. Victory 0. Boost 2 + ★.
# Treat attached character as an ELITE minion. It gains steady, villainous, and victory 0.
# When Revealed : Search your collection for a random CAPO villain. Put it into play engaged with you and attach this card to it.
# ★ Boost : Deal this to yourself as a facedown encounter card.
#
# Cartes de reference : night_thrasher/nt016 (un attachement qui cherche son porteur : `WhenThisRevealed` + `AttachTo2`), brawn/bw021 (« Deal this card to yourself as a
# facedown encounter card » : detourner le rangement de la carte de boost vers `dealt_encounter_cards`), skrull_menace/skrull_elite_skymax/sk243 (`CardFactory.CreateFace`
# du gabarit « Minion », `SetName`, `SetSubtitle`), game/ability/factory/treat.py (`TreatAsMinion` : memes etapes, mais ne gere que les allies et les heros).
# ⚠ Mots-pieges :
#  - « a random CAPO villain » (decision de l'utilisateur, 22/10/2026) : les 8 CAPO sans condition, face A en standard, face B en expert, au hasard de la partie
#    (`Rand.RandomChoice`) ; la « collection » = tous les CAPO du jeu (pas seulement ceux mis de cote) ;
#  - « Treat attached character as an ELITE minion » : la carte devient un SBIRE (gabarit « Minion ») qui GARDE son nom, sa devise, son visuel, ses stats (ATK, SCH, PV
#    FIXES de sa face) et son texte (decision de l'utilisateur : il garde ses capacites) ; il gagne le trait ELITE ;
#  - « It gains steady, villainous, and victory 0 » : les trois, tant que la carte est attachee (permanente) ;
#  - « engaged with YOU » : le joueur qui revele la carte ;
#  - « Deal THIS to yourself » : la carte de boost elle-meme, face cachee, devant le joueur contre qui l'activation a lieu (pas une carte du dessus du deck) ; Permanent :
#    le moteur refuse de la defausser, d'ou le `DealEncounterCard` direct (la carte n'est plus dans la zone de boost quand le moteur range).

TRAIT_ELITE = "ELITE"


def GetAbilities() -> Sequence['Ability']:
    from game.card.factory import CardFactory
    from game.operate.rand import Rand

    def creer_le_sbire(effect: 'Effect', card_id: str) -> 'Minion':
        """Le CAPO (un vilain) en sbire : gabarit « Minion » aux stats, au nom, au visuel et aux capacites du vilain."""
        paper = CardsDB.FindCardPaper(card_id)
        vilain = CardFactory.CreateFace(paper, effect.world)
        sbire = CardFactory.GenerateCard("Minion", None, effect.world).face.CastTo(Minion)
        sbire.pic_id = card_id
        sbire.SetName(vilain.printed_name)
        sbire.SetSubtitle(vilain.printed_subtitle)
        sbire.printed_attack = vilain.printed_attack
        sbire.printed_scheme = vilain.printed_scheme
        sbire.printed_health = vilain.printed_health
        sbire.printed_health_numeral = vilain.printed_health_numeral
        sbire.starting_health = vilain.starting_health
        sbire.ability.Add(*CardsDB.FindAbilities(paper.card_id, paper.pack, paper.set_name))
        sbire.effect.face = sbire
        CardFactory.FaceRegisterEffects(sbire)
        sbire.capo_traits = [t for t in vilain.traits_internal]
        return sbire

    def reveler(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Attachment)
        joueur = message.GetToPlayer()
        suffixe = "b" if Worlds.IsExpert(effect) else "a"
        card_id = Rand.RandomChoice([f"pu0{n}{suffixe}" for n in range(48, 56)], effect)
        sbire = creer_le_sbire(effect, card_id)
        sbire.PutIntoPlay(joueur, effect)
        sbire.GainTraits(1, [*sbire.capo_traits, TRAIT_ELITE], effect)
        sbire.GainKeyword(1, "Steady", effect)
        sbire.GainVillainous(1, effect)
        sbire.printed_victory = 0
        this.AttachTo2(sbire, effect)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        this = effect.this.CastTo(Attachment)
        joueur = message.GetAgainstPlayer()
        if not isinstance(joueur, Player):
            return
        # La carte de boost est donnee face cachee AVANT le rangement du moteur (qui ne defausse que ce qui est encore dans la zone de boost).
        # ⚠ Pas de `WhenCardWouldDiscard` a detourner comme bw021 : la carte est PERMANENTE, `DiscardInternal` refuse de la defausser (elle resterait
        # coincee dans la zone de boost).
        joueur.DealEncounterCard(this, effect)

    return [
        AbilityFactory.WhenThisRevealed(None, reveler),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
