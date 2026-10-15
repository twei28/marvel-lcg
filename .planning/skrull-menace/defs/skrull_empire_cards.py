# Entrees cards.json du scenario Skrull Empire + sets Army of Skrulls / Skrull Society.
# card_id = sk + numero IMPRIME en pied de carte (« MC Custom Content By Kajislav <n> »).
SE = "Skrull Empire"; AR = "Army of Skrulls"; SO = "Skrull Society"
def c(cid, typ, name, desc, traits, text, set_name):
    return {"card_id": cid, "type": typ, "name": name, "subtitle": "", "desc": desc,
            "traits": traits, "set_name": set_name, "text": text, "custom": "Kajislav"}
V=[]
def villain(base, name, stats, texte):
    for i,(atk,sch,extra) in enumerate(stats):
        d={"HP":"INF","ATK":atk,"SCH":sch,"Stage":str(i+1)}; d.update(extra)
        V.append(c(f"sk{base+i:03d}","Villain","* "+name,d,["SKRULL"],texte(i),SE))
villain(70,"Emperor Dorrek I",[("1*","2",{"Retaliate":"1"}),("2*","2",{"Retaliate":"1"}),("2*","3",{"Retaliate":"2"})],
  lambda i: f"Retaliate {[1,1,2][i]}.\n[star] Emperor Dorrek I's attacks gain ranged.\n<i>(This villain has no hit point dial: see the Skrull Empire environment.)</i>")
villain(73,"Emperor Dorrek VII",[("2*","1",{}),("3*","1",{}),("4*","2",{})],
  lambda i: "Incite 1[per_hero].\n[star] Emperor Dorrek VII's attacks gain overkill.\n<i>(This villain has no hit point dial: see the Skrull Empire environment.)</i>")
villain(76,"Empress R'Klll",[("1*","2",{}),("1*","3",{}),("2*","4",{})],
  lambda i: "<b>When Revealed</b>: Empress R'Klll attacks each player in hero form.\n[star] Empress R'Klll's attacks gain piercing.\n<i>(This villain has no hit point dial: see the Skrull Empire environment.)</i>")
villain(79,"Empress S'Byll",[("2","2",{"Steady":"1","Toughness":"1"}),("3","2",{"Steady":"1","Toughness":"1"}),("3","3",{"Stalwart":"1","Toughness":"1"})],
  lambda i: ("Stalwart. Toughness." if i==2 else "Steady. Toughness.")+"\n<i>(This villain has no hit point dial: see the Skrull Empire environment.)</i>")
MS=[
 c("sk082a","MainScheme","Rise of the Skrull Empire",{"Stage":"1"},[],"<b>Contents</b>: All villains (I) and (II) <i>(stages (II) and (III) instead for the expert mode)</i>. Skrull Empire, Skrull Society and Standard sets. One modular set <i>(Army of Skrulls)</i>.\n<b>Setup</b>: Create the [[PLANET]] and the Villain deck <i>(see insert)</i>. Reveal the top card of the Villain deck. Put the Skrull Empire environment (I) into play <i>(stage (II) instead for the expert mode)</i>.",SE),
 c("sk082b","MainScheme","Rise of the Skrull Empire",{"Stage":"1","TargetThreat":"6*","EscalationThreat":"2*","StartingThreat":"0"},[],"<b>When Revealed</b>: Reveal the top card of the [[PLANET]] deck.",SE),
 c("sk083a","MainScheme","Andromeda Galaxy Colonization",{"Stage":"2"},[],"<b>When Revealed</b>: Discard cards from the encounter deck until a [[SKRULL]] minion is discarded. Put that minion into play engaged with the first player.",SE),
 c("sk083b","MainScheme","Andromeda Galaxy Colonization",{"Stage":"2","TargetThreat":"7*","EscalationThreat":"1*","StartingThreat":"2*"},[],"<b>When Revealed</b>: Reveal the top card of the [[PLANET]] deck.",SE),
 c("sk084a","MainScheme","Further Empire Expansion",{"Stage":"3"},[],"<b>When Revealed</b>: Discard cards from the encounter deck until a [[SKRULL]] minion is discarded. Put that minion into play engaged with the first player.",SE),
 c("sk084b","MainScheme","Further Empire Expansion",{"Stage":"3","TargetThreat":"5*","EscalationThreat":"1*","StartingThreat":"0"},[],"<b>When Revealed</b>: Reveal the top card of the [[PLANET]] deck.",SE),
 c("sk085a","MainScheme","Entire Universe Domination",{"Stage":"4"},[],"<b>When Revealed</b>: Discard cards from the encounter deck until a [[SKRULL]] minion is discarded. Put that minion into play engaged with the first player.",SE),
 c("sk085b","MainScheme","Entire Universe Domination",{"Stage":"4","TargetThreat":"9*","EscalationThreat":"2*","StartingThreat":"1*"},[],"<b>When Revealed</b>: Reveal the top card of the [[PLANET]] deck.\n<b>If this stage is completed, the players lose the game.</b>",SE),
]
REB="<i>Incite Rebellion</i> — <b>Hero Action</b>: Choose to either exhaust your hero or spend 2 resources of any type → choose 1 [[PLANET]] environment in play. Treat its printed text box as if it were blank until the end of the round. <i>(Limit once per round per player.)</i>"
ENV=[
 c("sk086","Environment","Skrull Empire",{"Stage":"1"},[],"Hit points 14[per_hero].\n"+REB,SE),
 c("sk087","Environment","Skrull Empire",{"Stage":"2"},[],"Hit points 18[per_hero].\n<b>When Revealed</b>: Shuffle each set-aside Overthrow card into the encounter deck.\n"+REB,SE),
 c("sk088","Environment","Skrull Empire",{"Stage":"3"},[],"Hit points 22[per_hero].\n<b>When Revealed</b>: Shuffle each set-aside Overthrow card into the encounter deck.\n"+REB,SE),
]
P=[("sk089","Aks'Lo","Each [[SKRULL]] minion gets +2 hit points."),("sk090","Hy'lt Minor","Each identity gets -1 REC."),
   ("sk091","Satriani","Each [[SKRULL]] minion gains guard."),("sk092","Skrell","Each [[SKRULL]] minion gets +1 SCH."),
   ("sk093","Skrullos","Each side scheme gains the crisis icon ([crisis])."),("sk094","Tarnax II","Decrease the target threat value of the main scheme by 1[per_hero]."),
   ("sk095","Tarnax IV","While a side scheme is in play, this card gains the amplify icon ([amplify])."),("sk096","Tarnax VII","Each [[SKRULL]] minion gets +1 ATK."),
   ("sk097","Zaragz'na","Each ally and support enters play exhausted.")]
PL=[c(i,"Environment",n,{},["LOCATION","PLANET"],t,SE) for i,n,t in P]
ENC=[
 c("sk098","Attachment","Impostor",{"Boost":"1"},["CONDITION"],"Treat attached ally as a [[SKRULL]] minion with a blank text box. Attached minion's SCH is equal to its printed THW and it does not take consequential damage.\n<b>When Revealed</b>: Attach to the non-[[SKRULL]] ally with the most remaining hit points without Impostor attached. Attached ally engages its controller. Otherwise, the villain schemes.",SE),
 c("sk099","Minion","* Intelligentsia",{"HP":"5","SCH":"2","ATK":"0*","Acceleration":"1","Boost":"2"},["SKRULL"],"Each other [[SKRULL]] enemy gets +1 SCH.\n[star] <b>Forced Interrupt</b>: When Intelligentsia would attack, she schemes instead.",SE),
 c("sk100","SideScheme","Emperor's Throne",{"StartingThreat":"2*","Acceleration":"1","Hazard":"1","Boost":"3"},[],"<b>When Defeated</b>: The villain attacks the player who defeated this scheme <i>(even if that player is in alter-ego form)</i>. Give the villain 1 additional boost card for this activation.",SE),
 c("sk101","SideScheme","Seeking a Suitable World",{"StartingThreat":"3*","Incite":"2","Acceleration":"1"},[],"Incite 2.",SE),
 c("sk102","Treachery","A New Skrull Is Born",{"Boost":"1"},[],"<b>When Revealed</b>: Discard cards from the encounter deck until you discard a [[SKRULL]] minion and reveal it.",SE),
 c("sk103","Treachery","Giving Orders",{"Boost":"1"},[],"<b>When Revealed</b>: Each [[SKRULL]] minion activates against the player it is engaged with. If no minion activated this way, this card gains surge.",SE),
 c("sk104","Treachery","Long Live the Empire",{"Boost":"1"},[],"<b>When Revealed</b>: Heal 2 damage from the villain for each [[SKRULL]] enemy in play. If no damage was healed this way, this card gains surge.\n[star] <b>Boost</b>: Heal 1 damage from the villain for each [[SKRULL]] enemy in play.",SE),
 c("sk105","Treachery","Overthrow",{},[],"<b>When Revealed</b>: Remove the current villain from the game and reveal the top card of the villain deck. Then, set Overthrow aside, out of play.\n[star] <b>Boost</b>: Deal this card to yourself as a facedown encounter card.",SE),
 c("sk106","Treachery","Wrath of the Empire",{},[],"<b>When Revealed</b>: Discard the top 2 cards of the encounter deck for each [[PLANET]] environment in play. Place 1 acceleration token on the main scheme, if a card with the acceleration icon ([acceleration]) was discarded this way.\n[star] <b>Boost</b>: This card gets +1 boost icon ([boost]) for each [[PLANET]] environment in play.",SE),
]
MOD=[
 c("sk107","Minion","Skrull Scientist",{"HP":"3","SCH":"3","ATK":"0","Acceleration":"1","Boost":"2"},["GENIUS","SKRULL"],"[star] <b>Boost</b>: Heal 2 damage from the villain, after this activation ends.",SO),
 c("sk108","Minion","Skrull Spy",{"HP":"4","SCH":"2","ATK":"1"},["SKRULL","SPY"],"<b>When Revealed</b>: Discard 1 random card from your hand.\n[star] <b>Boost</b>: Discard 1 random card from your hand.",SO),
 c("sk109","Minion","Skrull Telepath",{"HP":"3","SCH":"2","ATK":"0*"},["PSIONIC","SKRULL"],"[star] <b>Forced Interrupt</b>: When Skrull Telepath would attack, it schemes instead.\n[star] <b>Boost</b>: If this activation is a scheme, reveal this card.",SO),
 c("sk110","Minion","Skrull Warrior",{"HP":"4","SCH":"2","ATK":"2","Guard":"1","Boost":"1"},["SKRULL"],"Guard. <i>(While this minion is engaged with you, you cannot attack the villain.)</i>\n[star] <b>Boost</b>: If this attack is undefended, you are stunned.",SO),
 c("sk111","SideScheme","Plotting Revenge",{"StartingThreat":"2","Hinder":"2*","Acceleration":"1","Boost":"2"},[],"<i>The Skrulls thoroughly studied human behavior in order to achieve their goal of conquering Earth and completely dominating the universe.</i>\nHinder 2[per_hero].",SO),
 c("sk112","Treachery","Outnumbered",{},[],"<b>When Revealed</b>: Engage each [[SKRULL]] minion in play. Then, search the encounter deck and discard pile for a [[SKRULL]] minion and reveal it.\n[star] <b>Boost</b>: This card gets +1 boost icon ([boost]) for each [[SKRULL]] enemy in play <i>(to a maximum of +4)</i> for this activation.",SO),
 c("sk113","Minion","Skrull Commander",{"HP":"5","SCH":"2","ATK":"2","Boost":"1"},["SKRULL","SOLDIER"],"Each other [[SKRULL]] minion gets +1 ATK.\n[star] <b>Boost</b>: If this activation is an attack, this card gets +2 boost icons ([boost][boost]) for this activation.",AR),
 c("sk114","Minion","Skrull Soldier",{"HP":"4","SCH":"2","ATK":"2","Boost":"1"},["SKRULL","SOLDIER"],"<b>When Revealed</b>: Place 2 threat on each side scheme in play.\n[star] <b>Boost</b>: Discard the top 2 cards of your deck.",AR),
 c("sk115","SideScheme","Hijacked",{"StartingThreat":"4","Hinder":"1*","Crisis":"1"},[],"Hinder 1[per_hero].\n<b>When Revealed</b>: Search your deck, discard pile and hand for an ally and place it beneath this scheme.\n<b>When Defeated</b>: Put the ally beneath this scheme into play under its owner's control.\n[star] <b>Boost</b>: Reveal this card.",AR),
 c("sk116","Treachery","Skrull Assault",{},[],"<b>When Revealed</b>: Each [[SKRULL]] minion attacks the hero it is engaged with. If no attacks were made this way, this card gains surge.\n[star] <b>Boost</b>: This card gets +1 boost icon ([boost]) for each [[SKRULL]] enemy in play <i>(to a maximum of +4)</i> for this activation.",AR),
]
CARDS = V+MS+ENV+PL+ENC+MOD
