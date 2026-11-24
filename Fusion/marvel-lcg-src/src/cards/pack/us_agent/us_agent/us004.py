from . import *

# Reckless — evenement signature, x2 (6/15, 7/15). ATTACK. TACTIC. THWART. Cout 0, ressource [mental].
# Hero Action (attack/thwart): Take X damage → remove X threat from a scheme and deal X damage to an enemy
# (to a maximum of 4.)
#
# Cartes de reference :
#  - `tm006` Majime : MEME carte au maximum ppres (3 chez Majime, 4 ici) ; son squelette (`DeclareNumber(0, N)`,
#    `heros.TakeDamage(this, declare, effect)`, X relu sur les PV REELLEMENT perdus) est une decision utilisateur du
#    15/10/2026 (`decisions-phase-b.md`), reprise telle quelle.
#  - `dt028` Pay It Forward : meme squelette.
#
# ⚠ Mots-pieges :
#  - « Take X damage → » : X est choisi par le joueur (0 a 4). C'est un COUT : RR Cost, « that cost is not considered paid
#    unless ALL of that damage was taken » (arbitrage du 26/10/2026). Toute prevention, meme partielle (Tough, Jessica's
#    Jacket...), annule l'effet en entier ; le degat deja subi reste subi. Ce n'est plus la lecture « X reel » de Majime.
#    X = 0 : aucun effet.
#  - « to a maximum of 4 » : borne le choix de X.
#  - « remove X threat from A scheme ... AND deal X damage to AN enemy » : une manigance et un ennemi au choix, effets
#    independants (s'il n'y a pas de menace, les degats partent quand meme).
#  - Libelle `(attack/thwart)` : alimente Sonne ET Desoriente.


def GetAbilities() -> Sequence['Ability']:

    def reckless(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)

        initiator = effect.GetInitiator()
        if initiator is None or not initiator.IsHero():
            return
        heros = initiator.GetHero()

        declare = initiator.DeclareNumber(0, 4)
        if declare <= 0:
            return
        subi = heros.TakeDamage(this, declare, effect)
        # RR Cost : « If taking damage is a cost, that cost is not considered paid unless all of that damage was taken
        # (if any of the damage is prevented, then the cost has not been paid) » : une prevention PARTIELLE annule
        # l'effet en entier (arbitrage du 26/10/2026), elle ne le reduit pas a X reel.
        if subi is None or subi.took_damage < declare:
            return
        x = declare

        manigances = [s for s in Worlds.GetOnAllFieldScheme(effect) if s.threat > 0]
        if manigances:
            manigance = initiator.AskChooseFace(
                manigances, effect, prompt=f"Remove {x} threat from a scheme")
            this.RemoveThreatFromSchemes([manigance or manigances[0]], x, effect)

        ennemis = [e for e in Worlds.FindCardsOnField(effect, card_type=Enemy)
                   if not e.IsDefeated()]
        if ennemis:
            ennemi = initiator.AskChooseFace(
                ennemis, effect, prompt=f"Deal {x} damage to an enemy")
            this.DealDamage([ennemi or ennemis[0]], x, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            reckless,
        ).SetPlay().SetLabel('attack', 'thwart'),
    ]
