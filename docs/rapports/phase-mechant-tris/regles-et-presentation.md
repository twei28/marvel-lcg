# Tris — règles et présentation, 19 octobre 2026

Référence consultée : [Rules Reference 1.8 officielle](https://cdn.svc.asmodee.net/production-fantasyflightgames/uploads/2026/08/mc_rulesreference_v18_compressed-1.pdf), annoncée par [Mission Updates](https://www.fantasyflightgames.com/mission-updates/). Sections : Villain Phase, Attack (Enemy Activation), Scheme (Enemy Activation), Boost, Reveal et Surge.

## Ordre à conserver

1. Menace sur la manigance principale, accélérations comprises.
2. Dans l'ordre des joueurs : activation du méchant contre ce joueur, puis activation des sbires engagés avec lui dans l'ordre choisi par ce joueur. Héros : attaque ; alter ego : manigance, sauf texte de carte.
3. Distribution des rencontres et cartes supplémentaires des icônes de danger, dans l'ordre des joueurs.
4. Révélation des rencontres une par une, dans leur ordre de distribution, jusqu'à ce qu'aucune carte distribuée ne reste. En 1.8, Renfort distribue une carte face cachée en fin de file ; il ne signifie pas une révélation immédiate hors phase du méchant.
5. Transmission du premier joueur, fin de phase et de round, effets de fin compris.

Attaque : carte boost distribuée face cachée, défense déclarée, boosts retournés un par un dans leur ordre de distribution, effet Boost ★ de chacun, icônes ajoutées, calcul des dégâts, dégâts, capacités de fin d'attaque selon leurs fenêtres. La version 1.8 distingue explicitement le calcul des dégâts de leur application. Un sbire n'a pas de boost par défaut ; Criminel ou un texte de carte peut lui en donner.

Manigance : pas de déclaration de défense ; boosts retournés et effets ★ résolus, puis menace sur la principale selon la MAN modifiée.

Une ★ n'est pas une icône numérique. Seul le texte Boost est actif sur la carte utilisée comme boost, pas son effet Une fois révélée. Un effet immédiat se résout au retournement ; un effet conditionnel après l'attaque attend son déclencheur. Un effet immédiat peut modifier le résultat de l'activation : le déplacer systématiquement après les dégâts changerait les règles.

## Changements limités à tris

- Avec plusieurs boosts : lecture d’une grande carte à la fois, puis page de synthèse avec les cartes côte à côte et le résultat. Aucun clic de lecture ne valide l’activation. La hauteur des cartes s’adapte à la fenêtre ; le survol conserve l’aperçu agrandi habituel.
- Révélation au clic, un boost à la fois ; les cartes non retournées restent face cachée dans le guide. Aucun résultat présenté avant le dernier boost.
- Les effets immédiats sont indiqués avec leur boost. Le texte d'un effet différé n'est pas rejoué sur le résultat : l'étape `etoile-differe` existante le présente après l'activation. Si sa condition de dégâts échoue, l'étape de résultat le signale selon le modèle existant.
- Les couleurs réutilisent les rôles du plateau : information pour progression et cadre, attaque pour ATQ/dégâts, manigance pour MAN, menace pour la pose de menace, défense pour le choix défensif. Les boutons de continuation conservent le thème du plateau.

## Vérifications et limites

393 tests ciblés : cartouche, modèle de vue, déroulé, frise et effets différés. Les contrôles Chromium et le déploiement local sont exécutés séparément. Les aperçus de géométrie utilisent des scénarios rendus par les tests, sans scans réels.

Cette reprise ne remplace pas le moteur et ne certifie pas toutes les interactions de toutes les cartes. Les variantes historiques de règles des sauvegardes restent respectées ; aucune migration forcée des parties existantes. Notamment, les fenêtres complexes où plusieurs capacités forcées ont le même déclencheur relèvent de l'ordonnancement du moteur, pas d'une réorganisation des pages du guide.
