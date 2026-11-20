"""L'ecran de connexion du site (la page que voit quelqu'un de deconnecte).

Refonte du 18/11/2026, demande de l'utilisateur : l'ancien formulaire seul etait « moche, amateur, pas raccord avec le jeu ».
Cet ecran reprend le langage du jeu (fond sombre, bleu #3f86e0, coins coupes en biseau, titres Bangers) et porte :
  - un EN-TETE (logo, liens publics, bascule FR/EN, bouton « Se connecter ») ;
  - DEUX cartes cote a cote : « J'ai un compte » (le formulaire) et « Je n'ai pas de compte » (jouer sans compte) ;
  - une BANDE du bas qui fait defiler, une a la fois, des anecdotes de comics sur les heros du jeu et des conseils
    (contenu dans `infos_accueil.py`, FR et EN, avec ses sources).

Fichier separe d'`orchestrateur.py` : l'orchestrateur ne fait que l'appeler (`_formulaire("connexion")`).
Aucun texte n'est ecrit en dur ici sans passer par `lang.t()` : l'anglais est dans `langue.py`.
"""
import html
import json
import random

import langue as lang
import infos_accueil

_GABARIT = """<!doctype html>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,interactive-widget=resizes-content">
<title>{titre} — NarwhalChampions</title>
{tete_appli}
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bangers&display=swap">
<style>
  /* Jetons de l'affichage « Normal » du jeu (affichage-epure-pages.css) : une seule teinte d'action, le bleu. */
  :root {{
    color-scheme: dark;
    --bg:#111318; --panel:#1c2028; --panel-2:#292e38; --border:#383e49;
    --text:#f2f3f5; --muted:#9da5b3;
    --accent:#3f86e0; --accent-hover:#5a9bf0; --accent-soft:rgba(63,134,224,.16); --accent-ink:#fff;
    --danger:#f85149; --warn:#f0b95f;
    --affiche:"Bangers","Anton",Impact,"Arial Black",sans-serif;
    --cut:14px;
  }}
  * {{ box-sizing:border-box; }}
  html {{ scroll-behavior:smooth; }}
  body {{ margin:0; min-height:100vh; display:flex; flex-direction:column; font:16px/1.5 system-ui,sans-serif;
         background:var(--bg); color:var(--text);
         background-image:radial-gradient(60rem 28rem at 50% -8rem, var(--accent-soft), transparent 70%),
                          radial-gradient(rgba(63,134,224,.10) 1px, transparent 1.6px);
         background-size:100% 100%, 16px 16px; }}
  a {{ color:var(--accent); }}
  a:hover {{ color:var(--accent-hover); }}
  :focus-visible {{ outline:2px solid var(--accent-hover); outline-offset:2px; }}

  /* ---- Biseau : coins haut-droit et bas-gauche coupes, filet de 1 px fait par un second decoupage plus petit. ---- */
  .biseau {{ --c:var(--cut); position:relative; background:var(--border);
            clip-path:polygon(0 0,calc(100% - var(--c)) 0,100% var(--c),100% 100%,var(--c) 100%,0 calc(100% - var(--c))); padding:1px; }}
  .biseau > .dedans {{ background:var(--panel);
            clip-path:polygon(0 0,calc(100% - var(--c) + 1px) 0,100% calc(var(--c) - 1px),100% 100%,calc(var(--c) - 1px) 100%,0 calc(100% - var(--c) + 1px)); }}
  .biseau.vif {{ background:var(--accent); }}

  /* ---- En-tete ---- */
  .entete {{ position:sticky; top:0; z-index:10; display:flex; align-items:center; gap:1.2rem; height:3.4rem;
            padding:0 max(1.2rem,env(safe-area-inset-left,0px)); background:rgba(28,32,40,.94); backdrop-filter:blur(6px);
            border-bottom:1px solid var(--border); }}
  .marque {{ display:flex; align-items:center; gap:.6rem; color:var(--text); text-decoration:none;
            font:1.35rem/1 var(--affiche); letter-spacing:.05em; text-transform:uppercase; }}
  .marque img {{ width:2rem; height:2rem; border-radius:50%; box-shadow:0 0 0 1px var(--border); }}
  .nav {{ display:flex; gap:.2rem; flex:1; }}
  .nav a {{ color:var(--muted); text-decoration:none; font-size:.9rem; padding:.4rem .7rem; }}
  .nav a:hover {{ color:var(--text); background:var(--panel-2); }}
  .droite {{ display:flex; align-items:center; gap:.7rem; margin-left:auto; padding-right:max(0rem,env(safe-area-inset-right,0px)); }}
  .lang {{ display:inline-flex; border:1px solid var(--border); font-size:.8rem; font-weight:600; text-decoration:none; }}
  .lang span {{ padding:.25rem .55rem; color:var(--muted); }}
  .lang span.lang-active {{ background:var(--accent); color:var(--accent-ink); }}
  .bouton {{ --c:9px; display:inline-flex; align-items:center; justify-content:center; gap:.5rem; font:inherit; font-weight:700;
            text-decoration:none; cursor:pointer; border:0; min-height:2.5rem; padding:.55rem 1.1rem; color:var(--accent-ink);
            background:var(--accent);
            clip-path:polygon(0 0,calc(100% - var(--c)) 0,100% var(--c),100% 100%,var(--c) 100%,0 calc(100% - var(--c))); }}
  .bouton:hover {{ background:var(--accent-hover); color:var(--accent-ink); }}
  .bouton.calme {{ background:var(--panel-2); color:var(--text); box-shadow:inset 0 0 0 1px var(--border); }}
  .bouton.calme:hover {{ background:#343a46; color:var(--text); }}
  .bouton.plein {{ width:100%; min-height:3rem; font-size:1.02rem; }}

  /* ---- Scene centrale ---- */
  main {{ flex:1; width:100%; max-width:62rem; margin:0 auto; padding:2.6rem max(1.2rem,env(safe-area-inset-left,0px)) 2rem; }}
  .titre {{ text-align:center; margin:0 0 1.9rem; }}
  .titre h1 {{ margin:0; font:clamp(2.2rem,5.6vw,3.8rem)/1 var(--affiche); letter-spacing:.04em; text-transform:uppercase; text-wrap:balance; }}
  .titre h1 em {{ font-style:normal; color:var(--accent); }}
  .titre p {{ margin:.7rem auto 0; max-width:36rem; color:var(--muted); text-wrap:balance; }}
  .cartes {{ display:grid; grid-template-columns:1fr 1fr; gap:1.2rem; align-items:stretch; }}
  .cartes .biseau, .cartes .dedans {{ display:flex; flex-direction:column; }}
  .cartes .dedans {{ flex:1; padding:1.5rem 1.5rem 1.4rem; }}
  .cartes h2 {{ margin:0 0 .3rem; font:1.7rem/1.1 var(--affiche); letter-spacing:.04em; text-transform:uppercase; }}
  .cartes .sous {{ margin:0 0 1.1rem; color:var(--muted); font-size:.92rem; }}
  form {{ margin:0; display:flex; flex-direction:column; flex:1; }}
  label {{ display:block; margin-bottom:.9rem; font-size:.85rem; color:var(--muted); }}
  input {{ width:100%; font:inherit; margin-top:.3rem; background:var(--bg); color:var(--text); border:1px solid var(--border);
          padding:.65rem .8rem; border-radius:0; }}
  input:focus {{ border-color:var(--accent); outline:none; box-shadow:0 0 0 2px var(--accent-soft); }}
  form .bouton {{ margin-top:auto; }}
  .erreur {{ border:1px solid var(--danger); background:#1d1113; color:#ff7b72; padding:.65rem .85rem; margin-bottom:1rem; font-size:.9rem; }}
  .petit {{ margin:.9rem 0 0; font-size:.82rem; color:var(--muted); }}
  .petit a {{ color:var(--accent); }}
  .liste {{ margin:0 0 1.2rem; padding:0; list-style:none; display:grid; gap:.45rem; color:var(--text); font-size:.92rem; }}
  .liste li {{ display:flex; gap:.6rem; align-items:baseline; }}
  .liste li::before {{ content:""; flex:none; width:.5rem; height:.5rem; background:var(--accent); transform:translateY(-.08rem) rotate(45deg); }}
  .cartes .invite .bouton {{ margin-top:auto; }}

  /* ---- La bande du bas : une info a la fois ---- */
  .bande {{ margin-top:2rem; }}
  .bande .dedans {{ display:grid; grid-template-columns:auto 1fr auto; gap:1rem; align-items:center; padding:.9rem 1.1rem; min-height:5.6rem; }}
  .etiquette {{ font:1.15rem/1 var(--affiche); letter-spacing:.06em; text-transform:uppercase; padding:.45rem .7rem; color:var(--accent-ink);
               background:var(--accent); white-space:nowrap; }}
  .etiquette.astuce {{ background:var(--warn); color:#1a1405; }}
  .bande p {{ margin:0; font-size:.98rem; text-wrap:pretty; }}
  .bande .src {{ display:block; margin-top:.25rem; color:var(--muted); font-size:.75rem; }}
  .fleches {{ display:flex; gap:.4rem; }}
  .fleches button {{ width:2.4rem; height:2.4rem; background:var(--panel-2); color:var(--text); border:1px solid var(--border); cursor:pointer;
                    font-size:1.1rem; line-height:1; border-radius:0; }}
  .fleches button:hover {{ border-color:var(--accent); color:var(--accent-hover); }}
  .points {{ display:flex; gap:.35rem; justify-content:center; margin-top:.7rem; }}
  .points i {{ width:.5rem; height:.5rem; background:var(--border); transform:rotate(45deg); }}
  .points i.on {{ background:var(--accent); }}
  @media (prefers-reduced-motion:no-preference) {{ .bande p {{ animation:entre .35s ease-out; }} @keyframes entre {{ from {{ opacity:0; transform:translateY(4px); }} }} }}

  footer {{ padding:1rem max(1.2rem,env(safe-area-inset-left,0px)) 1.6rem; max-width:62rem; margin:0 auto; width:100%; color:var(--muted); }}
  footer .liens {{ display:none; gap:1rem; flex-wrap:wrap; margin-bottom:.8rem; font-size:.9rem; }}
  .regle {{ margin:0 0 .7rem; font-size:.85rem; }}
  .mention-legale {{ color:var(--muted); opacity:.75; font-size:.72rem; line-height:1.5; margin:0; }}

  @media (max-width:820px) {{
    .nav {{ display:none; }}
    footer .liens {{ display:flex; }}
    .cartes {{ grid-template-columns:1fr; }}
    main {{ padding-top:1.6rem; }}
  }}
  /* TELEPHONE : les deux choix doivent tenir dans le premier ecran, sans defiler (remarque de l'utilisateur, 18/11/2026).
     On retire ce qui explique (accroche, sous-titres, liste de la carte invite) et on serre les marges. */
  @media (max-width:820px) {{
    main {{ padding-top:1rem; padding-bottom:1.2rem; }}
    .titre {{ margin-bottom:.9rem; }}
    .titre h1 {{ font-size:1.9rem; }}
    .titre p, .cartes .sous, .cartes .liste {{ display:none; }}
    .cartes {{ gap:.7rem; }}
    .cartes h2 {{ font-size:1.35rem; margin-bottom:.7rem; }}
    .cartes .dedans {{ padding:1rem 1.1rem; }}
    label {{ margin-bottom:.6rem; }}
    .petit {{ margin-top:.6rem; }}
    .bande {{ margin-top:1rem; }}
  }}
  @media (max-width:560px) {{
    .entete {{ gap:.6rem; padding-left:max(.8rem,env(safe-area-inset-left,0px)); }}
    .marque {{ font-size:1.1rem; }}
    .marque span {{ display:none; }}
    .entete .bouton {{ min-height:2.3rem; padding:.4rem .8rem; }}
    .cartes .dedans {{ padding:1.2rem 1.1rem; }}
    input {{ min-height:44px; font-size:16px; }}
    .bouton {{ min-height:44px; }}
    .bande .dedans {{ grid-template-columns:1fr; gap:.7rem; }}
    .fleches {{ justify-content:flex-end; }}
  }}
</style>
<header class="entete">
  <a class="marque" href="/"><img src="/narwhal.png" alt="" width="512" height="512"><span>NarwhalChampions</span></a>
  <nav class="nav" aria-label="{nav_nom}">{liens}</nav>
  <div class="droite">{langue}<a class="bouton" href="#acces">{se_connecter}</a></div>
</header>
<main>
  <div class="titre">
    <h1>{titre_h1}</h1>
    <p>{accroche}</p>
  </div>
  <div class="cartes">
    <section class="biseau vif" id="acces" aria-labelledby="t-acces"><div class="dedans">
      <h2 id="t-acces">{t_compte}</h2>
      <p class="sous">{s_compte}</p>
      {erreur}
      <form method="post" action="/connexion">
        {champs}
        <label>{mdp}<input name="mdp" type="password" autocomplete="current-password" required></label>
        <button class="bouton plein" type="submit">{se_connecter}</button>
      </form>
      <p class="petit">{oubli}</p>
    </div></section>
    <section class="biseau invite" aria-labelledby="t-invite"><div class="dedans">
      <h2 id="t-invite">{t_invite}</h2>
      <p class="sous">{s_invite}</p>
      <ul class="liste">{points_invite}</ul>
      <a class="bouton calme plein" href="/jouer-invite">{jouer_sans}</a>
      <p class="petit">{vers_inscription}</p>
    </div></section>
  </div>
  <div class="bande biseau" role="region" aria-label="{bande_nom}" aria-live="polite"><div class="dedans">
    <span class="etiquette {classe0}" id="b-etiquette">{etiquette0}</span>
    <div><p id="b-texte">{texte0}</p><span class="src" id="b-src">{src0}</span></div>
    <div class="fleches"><button type="button" id="b-prec" aria-label="{prec}">‹</button><button type="button" id="b-suiv" aria-label="{suiv}">›</button></div>
  </div></div>
  <div class="points" id="b-points" aria-hidden="true"></div>
</main>
<footer>
  <div class="liens">{liens}</div>
  <p class="regle">{regle}</p>
  <p class="mention-legale">{mention}</p>
  {bouton_appli}
</footer>
<script type="application/json" id="infos">{infos_json}</script>
<script>(function(){{
  var infos = JSON.parse(document.getElementById("infos").textContent);
  var n = infos.items.length, i = infos.depart, minuteur = null;
  var et = document.getElementById("b-etiquette"), tx = document.getElementById("b-texte"), sr = document.getElementById("b-src"),
      pts = document.getElementById("b-points");
  function peindre() {{
    var it = infos.items[i];
    et.textContent = it.type === "astuce" ? infos.noms.astuce : infos.noms.comics;
    et.className = "etiquette" + (it.type === "astuce" ? " astuce" : "");
    var p = tx.cloneNode(false); p.id = "b-texte"; p.textContent = it.texte; tx.replaceWith(p); tx = p;
    sr.textContent = it.source || "";
    // Une rangee de points glissante : jamais plus de 9, pour ne pas deborder avec 60 infos.
    var debut = Math.max(0, Math.min(n - 9, i - 4)), html = "";
    for (var k = debut; k < Math.min(n, debut + 9); k++) html += '<i class="' + (k === i ? "on" : "") + '"></i>';
    pts.innerHTML = html;
  }}
  function aller(d) {{ i = (i + d + n) % n; peindre(); relancer(); }}
  function relancer() {{
    clearInterval(minuteur);
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    minuteur = setInterval(function () {{ if (!document.hidden) {{ i = (i + 1) % n; peindre(); }} }}, 9000);
  }}
  document.getElementById("b-prec").onclick = function () {{ aller(-1); }};
  document.getElementById("b-suiv").onclick = function () {{ aller(1); }};
  peindre(); relancer();
}})();</script>
"""


def _liens_publics() -> str:
    """Les pages qu'on peut ouvrir sans compte (verifie dans `do_GET` : /signaler-un-bug et /contact-createurs)."""
    return ('<a href="/signaler-un-bug">%s</a><a href="/contact-createurs">%s</a><a href="/inscription">%s</a>'
            % (lang.t("Signaler un bug"), lang.t("Contacter les créateurs"), lang.t("Demander un compte")))


def page_connexion(erreur: str = "", instance_discord: str = "", *, langue_html: str, bouton_appli: str, mention: str,
                   tete_appli: str, jours_expiration: int, aleatoire: random.Random | None = None) -> str:
    """La page complete (str). `langue_html`, `bouton_appli`, `mention`, `tete_appli` viennent de l'orchestrateur."""
    infos = infos_accueil.pour_la_page(lang.actuelle(), aleatoire)
    premier = infos["items"][infos["depart"]]
    champs = ('<label>%s<input name="pseudo" autocomplete="username" required></label>'
              % lang.t("Pseudo ou adresse e-mail"))
    if instance_discord:
        champs += '<input type="hidden" name="da" value="%s">' % html.escape(instance_discord)
    # Les « < » du JSON ne doivent jamais fermer la balise <script>.
    infos_json = json.dumps(infos, ensure_ascii=False).replace("<", "\\u003c")
    liens = _liens_publics()
    return _GABARIT.format(
        titre=lang.t("Se connecter"), tete_appli=tete_appli, langue=langue_html, liens=liens,
        nav_nom=lang.t("Pages publiques"), se_connecter=lang.t("Se connecter"),
        titre_h1=lang.t("Prêt pour la <em>prochaine partie</em> ?"),
        accroche=lang.t("Marvel Champions dans ton navigateur : tes héros, tes decks, tes parties en solo ou à plusieurs."),
        t_compte=lang.t("J'ai un compte"), s_compte=lang.t("Retrouve tes decks, tes campagnes et tes parties en cours."),
        erreur='<div class="erreur">%s</div>' % html.escape(erreur) if erreur else "", champs=champs, mdp=lang.t("Mot de passe"),
        oubli=lang.t("Mot de passe oublié ? Demande un lien de réinitialisation à l'administrateur."),
        t_invite=lang.t("Je n'ai pas de compte"), s_invite=lang.t("Lance une partie tout de suite, sans rien créer."),
        points_invite="".join("<li>%s</li>" % lang.t(p) for p in (
            "Une table en ligne prête en quelques secondes",
            "Invite tes amis par un simple lien",
            "Tout est jouable, il suffit de posséder le jeu")),
        jouer_sans=lang.t("Jouer sans compte"),
        vers_inscription=lang.t('Tu veux garder tes decks et tes parties ? <a href="/inscription">Demande un compte</a>.'),
        bande_nom=lang.t("Le saviez-vous et astuces"), prec=lang.t("Précédent"), suiv=lang.t("Suivant"),
        classe0="astuce" if premier["type"] == "astuce" else "",
        etiquette0=infos["noms"]["astuce" if premier["type"] == "astuce" else "comics"],
        texte0=html.escape(premier["texte"]), src0=html.escape(premier.get("source") or ""),
        regle=lang.t("Les places sont comptées : {jours} jours sans venir et la tienne retourne au pot. Écris-moi, je te la rends.").replace("{jours}", str(jours_expiration)),
        mention=mention, bouton_appli=bouton_appli, infos_json=infos_json,
    )
