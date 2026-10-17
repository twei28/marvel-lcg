import html, json, os, re, shutil, subprocess

S = "/tmp/claude-29999/-home-oem-Desktop-Marvel-LCG/a5be412e-8d1d-4d37-b2dd-0f21cdb838dc/scratchpad"
OUT = "/home/oem/Desktop/Marvel LCG/docs/rapports/phase-mechant-sur-la-table"
FF = os.path.expanduser("~/.cache/ms-playwright/ffmpeg-1011/ffmpeg-linux")
os.makedirs(OUT + "/videos", exist_ok=True)
os.makedirs(OUT + "/images", exist_ok=True)

# nom, titre, ce que ce cas montre
CAS = [
    ("rhino-base", "Rhino, héros en alter ego (2 phases)", "La phase la plus simple : la menace arrive, Rhino manigance, puis les cartes rencontre se révèlent, avec des Renforts en chaîne."),
    ("rhino-annexe", "Rhino + manigance annexe + 2 sbires", "Les sbires manigancent à tour de rôle ; on choisit l'ordre ; la distribution des cartes rencontre."),
    ("rhino-sbires", "Rhino + 3 sbires, héros en forme héros", "Attaque du méchant, Sens d'Araignée, ordre d'activation de 3 sbires, défense, et la défaite du héros."),
    ("wrecking-crew", "The Wrecking Crew (plusieurs méchants)", "Chaque membre du gang attaque à son tour ; Renfort ; la défaite."),
    ("nebula", "Nebula (environnement et statut)", "Manigance de 2 menaces, statut Sonné, révélation d'une carte, puis 2e phase avec une manigance qui gagne 4 menaces."),
    ("ultron", "Ultron (drones, manigance annexe)", "Ultron avec ses drones et la manigance annexe Drone Factory."),
    ("klaw", "Klaw + 2 gardes", "Deux phases complètes avec des sbires, des attaques et des réponses du héros."),
    ("sinister-six", "Sinister Six (équipe de méchants)", "Plusieurs méchants et sbires qui s'activent en série, sur 2 phases."),
]

# (clé, titre, explication, regex sur le texte de l'étape)
TYPES = [
    ("menace", "La menace arrive", "Au début de la phase, la manigance principale gagne de la menace. La carte qui agit a un halo doré ; on clique dessus (ou Espace) pour passer à la suite.", r"gagne \d+ menaces?(?! sur)"),
    ("manigance-annonce", "Le méchant va manigancer", "Le bandeau annonce la manigance AVANT qu'elle ait lieu, avec le nombre de menaces.", r"va manigancer"),
    ("manigance", "La manigance a lieu", "La menace est posée sur la manigance ; le jeton vole jusqu'à elle.", r"manigance sur"),
    ("attaque-annonce", "Le méchant va attaquer", "L'attaque est annoncée avec ses dégâts : le joueur voit qui est visé avant de décider de défendre.", r"va attaquer"),
    ("interruption", "Une réponse du héros (ex. Sens d'Araignée)", "Quand une carte permet d'interrompre l'attaque, le jeu pose la question ; « Ne pas utiliser » passe son tour.", r"Ne pas utiliser"),
    ("defense", "Qui défend ?", "Le joueur choisit le défenseur, ou « Ne pas défendre » (ATQ affichée).", r"Qui défend"),
    ("attaque", "L'attaque est résolue", "Les dégâts sont infligés ; le jeton de dégâts vole jusqu'à la carte touchée.", r"attaque .* \d+ dégâts?"),
    ("riposte", "Riposte", "Un allié ou un héros qui riposte inflige ses dégâts en retour.", r"Riposte"),
    ("statut", "Un statut est donné (Sonné, Désorienté…)", "Le bandeau dit quel statut est posé et sur qui.", r"gagne (Sonn|Désorient)"),
    ("ordre", "Ordre d'activation des sbires", "Avec plusieurs sbires, le joueur choisit l'ordre en cliquant les cartes vertes : 1/3, 2/3, 3/3, puis Valider.", r"Ordre d.activation"),
    ("revele", "Une carte rencontre est révélée", "La carte sort du paquet, grande, au milieu ; le bandeau dit qui la révèle.", r"révèle"),
    ("renfort", "Renfort (surge)", "Une carte avec Renfort en fait révéler une autre ; le bandeau l'écrit en clair.", r"Renfort"),
    ("distribution", "Distribution des cartes rencontre", "En multijoueur, chaque joueur reçoit sa carte avant la révélation.", r"distribution"),
    ("defaite", "Le héros est vaincu", "La phase s'arrête et le bandeau le dit ; « Continuer » mène à l'écran de fin.", r"vaincu|☠"),
    ("fin", "Fin de la phase", "Le bilan : menaces gagnées en tout, et « Terminer la phase ».", r"Fin de la phase|Terminer la phase"),
]


def nettoyer(t):
    t = (t or "").replace("‹", "").replace("Clique la carte dorée, ou Espace", "").strip()
    return re.sub(r"\s+", " ", t)


donnees = {}
for nom, titre, doc in CAS:
    jf = f"{S}/capt/table/{nom}/journal.jsonl"
    vids = [os.path.join(r, f) for r, _, fs in os.walk(f"{S}/pw-out/{nom}") for f in fs if f == "video.webm"]
    if not os.path.exists(jf) or not vids:
        print("ABSENT", nom)
        continue
    pas = []
    for l in open(jf):
        d = json.loads(l)
        if d.get("rang") is None or d.get("fin") or "t" not in d:
            continue
        texte = nettoyer(d.get("cartouche"))
        if texte:
            pas.append({"t": d["t"] / 1000.0, "texte": texte, "phase": d.get("phase")})
    if not pas:
        print("VIDE", nom)
        continue
    debut = max(0.0, pas[0]["t"] - 4.0)
    fin = pas[-1]["t"] + 3.0
    sortie = f"{OUT}/videos/{nom}.webm"
    subprocess.run([FF, "-hide_banner", "-loglevel", "error", "-y", "-ss", f"{debut:.2f}", "-t", f"{fin - debut:.2f}",
                    "-i", vids[0], "-c:v", "libvpx", "-b:v", "230k", "-crf", "34", "-an", sortie], check=True)
    for p in pas:
        p["t"] = round(p["t"] - debut, 2)
    donnees[nom] = {"titre": titre, "doc": doc, "pas": pas, "taille": os.path.getsize(sortie)}
    print(nom, len(pas), "étapes", round(donnees[nom]["taille"] / 1e6, 1), "Mo")

# catalogue : premier exemple de chaque type
exemples = {}
for cle, tt, expl, rx in TYPES:
    for nom, d in donnees.items():
        for i, p in enumerate(d["pas"]):
            if re.search(rx, p["texte"]):
                exemples.setdefault(cle, (nom, p))
                break
        if cle in exemples:
            break

bloque = f"{S}/bloque/bebop-forcees.png"
if os.path.exists(bloque):
    shutil.copy(bloque, OUT + "/images/bebop-capacites-forcees.png")


def seg(nom, t, avant=2.5, duree=7.0):
    deb = max(0.0, t - avant)
    return (f'<video class="seg" muted playsinline loop preload="metadata" src="videos/{nom}.webm" '
            f'data-start="{deb:.2f}" data-end="{deb + duree:.2f}"></video>')


e = html.escape
parties = []
parties.append("""<!doctype html>
<html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Phase du méchant · Sur la table</title>
<style>
:root{--fond:#0e1116;--carte:#171c24;--bord:#2a3240;--texte:#e8ecf2;--doux:#9aa6b6;--rouge:#e23a3a;--or:#f0b95f;--bleu:#6bb6ff}
*{box-sizing:border-box}
body{margin:0;background:var(--fond);color:var(--texte);font:16px/1.55 system-ui,-apple-system,Segoe UI,Roboto,sans-serif}
header{padding:32px 16px 8px;max-width:1100px;margin:auto}
h1{font-size:30px;margin:0 0 6px}
h2{font-size:22px;margin:40px 0 12px;padding-top:8px;border-top:2px solid var(--rouge)}
h3{font-size:17px;margin:0 0 4px}
main{max-width:1100px;margin:auto;padding:0 16px 80px}
p{color:var(--doux);margin:6px 0 12px}
nav{position:sticky;top:0;background:rgba(14,17,22,.95);backdrop-filter:blur(6px);border-bottom:1px solid var(--bord);z-index:5}
nav div{max-width:1100px;margin:auto;padding:8px 16px;display:flex;gap:6px;flex-wrap:wrap}
nav a{color:var(--texte);text-decoration:none;font-size:13px;border:1px solid var(--bord);border-radius:99px;padding:3px 10px}
nav a:hover{border-color:var(--rouge)}
.grille{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:14px}
.carte{background:var(--carte);border:1px solid var(--bord);border-radius:10px;overflow:hidden}
.carte .t{padding:10px 12px}
video{width:100%;display:block;background:#000;aspect-ratio:16/9}
.seg{cursor:pointer}
.etiq{display:inline-block;font-size:12px;color:var(--or);border:1px solid var(--bord);border-radius:99px;padding:0 8px;margin-top:4px}
.cas{background:var(--carte);border:1px solid var(--bord);border-radius:12px;padding:14px;margin:16px 0}
.cas .corps{display:grid;grid-template-columns:minmax(0,3fr) minmax(0,2fr);gap:14px}
@media(max-width:820px){.cas .corps{grid-template-columns:1fr}}
ol.pas{list-style:none;margin:0;padding:0;max-height:430px;overflow:auto;border:1px solid var(--bord);border-radius:8px}
ol.pas li button{all:unset;display:block;width:100%;box-sizing:border-box;padding:6px 10px;cursor:pointer;font-size:14px;border-bottom:1px solid var(--bord)}
ol.pas li button:hover,ol.pas li button.on{background:#222b38}
ol.pas small{color:var(--doux);margin-right:6px}
.ok{border-left:4px solid #3fb950}.ko{border-left:4px solid var(--rouge)}.nb{border-left:4px solid var(--or)}
.note{background:var(--carte);border:1px solid var(--bord);border-radius:8px;padding:10px 14px;margin:10px 0}
img{max-width:100%;border-radius:8px;border:1px solid var(--bord)}
code{background:#222b38;padding:1px 5px;border-radius:4px;font-size:.92em}
.etapes{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:10px;margin:12px 0}
.etapes div{background:var(--carte);border:1px solid var(--bord);border-top:3px solid var(--rouge);border-radius:8px;padding:10px}
.etapes b{color:var(--or)}
</style></head><body>
<header><h1>La phase du méchant, « Sur la table »</h1>
<p>Capturée en jouant de vraies parties le 17/10/2026 : 8 parties, plusieurs méchants, une vidéo de chacune. Rien n'est un montage.</p></header>
<nav><div><a href="#etapes">Les 5 étapes</a><a href="#catalogue">Tout ce qui peut arriver</a><a href="#parties">Les parties</a><a href="#points">À vérifier</a></div></nav>
<main>
<section id="etapes"><h2>Comment se déroule une phase</h2>
<p>Aucune fenêtre au milieu du plateau : la carte qui agit brille en doré, une ligne en haut dit ce qui se passe, et on clique la carte dorée (ou Espace) pour passer à la suite. Rien n'avance tout seul.</p>
<div class="etapes">
<div><b>1 · Menace</b><br>La manigance principale gagne sa menace du round.</div>
<div><b>2A · Le méchant</b><br>Il manigance ou attaque. L'attaque ouvre les réponses du héros et le choix du défenseur.</div>
<div><b>2B · Les sbires</b><br>Chaque sbire manigance ou attaque. On choisit l'ordre quand il y en a plusieurs.</div>
<div><b>3 · Cartes rencontre</b><br>Distribution, puis révélation une à une, avec Renforts et boosts.</div>
<div><b>Bilan</b><br>Menaces gagnées, puis « Terminer la phase ». Un héros vaincu l'arrête net.</div>
</div></section>
""")

parties.append('<section id="catalogue"><h2>Tout ce qui peut arriver pendant une phase</h2><p>Chaque case est un extrait tiré d\'une vraie partie (clique pour mettre en pause). Un type qui ne s\'est pas présenté dans mes parties n\'apparaît pas.</p><div class="grille">')
manquants = []
for cle, tt, expl, rx in TYPES:
    if cle not in exemples:
        manquants.append(tt)
        continue
    nom, p = exemples[cle]
    parties.append(f'<div class="carte">{seg(nom, p["t"])}<div class="t"><h3>{e(tt)}</h3><p>{e(expl)}</p>'
                   f'<span class="etiq">{e(donnees[nom]["titre"])}</span></div></div>')
parties.append("</div>")
if manquants:
    parties.append('<div class="note nb"><b>Pas vus dans mes parties :</b> ' + e(", ".join(manquants)) + ".</div>")
parties.append("</section>")

parties.append('<section id="parties"><h2>Les parties, une par une</h2><p>Chaque vidéo est la phase entière. Clique une étape à droite pour y aller.</p>')
for nom, d in donnees.items():
    lis = "".join(
        f'<li><button data-t="{p["t"]}"><small>{int(p["t"]//60)}:{int(p["t"]%60):02d}</small>{e(p["texte"])}</button></li>'
        for p in d["pas"])
    parties.append(f'<div class="cas" id="cas-{nom}"><h3>{e(d["titre"])}</h3><p>{e(d["doc"])}</p>'
                   f'<div class="corps"><video class="pleine" controls muted playsinline preload="metadata" src="videos/{nom}.webm"></video>'
                   f'<ol class="pas">{lis}</ol></div></div>')
parties.append("</section>")

parties.append("""<section id="points"><h2>À vérifier</h2>
<div class="note ko"><b>Nom interne affiché.</b> Dans la partie « Rhino + manigance annexe », une étape du bandeau affiche <code>distribution-tableau</code> au lieu d'un texte lisible, avec un bouton « Continuer ».</div>
<div class="note ko"><b>Mot anglais dans le bandeau.</b> Dans la partie Nebula : « Peter Parker gagne <i>Sonné Stunned</i> ». Le statut est écrit deux fois, en français puis en anglais.</div>
<div class="note ko"><b>Écran sans issue évidente (Bebop et Rocksteady).</b> Avec deux méchants qui ont chacun une capacité forcée en fin de phase, le jeu affiche « Des capacités forcées se déclenchent en même temps → Bebop, Rocksteady ». Mon robot n'a pas su quoi cliquer et la partie est restée là plus d'une minute. Je ne sais pas si un humain trouverait où cliquer : à essayer à la main.<br><img src="images/bebop-capacites-forcees.png" alt="Bebop et Rocksteady : capacités forcées simultanées"></div>
<div class="note nb"><b>Pas couvert par ces parties :</b> les choix des cartes (« Choisis… »), un héros qui défend avec un allié, les environnements qui changent la phase, et le multijoueur (le cas à 2 joueurs est resté bloqué sur une capacité de héros). À jouer à la main pour les voir.</div>
<div class="note"><b>Comment c'est fait.</b> Un robot joue le plateau en mode « Sur la table » (<code>?phase=sur-table</code>) sur un moteur de développement, force quelques situations avec les commandes de test (sbires en jeu, forme héros), et enregistre la vidéo. La version du plateau est celle du 17/10/2026.</div>
</section></main>
<script>
document.querySelectorAll('video.seg').forEach(function(v){
  var a=parseFloat(v.dataset.start),b=parseFloat(v.dataset.end);
  v.addEventListener('loadedmetadata',function(){v.currentTime=a});
  v.addEventListener('timeupdate',function(){if(v.currentTime>=b||v.currentTime<a-0.3){v.currentTime=a}});
  v.addEventListener('click',function(){if(v.paused){v.play()}else{v.pause()}});
  new IntersectionObserver(function(es){es.forEach(function(en){if(en.isIntersecting){v.play().catch(function(){})}else{v.pause()}})},{threshold:.5}).observe(v);
});
document.querySelectorAll('.cas').forEach(function(c){
  var v=c.querySelector('video.pleine');
  c.querySelectorAll('ol.pas button').forEach(function(b){
    b.addEventListener('click',function(){
      v.currentTime=Math.max(0,parseFloat(b.dataset.t)-2.5);v.play().catch(function(){});
      c.querySelectorAll('ol.pas button').forEach(function(x){x.classList.remove('on')});b.classList.add('on');
    });
  });
});
</script></body></html>""")

open(OUT + "/index.html", "w", encoding="utf-8").write("\n".join(parties))
tot = sum(os.path.getsize(os.path.join(OUT, "videos", f)) for f in os.listdir(OUT + "/videos"))
print("HTML ok ; vidéos", round(tot / 1e6, 1), "Mo ; exemples:", sorted(exemples))
