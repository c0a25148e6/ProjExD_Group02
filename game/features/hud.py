"""HUD機能(担当:
"""

from __future__ import annotations

from typing import Any

from game.core import Feature, FPSGame


class Hud(Feature):


    name = "HUD"

    def setup(self, game: FPSGame) -> None:
        self.kills = 0
        self.log_text = ""
        self.log_timer = 0.0
        game.on("enemy_defeated", self.on_enemy_defeated)

    def on_enemy_defeated(self, data: dict[str, Any]) -> None:
        self.kills += 1
        self.log_text = "+100"
        self.log_timer = 2.0

    def update(self, game: FPSGame, dt: float) -> None:
            if self.log_timer > 0:
                self.log_timer -= dt

    def draw_hud(self, game: FPSGame, screen: Any) -> None:
        
        hp = game.player.health
        
        if hp <= 25:
            if int(game.time * 4) % 2 == 0:
                game.draw_bar(20, 44, game.player.health, game.player.max_health, color=(255, 0, 0), label="HP") # 赤いHPバーを描く
                pass
        elif hp <= 50:
                game.draw_bar(20, 44, game.player.health, game.player.max_health, color=(255, 255, 0), label="HP") # 黄色いHPバーを描く
                pass
        else:
                game.draw_bar(20, 44, game.player.health, game.player.max_health, color=(230, 70, 60), label="HP")# 通常色のHPバーを描く
                pass        
        
        game.draw_bar(20, 96, game.player.ammo, game.player.max_ammo, color=(80, 160, 255), label="弾薬")
        game.draw_text(f"スコア {game.score}", 20, 122, size=22)
        game.draw_text(f"撃破数 {self.kills}", 20, 150, size=22)
        
        if self.log_timer > 0:
            game.draw_text(self.log_text, 20, 180, size=22, color=(255, 255, 100)) # self.log_text を画面に表示する
            pass       
        
        if hasattr(game, "map") and game.map:
            map_rows = len(game.map)
            map_cols = len(game.map[0])
            
            # 右上に配置するための開始座標を計算 (画面右端からマップの横幅+余白20pxを引く)
            start_x = game.width - (map_cols * 8) - 20
            start_y = 20
            
            # プレイヤーのいるマス（行・列）を取得
            p_row, p_col = game.world_to_cell(game.player.x, game.player.z)
            
            # マップ配列をループ処理して1マスずつ描画
            for r in range(map_rows):
                for c in range(map_cols):
                    cell_type = game.map[r][c]
                    
                    # 空白以外の文字（壁など）はグレー、通路は濃いグレーで色分け
                    if cell_type != "#":
                        color = (120, 120, 120)  # 壁の色
                    else:
                        color = (40, 40, 40)     # 道の色
                    
                    # 実際の描画位置を計算して四角形を描画
                    x = start_x + (c * 8)
                    y = start_y + (r * 8)
                    game.draw_rect(x, y, 8, 8, color)
                    
                    # もし現在のマスがプレイヤーの位置なら、緑色で上書き描画
                    if r == p_row and c == p_col:
                        game.draw_rect(x, y, 8, 8, (0, 255, 0)) 
        
        target = game.aim_target()
        if target is not None:
            name = target.name
            enemy_hp = target.data.get("hp", "???")  # 安全にHPを取得（なければ"???"）
            
            # 画面中央の少し上の座標を計算
            center_x = game.width // 2
            center_y = game.height // 2 - 60
            
            # 敵の名前とHPを画面に描画 (少し左にずらして中央に寄せます)
            game.draw_text(name, center_x - 40, center_y, size=22, color=(255, 50, 50))
            game.draw_text(f"HP: {enemy_hp}", center_x - 40, center_y + 26, size=18, color=(255, 255, 255))
        
        game.draw_text(
            "WASD移動 / Shiftダッシュ / マウス視点 / 左クリック射撃 / ESC終了",
            20,
            game.height - 36,
            size=18,
            color=(160, 168, 180),
        )
