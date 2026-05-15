import pandas as pd
from io import StringIO

def load_html(path):
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()
    tables = pd.read_html(StringIO(html), header=1)
    df = tables[0].copy()
    df = df[df['Player'] != 'Player'].reset_index(drop=True)
    return df

def get_player_stats():
    print("Reading local HTML files...")

    standard   = load_html('data/standard.html')
    defense    = load_html('data/defense.html')
    possession = load_html('data/possession.html')
    passing    = load_html('data/passing.html')

    # ── Pick only the columns we need ──
    std = standard[['Player','Nation','Pos','Squad','Comp','Age','MP','Min']].copy()

    dfn = defense[['Player','Squad','Tkl','TklW','Int','Clr','Blocks']].copy()

    pos = possession[['Player','Squad','Carries','PrgDist','1/3']].copy()
    pos = pos.rename(columns={'1/3': 'PrgCarries_1_3'})

    pas = passing[['Player','Squad','Ast','KP','CrsPA']].copy()

    # ── Merge on Player + Squad to avoid duplicate name issues ──
    merged = std.merge(dfn, on=['Player','Squad'], how='left') \
               .merge(pos, on=['Player','Squad'], how='left') \
               .merge(pas, on=['Player','Squad'], how='left')

    # ── Convert numeric columns ──
    num_cols = ['MP','Min','Tkl','TklW','Int','Clr','Blocks',
                'Carries','PrgDist','PrgCarries_1_3','Ast','KP','CrsPA']
    for col in num_cols:
        merged[col] = pd.to_numeric(merged[col], errors='coerce')

    # ── Filter defenders only ──
    defenders = merged[merged['Pos'].str.contains('DF', na=False)].copy()

    # ── Save ──
    merged.to_csv('data/all_players.csv', index=False)
    defenders.to_csv('data/fullbacks.csv', index=False)

    print(f"✅ All players: {len(merged)}")
    print(f"✅ Defenders:   {len(defenders)}")
    print(defenders[['Player','Squad','Pos','Min','Tkl','Int','CrsPA']].head(15))
    return merged, defenders

if __name__ == "__main__":
    all_players, defenders = get_player_stats()