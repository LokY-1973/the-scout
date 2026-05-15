import streamlit as st
import plotly.graph_objects as go
import json, pandas as pd

st.set_page_config(page_title="The Scout", page_icon="⚽", layout="wide", initial_sidebar_state="collapsed")

for k,v in [("page","league_select"),("league",None),("team",None),("position",None)]:
    if k not in st.session_state: st.session_state[k] = v

@st.cache_data
def load_squads():
    with open("data/squads.json") as f: return json.load(f)
@st.cache_data
def load_stats():
    try: return pd.read_csv("data/all_players.csv")
    except: return pd.DataFrame()

SQUADS = load_squads()
STATS  = load_stats()

LEAGUES = {
    "Premier League":{"code":"PL","logo":"https://crests.football-data.org/PL.png",
        "bg":"linear-gradient(135deg,#37003C 0%,#1a0020 50%,#004d2e 100%)"},
    "La Liga":{"code":"PD","logo":"https://crests.football-data.org/PD.png",
        "bg":"linear-gradient(135deg,#FF4B00 0%,#1a0500 50%,#001a4d 100%)"},
    "Bundesliga":{"code":"BL1","logo":"https://crests.football-data.org/BL1.png",
        "bg":"linear-gradient(135deg,#D3010C 0%,#1a0000 50%,#111 100%)"},
    "Serie A":{"code":"SA","logo":"https://crests.football-data.org/SA.png",
        "bg":"linear-gradient(135deg,#024494 0%,#011228 50%,#000 100%)"},
    "Ligue 1":{"code":"FL1","logo":"https://crests.football-data.org/FL1.png",
        "bg":"linear-gradient(135deg,#003DA5 0%,#001228 50%,#1a1a1a 100%)"},
}

TEAM_COLORS = {
    "Arsenal FC":("#EF0107","#063672"),"Manchester City FC":("#6CABDD","#1C2C5B"),
    "Liverpool FC":("#C8102E","#00B2A9"),"Chelsea FC":("#034694","#DBA111"),
    "Manchester United FC":("#DA291C","#FBE122"),"Tottenham Hotspur FC":("#132257","#FFFFFF"),
    "Newcastle United FC":("#241F20","#41B6E6"),"Aston Villa FC":("#95BFE5","#670E36"),
    "Brighton & Hove Albion FC":("#0057B8","#FFCD00"),"West Ham United FC":("#7A263A","#1BB1E7"),
    "Crystal Palace FC":("#1B458F","#C4122E"),"Fulham FC":("#CC0000","#000000"),
    "Brentford FC":("#E30613","#FFFFFF"),"Wolverhampton Wanderers FC":("#FDB913","#231F20"),
    "Everton FC":("#003399","#FFFFFF"),"Nottingham Forest FC":("#DD0000","#FFFFFF"),
    "Leeds United FC":("#FFCD00","#1D428A"),"AFC Bournemouth":("#DA291C","#000000"),
    "Burnley FC":("#6C1D45","#99D6EA"),"Sunderland AFC":("#EB172B","#000000"),
    "FC Barcelona":("#A50044","#004D98"),"Real Madrid CF":("#00529F","#FEBE10"),
    "Club Atlético de Madrid":("#CB3524","#003DA5"),"Real Betis Balompié":("#00954C","#FFFFFF"),
    "Sevilla FC":("#D2122E","#FFFFFF"),"Villarreal CF":("#FFCD00","#009DE0"),
    "Athletic Club":("#EE2523","#FFFFFF"),"Real Sociedad de Fútbol":("#1768AC","#FFFFFF"),
    "RC Celta de Vigo":("#8DC8E8","#000000"),"Valencia CF":("#FF7F00","#000000"),
    "Girona FC":("#9D2235","#FFFFFF"),"Getafe CF":("#005998","#FFFFFF"),
    "CA Osasuna":("#D32532","#003DA5"),"RCD Espanyol de Barcelona":("#0070B8","#FFFFFF"),
    "Deportivo Alavés":("#002B7F","#FFFFFF"),"RCD Mallorca":("#EE3524","#000000"),
    "Rayo Vallecano de Madrid":("#CC0000","#FFFFFF"),"Levante UD":("#004B9B","#D10A11"),
    "Elche CF":("#00833F","#FFFFFF"),"Real Oviedo":("#003DA5","#FFFFFF"),
    "FC Bayern München":("#DC052D","#0066B2"),"Borussia Dortmund":("#FDE100","#000000"),
    "Bayer 04 Leverkusen":("#E32221","#000000"),"RB Leipzig":("#DD0741","#001E62"),
    "Eintracht Frankfurt":("#E1000F","#000000"),"VfB Stuttgart":("#E32219","#FFFFFF"),
    "SC Freiburg":("#E32328","#000000"),"1. FC Köln":("#FF0000","#FFFFFF"),
    "Hamburger SV":("#005CA9","#FFFFFF"),"Borussia Mönchengladbach":("#000000","#FFFFFF"),
    "VfL Wolfsburg":("#65B32E","#003D72"),"SV Werder Bremen":("#1D9A48","#FFFFFF"),
    "TSG 1899 Hoffenheim":("#1763A2","#FFFFFF"),"1. FSV Mainz 05":("#C3152A","#FFFFFF"),
    "FC Augsburg":("#BA3733","#FFFFFF"),"FC St. Pauli 1910":("#8B1C10","#FFFFFF"),
    "1. FC Union Berlin":("#EB1923","#FFFFFF"),"1. FC Heidenheim 1846":("#DA251D","#FFFFFF"),
    "FC Internazionale Milano":("#010E80","#000000"),"Juventus FC":("#000000","#FFFFFF"),
    "AC Milan":("#FB090B","#000000"),"SSC Napoli":("#087DB0","#FFFFFF"),
    "AS Roma":("#8E1F2F","#F5C518"),"SS Lazio":("#87D8F7","#003DA5"),
    "ACF Fiorentina":("#4B1869","#FFFFFF"),"Atalanta BC":("#1C3580","#000000"),
    "Bologna FC 1909":("#9A1F40","#003DA5"),"Torino FC":("#8B1C10","#FFFFFF"),
    "Udinese Calcio":("#333333","#FFFFFF"),"Cagliari Calcio":("#004B98","#FFFFFF"),
    "Genoa CFC":("#A81620","#003DA5"),"Hellas Verona FC":("#134E96","#FFD700"),
    "Parma Calcio 1913":("#FFDD00","#003DA5"),"US Lecce":("#FFD700","#DA291C"),
    "Como 1907":("#1B4FA0","#FFFFFF"),"US Cremonese":("#D2122E","#FFFFFF"),
    "US Sassuolo Calcio":("#1E7A3B","#000000"),"AC Pisa 1909":("#003DA5","#FFFFFF"),
    "Paris Saint-Germain FC":("#004170","#DA291C"),"AS Monaco FC":("#CE1126","#FFFFFF"),
    "Olympique de Marseille":("#009CDE","#FFFFFF"),"Lille OSC":("#EF3340","#FFFFFF"),
    "OGC Nice":("#C8102E","#000000"),"Olympique Lyonnais":("#0040A0","#FFFFFF"),
    "Stade Rennais FC 1901":("#CC0000","#000000"),"Racing Club de Lens":("#ED1C24","#FFCD00"),
    "Stade Brestois 29":("#EF3340","#FFFFFF"),"AJ Auxerre":("#003DA5","#FFFFFF"),
    "Toulouse FC":("#6C2A88","#FFFFFF"),"FC Nantes":("#FFCD00","#000000"),
    "RC Strasbourg Alsace":("#005CA9","#FFFFFF"),"FC Lorient":("#F90000","#000000"),
    "Angers SCO":("#222222","#FFFFFF"),"Le Havre AC":("#1C62B9","#FFFFFF"),
    "FC Metz":("#8B1C2E","#FFCD00"),"Paris FC":("#001489","#FFFFFF"),
}

POS_MAP = {
    "Goalkeeper":"GK","Centre-Back":"CB","Right-Back":"RB","Left-Back":"LB",
    "Defensive Midfield":"CDM","Central Midfield":"CM","Attacking Midfield":"CAM",
    "Right Winger":"RW","Left Winger":"LW","Left Midfield":"CM","Right Midfield":"CM",
    "Centre-Forward":"ST","Secondary Striker":"ST","Defence":"CB","Midfield":"CM","Offence":"ST",
}

# 4-3-3 positions: (x, y) where y=0 is bottom (GK end), y=100 is top (attack)
FORMATION_433 = {
    "GK":  [(50, 10)],
    "RB":  [(82, 28)],
    "CB":  [(63, 25),(37, 25)],
    "LB":  [(18, 28)],
    "CDM": [(50, 45)],
    "CM":  [(70, 57),(30, 57)],
    "RW":  [(80, 76)],
    "ST":  [(50, 84)],
    "LW":  [(20, 76)],
}

POSITION_ARCHETYPES = {
    "GK":  ["🧤 Shot Stopper","🦶 Sweeper Keeper","👊 Command of Area"],
    "RB":  ["⚡ Attacking","⚖️ Balanced","🛡️ Defensive"],
    "LB":  ["⚡ Attacking","⚖️ Balanced","🛡️ Defensive"],
    "CB":  ["🏃 Pace CB","🎯 Ball-Playing CB","💪 Physical CB","🛡️ Defensive CB"],
    "CDM": ["⚓ Defensive Anchor","💥 Ball Winner","🎭 Deep Playmaker"],
    "CM":  ["🔄 Box-to-Box","🎨 Advanced Playmaker","🛡️ Defensive CM","🌀 Mezzala"],
    "CAM": ["🎩 Classic #10","👟 Shadow Striker"],
    "RW":  ["🔄 Inverted Winger","🏃 Traditional Winger","🎯 Inside Forward"],
    "LW":  ["🔄 Inverted Winger","🏃 Traditional Winger","🎯 Inside Forward"],
    "ST":  ["🏆 Complete Forward","📍 Poacher","🎭 False 9","🎯 Target Man","🔥 Press Forward"],
}

TIER_COLORS = {
    "Crucial":"#FFD700","Important":"#3A86FF","Rotation":"#06D6A0",
    "Sporadic":"#6C757D","Prospect":"#9B59B6","Unknown":"#546E7A",
}
TIER_MINS = {"Premier League":3420,"La Liga":3420,"Bundesliga":3060,"Serie A":3420,"Ligue 1":3060}

def get_tier(mins, league, age):
    if age and age <= 21 and mins < 1500: return "Prospect"
    total = TIER_MINS.get(league, 3420)
    pct   = mins / total if total else 0
    if pct > 0.75: return "Crucial"
    if pct > 0.55: return "Important"
    if pct > 0.30: return "Rotation"
    if pct > 0:    return "Sporadic"
    return "Unknown"

def get_mins(name):
    if STATS.empty: return 0
    last = name.split()[-1]
    m = STATS[STATS["Player"].str.contains(last, na=False, case=False)]
    if len(m):
        v = pd.to_numeric(m.iloc[0]["Min"], errors="coerce")
        return int(v) if not pd.isna(v) else 0
    return 0

def clean_name(n):
    for r in [" FC"," CF"," AFC","FC ","AFC "," SC"," AC"," BC"," 1909"," 1910"," 1846"," 1899"]:
        n = n.replace(r,"")
    return n.strip()

def short_name(full):
    parts = full.split()
    if len(parts) == 1: return full
    return parts[-1] if len(parts[-1]) > 3 else full

def team_gradient(team_key):
    c1,c2 = TEAM_COLORS.get(team_key,("#1a1a2e","#0f3460"))
    return f"linear-gradient(135deg,{c2} 0%,#080810 50%,{c1}55 100%)"

def set_bg(grad):
    st.markdown(f"""<style>
    .stApp,[data-testid="stAppViewContainer"],.main,.block-container{{
        background:{grad} !important;background-attachment:fixed !important;
    }}
    </style>""", unsafe_allow_html=True)

st.markdown("""<style>
*{font-family:'Segoe UI',Arial,sans-serif;}
h1,h2,h3,p,label,div{color:#f0f0f0;}
.player-card{background:rgba(255,255,255,0.07);border:1px solid rgba(255,255,255,0.12);
    border-radius:10px;padding:14px;margin:6px 0;}
.player-card.selected{border:2px solid #FFD700;background:rgba(255,215,0,0.08);}
.tier-badge{display:inline-block;padding:3px 10px;border-radius:12px;font-size:12px;font-weight:700;}
.section-title{font-size:20px;font-weight:700;margin-bottom:12px;}
</style>""", unsafe_allow_html=True)

def tier_badge(tier):
    c = TIER_COLORS.get(tier,"#444")
    tc = "#000" if tier in ["Crucial","Rotation","Prospect"] else "#fff"
    i  = {"Crucial":"🥇","Important":"🔵","Rotation":"🟢","Sporadic":"⚪","Prospect":"🟣","Unknown":""}
    return f'<span class="tier-badge" style="background:{c};color:{tc}">{i.get(tier,"")} {tier}</span>'

def group_squad(raw_squad, league):
    grouped = {}
    for p in raw_squad:
        pos  = POS_MAP.get(p.get("position") or "Midfield","CM")
        mins = get_mins(p.get("name",""))
        tier = get_tier(mins, league, p.get("age"))
        grouped.setdefault(pos,[]).append({**p,"pos_key":pos,"mins":mins,"tier":tier})
    return grouped

def draw_pitch(squad_grouped, selected_pos, team_key):
    c1,c2 = TEAM_COLORS.get(team_key,("#1C2C5B","#6CABDD"))
    fig = go.Figure()

    # ── Pitch markings ──
    fig.add_shape(type="rect",x0=0,x1=100,y0=0,y1=100,fillcolor="#2d8a3e",line=dict(color="#fff",width=2))
    # Stripes
    for i in range(10):
        if i%2==0:
            fig.add_shape(type="rect",x0=0,x1=100,y0=i*10,y1=(i+1)*10,
                          fillcolor="rgba(255,255,255,0.03)",line=dict(width=0))
    fig.add_shape(type="line",x0=0,x1=100,y0=50,y1=50,line=dict(color="rgba(255,255,255,0.5)",width=1.5))
    fig.add_shape(type="circle",x0=42,x1=58,y0=42,y1=58,line=dict(color="rgba(255,255,255,0.5)",width=1.5))
    fig.add_shape(type="circle",x0=49,x1=51,y0=49,y1=51,fillcolor="white",line=dict(width=0))
    # Bottom penalty area
    fig.add_shape(type="rect",x0=18,x1=82,y0=0,y1=17,
                  line=dict(color="rgba(255,255,255,0.5)",width=1.5),fillcolor="rgba(0,0,0,0)")
    # Top penalty area
    fig.add_shape(type="rect",x0=18,x1=82,y0=83,y1=100,
                  line=dict(color="rgba(255,255,255,0.5)",width=1.5),fillcolor="rgba(0,0,0,0)")
    # Bottom 6-yard
    fig.add_shape(type="rect",x0=37,x1=63,y0=0,y1=6,
                  line=dict(color="rgba(255,255,255,0.4)",width=1),fillcolor="rgba(0,0,0,0)")
    # Top 6-yard
    fig.add_shape(type="rect",x0=37,x1=63,y0=94,y1=100,
                  line=dict(color="rgba(255,255,255,0.4)",width=1),fillcolor="rgba(0,0,0,0)")
    # Goals
    fig.add_shape(type="rect",x0=44,x1=56,y0=0,y1=-2,fillcolor="rgba(255,255,255,0.3)",line=dict(width=0))
    fig.add_shape(type="rect",x0=44,x1=56,y0=100,y1=102,fillcolor="rgba(255,255,255,0.3)",line=dict(width=0))

    # ── Players ──
    for pos, pts in FORMATION_433.items():
        players = squad_grouped.get(pos,[])
        starter = players[0] if players else None
        tier    = starter["tier"] if starter else "Unknown"
        tcolor  = TIER_COLORS.get(tier,"#546E7A")
        is_sel  = (pos == selected_pos)
        name    = short_name(starter["name"]) if starter else "—"

        for (x,y) in pts:
            # Glow for selected
            if is_sel:
                fig.add_trace(go.Scatter(
                    x=[x],y=[y],mode="markers",
                    marker=dict(size=56,color="rgba(255,255,255,0.15)",line=dict(width=0)),
                    hoverinfo="skip",showlegend=False))

            # Player circle (dark with tier color border)
            fig.add_trace(go.Scatter(
                x=[x],y=[y],mode="markers",
                marker=dict(
                    size=36 if is_sel else 30,
                    color="#1a1a2e" if not is_sel else tcolor,
                    line=dict(color=tcolor,width=4 if is_sel else 2.5),
                    symbol="circle",
                ),
                hovertext=f"<b>{pos}</b>: {starter['name'] if starter else '—'}<br>Tier: {tier}",
                hoverinfo="text",showlegend=False,
            ))

            # Position label inside circle
            fig.add_trace(go.Scatter(
                x=[x],y=[y],mode="text",
                text=[f"<b>{pos}</b>"],
                textfont=dict(color="#fff" if not is_sel else "#000",size=8,family="Arial Black"),
                hoverinfo="skip",showlegend=False,
            ))

            # Player name below circle
            fig.add_trace(go.Scatter(
                x=[x],y=[y-7],mode="text",
                text=[f"<b>{name}</b>"],
                textfont=dict(color="white",size=9,family="Arial"),
                hoverinfo="skip",showlegend=False,
            ))

    fig.update_layout(
        xaxis=dict(range=[-3,103],visible=False,fixedrange=True),
        yaxis=dict(range=[-10,110],visible=False,scaleanchor="x",fixedrange=True),
        plot_bgcolor="rgba(0,0,0,0)",paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0,r=0,t=0,b=0),height=540,
        hoverlabel=dict(bgcolor="#111",font_color="#fff",bordercolor="#333"),
        dragmode=False,
    )
    return fig

# ── PAGES ─────────────────────────────────────────────────────────────────────

def page_league_select():
    set_bg("linear-gradient(135deg,#0a0a0a 0%,#111 100%)")
    st.markdown("<h1 style='text-align:center;font-size:44px;margin-bottom:6px'>⚽ The Scout</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;color:#888;font-size:16px;margin-bottom:48px'>Football Intelligence Platform</p>", unsafe_allow_html=True)
    cols = st.columns(5)
    for i,(name,data) in enumerate(LEAGUES.items()):
        with cols[i]:
            st.markdown('<div style="background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.1);border-radius:16px;padding:24px 10px;text-align:center">',unsafe_allow_html=True)
            st.image(data["logo"],width=88)
            st.markdown(f'<p style="font-weight:700;margin-top:10px;font-size:13px">{name}</p>',unsafe_allow_html=True)
            st.markdown('</div>',unsafe_allow_html=True)
            if st.button("Select",key=f"lg_{name}",use_container_width=True):
                st.session_state.league=name; st.session_state.page="team_select"
                st.session_state.team=None; st.session_state.position=None; st.rerun()

def page_team_select():
    set_bg(LEAGUES[st.session_state.league]["bg"])
    c1,c2=st.columns([1,6])
    with c1:
        if st.button("← Leagues"): st.session_state.page="league_select"; st.rerun()
    with c2:
        st.markdown(f"<h2 style='margin:0'>{st.session_state.league}</h2>",unsafe_allow_html=True)
    st.markdown("<p style='color:#aaa;margin-bottom:20px'>Select a team</p>",unsafe_allow_html=True)
    st.markdown("---")
    teams={k:v for k,v in SQUADS.items() if v["league"]==st.session_state.league}
    cols=st.columns(5)
    for i,(tk,td) in enumerate(teams.items()):
        with cols[i%5]:
            crest=td.get("crest","")
            if crest:
                try: st.image(crest,width=64)
                except: pass
            if st.button(clean_name(tk),key=f"tm_{tk}",use_container_width=True):
                st.session_state.team=tk; st.session_state.page="formation"
                st.session_state.position=None; st.rerun()

def page_formation():
    tk   = st.session_state.team
    td   = SQUADS.get(tk,{})
    lg   = td.get("league","Premier League")
    sq   = td.get("squad",[])
    crest= td.get("crest","")
    set_bg(team_gradient(tk))
    grp  = group_squad(sq, lg)

    # Header
    h1,h2,h3,_=st.columns([1,0.7,4,3])
    with h1:
        if st.button("← Teams"): st.session_state.page="team_select"; st.rerun()
    with h2:
        if crest:
            try: st.image(crest,width=52)
            except: pass
    with h3:
        st.markdown(f"<h2 style='margin:0;padding-top:6px'>{clean_name(tk)}</h2>",unsafe_allow_html=True)
        st.markdown(f"<span style='color:#aaa;font-size:13px'>{lg} · 4-3-3</span>",unsafe_allow_html=True)

    st.markdown("---")

    # Tier legend
    legend="&nbsp;&nbsp;".join([
        f'<span class="tier-badge" style="background:{c};color:{"#000" if t in ["Crucial","Rotation","Prospect"] else "#fff"};font-size:11px">{t}</span>'
        for t,c in TIER_COLORS.items() if t!="Unknown"])
    st.markdown(legend+"<br><br>",unsafe_allow_html=True)

    cp,pp=st.columns([1.1,1])

    with cp:
        pos_keys=list(FORMATION_433.keys())
        sel_idx=pos_keys.index(st.session_state.position) if st.session_state.position in pos_keys else 0
        sel=st.radio("pos",pos_keys,index=sel_idx,horizontal=True,label_visibility="collapsed")
        st.session_state.position=sel
        fig=draw_pitch(grp,sel,tk)
        st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False,"staticPlot":True})

    with pp:
        st.markdown(f"<div class='section-title'>{sel} — Current Options</div>",unsafe_allow_html=True)
        players=grp.get(sel,[])
        if players:
            for p in sorted(players,key=lambda x:-x["mins"]):
                mins_txt=f"{p['mins']} mins" if p['mins'] else "No minutes data"
                st.markdown(f"""<div class="player-card">
                    <b style="font-size:15px">{p['name']}</b>&nbsp;&nbsp;{tier_badge(p['tier'])}
                    <div style="color:#888;font-size:12px;margin-top:5px">
                        Age {p.get('age','—')} &nbsp;·&nbsp; {p.get('nationality','')} &nbsp;·&nbsp; {mins_txt}
                    </div></div>""",unsafe_allow_html=True)
        else:
            st.info("No players found for this position.")

        st.markdown("---")
        st.markdown("<div class='section-title'>🔍 Scout Suggestions</div>",unsafe_allow_html=True)
        archs=POSITION_ARCHETYPES.get(sel,["Balanced"])
        tabs=st.tabs(archs)
        for tab,arch in zip(tabs,archs):
            with tab:
                st.markdown(f"""<div style="background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.1);
                     border-radius:10px;padding:24px;text-align:center">
                    <div style="font-size:32px">🏗️</div>
                    <div style="margin-top:10px;font-size:14px">
                        <b style="color:#fff">{arch}</b> suggestions<br>
                        <span style="font-size:12px;color:#888">stats engine connecting...</span>
                    </div></div>""",unsafe_allow_html=True)

# ── ROUTER ────────────────────────────────────────────────────────────────────
if   st.session_state.page=="league_select": page_league_select()
elif st.session_state.page=="team_select":   page_team_select()
elif st.session_state.page=="formation":     page_formation()
