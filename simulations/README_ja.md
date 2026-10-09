# シミュレーション

[English Version](README.md)

このディレクトリには、UHV構想の初期探索のための、簡単なPython 3の推定ツールが含まれている。外部の依存関係を使わず、一次近似の計算のみを意図している。工学的な主張を行う前には、試作機と現地での測定が必要である。

## 気化冷却の推定ツール

`evaporative_cooling_estimator.py`は、水の流量と蒸発効率から、冷却の出力を推計する。

```text
Q_evap = m_dot × L_v × eta_evap
```

例：

```bash
python evaporative_cooling_estimator.py --water-flow 10 --efficiency 0.7
```

単位：

* `--water-flow`：1時間あたりのリットル数
* `--efficiency`：0から1の蒸発効率
* 出力：ワットとキロワット

## 風力回収の推定ツール

`wind_recovery_estimator.py`は、補助的な風力回収の電力を推計する。

```text
P = 0.5 * rho * A * v^3 * Cp * eta
```

例：

```bash
python wind_recovery_estimator.py --area 0.1 --speed 20 --cp 0.25 --efficiency 0.7
```

単位：

* `--area`：受風面積または吸気面積（平方メートル）
* `--speed`：風速（メートル毎秒）
* `--cp`：出力係数
* `--efficiency`：0から1の、発電機と変換の効率
* 出力：ワットとキロワット

車両自身が生み出す気流については、回収した電力を、増加した空気抵抗とあわせて評価しなければならない。これは、主推進のエネルギー源ではない。

## 代表的なケースの推定ツール

`representative_case_estimator.py`は、乾燥した砂漠の道路、都市のバス路線、空港や港湾の作業車両、多湿の気候での限界、夜間や弱風での限界といった、代表的な検証シナリオについて、簡略化した冷却と水の使用量の推計を組み合わせる。

例：

```bash
python representative_case_estimator.py --case dry_desert_road --vehicles 1 --water-flow 10 --hours 1 --efficiency 0.7
```

単位：

* `--vehicles`：車両数
* `--water-flow`：車両1台・1時間あたりのリットル数
* `--hours`：運転時間
* `--efficiency`：0から1の、代表的な蒸発効率
* 出力：概念的な冷却出力と水の使用量

## 液滴の蒸発時間の推定ツール

`droplet_evaporation_time_estimator.py`は、液滴の蒸発時間について、ヒューリスティックなスクリーニング用の推計を提供する。検証済みの液滴物理モデルではない。

例：

```bash
python droplet_evaporation_time_estimator.py --diameter 20 --temperature 40 --humidity 20 --wind-speed 3
```

単位：

* `--diameter`：液滴の直径（マイクロメートル）
* `--temperature`：周囲の気温（摂氏）
* `--humidity`：相対湿度（パーセント）
* `--wind-speed`：局所的な風または気流の速度（メートル毎秒）
* 出力：推計される蒸発時間（秒）

## 水使用のシナリオ

`water_use_scenario.py`は、車両または車両群の、1日あたりおよび季節ごとの水需要を推計する。

例：

```bash
python water_use_scenario.py --vehicles 20 --water-flow 8 --hours 6 --days 90
```

単位：

* `--vehicles`：車両数
* `--water-flow`：車両1台・1時間あたりのリットル数
* `--hours`：1日あたりの運転時間
* `--days`：運転日数
* 出力：1日あたりのリットル数と、選んだ期間全体のリットル数

## 速度とエネルギーのプロファイル

`speed_energy_profile.py`は、車速の範囲にわたって、センターミストの理論上の潜熱冷却ポテンシャルと、補助的なAER-Loopの風力回収電力を比較する。冷却の値は潜熱のポテンシャルであり、検証済みの有効な冷却ではない。AER-Loopの値は補助的なものにすぎず、空気抵抗とあわせて評価しなければならない。

例：

```bash
python speed_energy_profile.py --mist-l-min 0.5 --evap-efficiency 0.7 --speed-min 20 --speed-max 80 --speed-step 10
```

CSVの例：

```bash
python speed_energy_profile.py --mist-l-min 0.5 --evap-efficiency 0.7 --csv speed_profile.csv
```

ユーザーは、Python/matplotlib、表計算ソフト、gnuplotといった外部のツールで、CSV出力をグラフ化してもよい。リポジトリのスクリプト自体は、標準ライブラリのみのままである。

## 駐車時の補助エネルギー収支

`parking_auxiliary_energy_balance.py`は、保護型の太陽電池スキンからの入力、駐車中の自然風による補助発電、待機負荷から、簡略化した1日の補助エネルギー収支を推計する。検証済みの車両充電モデルではなく、走行用の主バッテリーの充電を意味するものでもない。

例：

```bash
python parking_auxiliary_energy_balance.py --solar-area 2.0 --solar-efficiency 0.12 --solar-hours 5 --solar-irradiance 800 --wind-area 0.05 --wind-speed 4 --cp 0.15 --conversion-efficiency 0.7 --operation-hours 24 --standby-load-w 5
```

単位：

* `--solar-area`：保護された太陽電池の面積（平方メートル）
* `--solar-irradiance`：代表的な日射量（W/m^2）
* `--solar-efficiency`：代表的な保護型モジュールの変換効率
* `--solar-hours`：1日あたりの日照時間の相当値
* `--wind-area`：垂直軸のロータまたは吸気の面積（平方メートル）
* `--wind-speed`：平均的な自然風の風速（m/s）
* `--cp`：風力の出力係数
* `--conversion-efficiency`：発電機と充電変換の効率
* `--operation-hours`：風力発電と待機負荷の、1日あたりの時間
* `--standby-load-w`：補助的な待機負荷（ワット）
* 出力：Wh/日での発電量、負荷、余剰または不足

## UHVの制御ステートマシン

`uhv_control_state_machine.py`は、速度適応型のミスト許可、駐車シールドの挙動、フェイルセーフの停止条件について、簡略化した概念的な制御状態を評価する。認証された車両の安全ソフトウェアではない。

例：

```bash
python uhv_control_state_machine.py --speed-kmh 30 --temperature-c 38 --humidity 35 --visibility-ok --water-quality-ok --battery-soc 80
```

入力には、速度、温度、湿度、視認性、路面の濡れ、歩行者の接近、水質、バッテリーの状態、雨、故障フラグが含まれる。出力には、選択されたモード、ミストの許可、理由の一覧が含まれる。

## 速度ガバナンス・コントローラー

`speed_governance_controller.py`は、概念的な速度ガバナンスと生命保護の制御レイヤーを評価する。認証された車両の安全ソフトウェアではない。

例 — 歩行者と交差点がある場合の法定速度：

```bash
python speed_governance_controller.py --driver-speed-request 80 --legal-speed-limit 40 --intersection-near --pedestrian-near
```

例 — 天候に応じた安全速度：

```bash
python speed_governance_controller.py --driver-speed-request 60 --legal-speed-limit 60 --road-wet --rain
```

例 — オートバイの死角：

```bash
python speed_governance_controller.py --driver-speed-request 50 --legal-speed-limit 50 --motorcycle-blind-spot
```

入力には、運転者の速度の要求、法定速度、スクールゾーン、交差点への接近、歩行者の接近、自転車の接近、オートバイの死角、視認性、路面の濡れ、雨、インフラからの警告、センサーの故障フラグが含まれる。出力には、許可される目標速度、安全モード、警告の一覧、理由の一覧が含まれる。

これらのツールのすべての出力は、検証計画のための簡略化した推計である。証明された冷却性能、保証された都市規模での効果、あるいは向上した車両効率として示してはならない。

## 移動型ミスト冷却シミュレーター

`mobile_mist_cooling_simulator.py`は、超音波ミストを搭載した移動体のユニットが、道路や都市の回廊を運行する場合の、局所的な冷却ポテンシャルについて、例示的な推計を提供する。

CFDモデルではなく、認証された熱の予測でもない。
すべての出力は、概念的な比較のみを目的とした、仮定に基づく推計である。
工学的な主張を行う前に、現地試験が必要である。

例：

```bash
python simulations/mobile_mist_cooling_simulator.py --vehicles 100 --mist-output-lph 5 --operating-hours 8 --ambient-temp-c 40 --relative-humidity 25
```

任意の出力フラグ：`--output-markdown`、`--output-csv`、`--output-summary-json`

主な入力：`--vehicles`、`--mist-output-lph`、`--operating-hours`、`--ambient-temp-c`、`--relative-humidity`、`--wind-speed-ms`、`--road-corridor-width-m`、`--mixing-height-m`、`--evaporation-efficiency`、`--coverage-efficiency`、`--heat-loss-factor`、`--max-temp-drop-c`

## 保守に関する仮定

移動型ミスト冷却のシミュレーションは、システムが正常に動作していることを仮定している。

実際の展開では、冷却出力と水の使用量は、保守の間隔、タンクの衛生、フィルターの状態、詰まりのリスク、水質に左右される。

参照：

- [センターミストのメンテナンス周期](../docs/center_mist_maintenance_schedule.md)

---

## タンクの衛生と重力落下式の回収

移動型ミスト冷却のシミュレーションは、ミストシステムが正常に機能していることを仮定している。実際の展開では、冷却出力は、タンクの衛生、フィルターの状態、水質、詰まりのリスク、保守の間隔に左右される。

重力落下式のマイクロ水力回収は、小さな補助的な回収の構想であり、正味のエネルギー発電としてモデル化してはならない。

タンクの衛生と回収の設計の詳細については、[docs/center_mist_tank_hygiene_and_recovery.md](../docs/center_mist_tank_hygiene_and_recovery.md)を参照。

## 移動型ミスト冷却のグラフ生成ツール

`generate_mobile_mist_cooling_graphs.py`は、4つの代表的なシナリオについて、例示的な比較グラフを生成する。

1. 乾燥気候での直接のタンク補給
2. 降雨のある気候での二系統供給
3. 高湿度で蒸発が低い場合
4. 粉塵のある砂漠で、保守が制約となる場合

matplotlibが必要。出力は`images/`に保存される。

例：

```bash
python simulations/generate_mobile_mist_cooling_graphs.py
```

---

## 著者紹介

Master / inchacomusho / InchaComisho

独立した日本人の構想設計者、観察者、提案者、AIチューナー、人工叡智の定義者。  
学術的枠組み「自然補完科学」の創始者・提唱者。  
クーリングクレジット・フレームワークの定義者であり、自然冷却価値評価プロトコルの創始者・原著者。  
地球温暖化の因果構造とその完全な解決策の定義者・体系化者。

Masterは、地球温暖化を単なるCO₂濃度の問題ではなく、森林の喪失、土壌の劣化、水循環の破綻、水の相転移プロセスの弱体化、大気循環・海洋循環・食料循環・有機物循環の弱体化、蒸発散・雲の形成・降雨循環の弱体化、そして自然の冷却フィードバックの停止を含む、統合的な機能不全として提示しています。  
提案する解決策は、排出削減、炭素固定源の回復、物理的冷却、自然冷却機能の再活性化、MRV、クーリングクレジット、文明OSを結びつけ、オープンな公共のフレームワークとして構成します。

Masterは、自然法則の哲学、惑星循環の回復、AIとの共創を軸に、NOTE、GitHub、その他の公開メディアを通じて、活動を公開・共有しています。


## ライセンス

CC BY 4.0

この記事は、クリエイティブ・コモンズ 表示 4.0 国際ライセンス（CC BY 4.0）の下で公開されています。  
適切なクレジット表示を行う限り、共有、再配布、翻訳、改変、再利用が認められます。

