from .commun import *
from cards.pack.mts.the_tower_defense import DealDamageToAvengersTower

# Angry Birds (defi 4, p282, ID 6141) : The Tower Defense (Mad Titan's Shadow). Difficulte 1.
# Heros « Red Birds » (Angel, Falcon, Nova, Rogue, Spectrum, Wonder Man) et « Blue Birds » (Captain Marvel, Doctor Strange, Magneto, Phoenix, Rocket, Star-Lord,
# Storm, Thor, Valkyrie, Vision, War Machine, Wasp) : les Blue Birds commencent avec leur amelioration AERIAL en jeu, mais -2 a la taille de main de la main de depart.
# Regles speciales : « Only AERIAL & identity specific allies » (restriction de deck : non verifiee par le moteur, comme `UsingOnlyHeroes`) ;
# « All allies gain: Action: Discard this ally -> deal 1 damage to Avenger's Tower and 4 damage to the villain. »
#
# Cartes de reference : pack challenges/2414_symbiote_smackdown (une carte mise en jeu a la mise en place), hunting_season/campaign.py `CarteDeDepartEnPlus`
# (main de depart modifiee le temps de la pioche : `WhenCampaignSetup` -> `WhenCampaignSetupAfterMulligans`), leonardo/tl011 (`given_abilities` : aptitude OCTROYEE
# a chaque allie), nebu/22014 (`CostFunc.Discard("This")`), mts/the_tower_defense (`DealDamageToAvengersTower`).
# Decisions de l'utilisateur (22/10/2026) : (1) l'AERIAL des Blue Birds est une amelioration AERIAL DE LEUR DECK (rien si le deck n'en a pas) ; (2) « the villain » =
# le vilain ACTIF (The Tower Defense a deux vilains, un seul actif) ; si la Tour n'est pas en jeu, son 1 degat est perdu.
# Decision de portage (RR muette) : « -2 hand size for their opening hand » = deux cartes de MOINS piochees a la mise en place (la taille de main redevient normale ensuite).

BLUE_BIRDS = ("Captain Marvel", "Doctor Strange", "Magneto", "Phoenix", "Rocket Raccoon", "Star-Lord", "Storm", "Thor", "Valkyrie", "Vision", "War Machine", "Wasp")
CLE_MAIN = '_defi_birds_main_'


def GetAbilities() -> Sequence['Ability']:

    def oiseaux_bleus(effect: 'Effect') -> List['Player']:
        return [joueur for joueur in Worlds.GetPlayers(effect) if joueur.IsName(*BLUE_BIRDS)]

    def depart(effect: 'Effect', message: 'Message.WhenCampaignSetup') -> None:
        for joueur in oiseaux_bleus(effect):
            amelioration = Search.PlayerCard(effect, joueur, include_player_deck=True, card_type=Upgrade, trait="AERIAL")
            if amelioration:
                amelioration.PutIntoPlay(joueur, effect)
            joueur.GetIdentity().Gain(effect, -2, hand_size=1)
            Stores.SetStr(f'{CLE_MAIN}{joueur.player_id}', '1', effect)

    def rendre_la_main(effect: 'Effect', message: 'Message.WhenCampaignSetupAfterMulligans') -> None:
        for joueur in Worlds.GetPlayers(effect):
            cle = f'{CLE_MAIN}{joueur.player_id}'
            if Stores.HasKey(cle, effect) and Stores.GetStr(cle, effect) == '1':
                joueur.GetIdentity().Gain(effect, 2, hand_size=1)
                Stores.SetStr(cle, '0', effect)

    def lancer_l_oiseau(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        DealDamageToAvengersTower(1, effect)
        for vilain in Worlds.GetVillains(effect):
            if vilain.IsActive():
                effect.this.DealDamage([vilain], 4, effect)
                break

    aptitude_donnee = AbilityFactory.WhenInYourPlayTurn(AbilityType.Action, lancer_l_oiseau).SetCostFunc(CostFunc.Discard("This"))

    return [
        Ability(AbilityType.Challenge, Message.WhenCampaignSetup, [], depart),
        Ability(AbilityType.Challenge, Message.WhenCampaignSetupAfterMulligans, [], rendre_la_main),
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(Ally, given_abilities=[aptitude_donnee]),
    ]
