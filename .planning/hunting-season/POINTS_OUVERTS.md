# Points ouverts

1. **Décision utilisateur en attente : Swarmed by Rats, hs018/hs019.**
   Le texte imprime `Interrupt: After you defeat a RAT minion engaged with you,
   discard two cards from your hand → discard this card.` La carte hs018 a été
   montrée à l'utilisateur, qui n'a pas encore choisi entre garder l'ambiguïté
   imprimée et traiter le déclencheur comme Response. Conserver le texte et
   demander une décision avant de coder cette capacité. Le gain guard aux RAT
   engagés est un effet distinct qui peut être intégré indépendamment.

2. **Scripts partiels.** Chaque script indique son texte imprimé et les effets
   à coder. Le manifeste donne son état. Un GetAbilities vide est une tâche,
   pas une implémentation. Le moteur n'a pas été importé ou simulé ici.

3. **Statistiques dynamiques.** HP=X de Regular Rats/Feral Rats ; ATK+=X de
   Primal Strength ; StartingThreat=X et EscalationThreat=X de hs058b ; SCH=*
   et ATK=* de The Chameleon hs077. Vérifier le parseur réel et utiliser la
   convention native. Ne pas convertir aveuglément * en valeur par joueur.
   Les valeurs de ce brouillon ne doivent pas arriver au chargeur sans adaptation.

4. **DEF+ d'attachement.** Coiled Up et Quicksand impriment -1 ATK/THW/DEF.
   DEF+ n'est pas listé dans le tableau du kit. Employer soit le support natif
   confirmé, soit une capacité continue ; jamais les deux, ce qui doublerait
   le malus. Hunterbot donne +1 ATK au héros uniquement ; vérifier la forme.

5. **Stock, XP et interface.** Le schéma de campagne fourni ne permet pas de
   représenter complètement marché partagé, transactions, Master Hunter,
   propriétaire des récompenses, pénalités de défaite et achats de mise en
   place. Le contrat et les calculs purs sont fournis pour une implémentation
   explicite dans le dépôt. Les clés d'installation ne sont pas ajoutées comme
   champs inventés dans le JSON natif. L'interface victoire seule ne suffit pas.

6. **Fin de partie et snapshot.** Préserver le stade du complot, les RAT engagés,
   le nombre de REPTILE attachments du vilain, les blessures de Jameson,
   l'état mis de côté de la queue, les PV réels/max/base et les PREDATOR possédés
   avant les mouvements de nettoyage. Les calculs n'utilisent pas un état
   reconstitué après suppression du dernier stade du vilain.

7. **Détection du scénario.** WriteCampaignLogAtGameOver vient de mts selon le
   kit. Vérifier sa signature et sa détection d'ID : les scénarios ici s'appellent
   hs_vermin, hs_scorpion, etc., pas seulement le clean(set_name). Ne pas inventer
   un argument scenario_id s'il n'est pas réellement supporté.

8. **Progression après défaite.** Le texte général p.2 dit de gagner les cinq
   scénarios ; les règles spécifiques de défaites 1 à 4 prescrivent gains,
   visite du Lodge et passage au suivant. Le calcul suit ces prescriptions
   spécifiques et réserve la fin de campagne au résultat de Kraven. Ce choix
   d'interprétation est explicite ; ne pas lui substituer un verrou victoire
   générique sans résoudre la contradiction des sources.

9. **Libellés imprimés incohérents.** La mise en place Scorpion dit upgrade pour
   sa queue alors que son bandeau est Attachment ; Vulture 1A dit Wing Suits
   alors que le titre est Wingsuits ; le livret écrit Cold-Blooded. Utiliser ID
   et type effectifs pour les recherches, en gardant le texte source intact.

10. **Texte exact et images.** Les règles de gameplay ont été transcrites ; les
    phrases d'ambiance et les rappels non mécaniques ne sont pas complets dans
    le JSON. Les 239 scans de référence permettent de les compléter. Les JPEG
    sont des références de lecture réduites, pas des masters d'impression.
    L'OCR brut peut confondre symboles, chiffres, rotation et ponctuation.

11. **Jeu réel.** Le préfixe, la fusion cards.json, les noms de dossier, les
    clones, les ressources, les compteurs et les timing windows doivent être
    contrôlés avec le dépôt. La vérification jointe est statique et n'est pas
    une preuve que les scripts chargent ou que les scénarios se jouent.
