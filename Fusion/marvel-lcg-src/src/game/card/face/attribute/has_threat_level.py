from . import *

class HasThreatLevel(HasAttribute):
    @override
    def __init__(self, paper: 'Paper') -> None:
        """Le mot-cle « Threat Level X » du set fan-made The Spot.

        C'est un NOMBRE, pas un effet : il ne fait rien par lui-meme. Le chiffre
        vit dans une icone rouge sur la carte, et les autres cartes du set s'en
        servent pour se comparer entre elles — « move that threat to the card
        with the highest Threat Level instead ».

        Il se modele sur `Hinder`, l'autre mot-cle chiffre du jeu, a une
        difference pres : `Hinder` POSE des jetons quand la carte entre en jeu,
        celui-ci ne pose rien. D'ou `HasAttribute` seul, sans `CanPlaceToken`.
        """
        self.printed_threat_level = 0

        super().__init__(paper)

        self.RegisterAttribute("ThreatLevel", "printed_threat_level")
        self.RegisterInfoDict('threat_level')

    ################################################################################
    #
    @override
    def CheckPrintedValue(self):
        assert self.printed_threat_level >= 0
        return super().CheckPrintedValue()

    @override
    def OnResetKeywords(self, by_effect: 'Effect'):
        self.GainThreatLevel(self.printed_threat_level, by_effect)
        return super().OnResetKeywords(by_effect)

    @final
    def HasThreatLevelKeyword(self) -> bool:
        """« a Spot card with the Threat Level keyword » : PORTER le mot-cle et
        avoir un niveau de zero sont deux choses differentes. Le texte cible les
        cartes qui le portent, quelle que soit leur valeur."""
        return self.printed_threat_level > 0 or self.threat_level > 0

    @final
    @property
    def threat_level(self) -> int:
        return self.GetKeyword('ThreatLevel')

    @final
    def GainThreatLevel(self, diff: int, by_effect: 'Effect'):
        self.GainKeyword(diff, 'ThreatLevel', by_effect)
