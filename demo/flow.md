# Flow Demo

@[flow](direction: Vertical)
df（全データ）
 → groupby("track_genre", as_index=False) でジャンルごとに分割
 → ["popularity"] で集計対象の列を絞り込む
 → mean() で各グループの平均を計算
 → sort_values("popularity", ascending=False) で降順に並べ替え
 → head(10) で上位10ジャンルを抽出
@[/flow]

@[flow: Horizontal Flow]
A -> B -> C -> D -> E
@[/flow]
