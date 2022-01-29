# 2x2 Rubik's Cube Solver
教育版レゴ®マインドストーム® EV3を使った2×2ルービックキューブを自動でそろえてくれる装置「ルービックキューブソルバー」のソースコードです。

**[ルービックキューブソルバーを動かした動画](https://youtu.be/zLtCLgSnmFU)**

EV3単体で動作させることができます。
EV3単体での動作が遅い場合はPCと通信して、ルービックキューブを回す手順を計算する処理をPCに任せることができます。

## EV3単体で動作させる場合
### 準備
1. [教育版レゴ®マインドストーム® EV3によるPythonプログラミング](https://education.lego.com/ja-jp/product-resources/mindstorms-ev3/%E5%85%88%E7%94%9F%E5%90%91%E3%81%91%E3%83%AA%E3%82%BD%E3%83%BC%E3%82%B9/ev3-python%E3%81%A7%E3%81%AE%E3%83%97%E3%83%AD%E3%82%B0%E3%83%A9%E3%83%9F%E3%83%B3%E3%82%B0)に移動し、"EV3 MicroPython micro SD card image"をPCにダウンロードする。
2. microSDカード(8GB以上推奨)にダウンロードしたイメージを書き込む。
3. EV3のmicroSDカードスロットに挿入し電源を入れる。
4. [LEGO Mindstorms×AI　機械学習その1　環境構築編](https://qiita.com/Hiroki-Fujimoto/items/6ce278411ca151fee750#visual-studio-code%E3%81%AE%E3%83%80%E3%82%A6%E3%83%B3%E3%83%AD%E3%83%BC%E3%83%89)を参考にPCにVisual Studio Codeをインストールし、拡張機能を導入する。
5. PCとEV3間をケーブルで接続し、このリポジトリのEV3フォルダ内のファイルをEV3に転送する。
6. [Connecting to the Internet via USB](https://www.ev3dev.org/docs/tutorials/connecting-to-the-internet-via-usb/)を参考にEV3をインターネットに接続し、PCからEV3へssh接続する。
7. Pythonのライブラリ`numpy`とC言語のコンパイラを導入する。
8. EV3内にある`rcSolver.c`をコンパイルする(出力ファイル名は`rcSolver.out`)。

### 実行方法
1. PCからEV3へssh接続して2×2ルービックキューブをルービックキューブソルバーにセットする。
2. `main_NotConnection.py`を実行し、`Ready. Solve?`の表示が出たら`y`と入力する。

## PCとEV3を接続する場合
### 準備
1. 計算を任せるPCにPython3とC言語のコンパイラを導入し、Pythonにはライブラリ`numpy`と`matplotlib`を導入する。
2. PC上でこのリポジトリの`PC/rcSolver.c`をコンパイルする。
3. 出力ファイル名に合わせて`PC/Identify_Solve.py`の239行目`run(['./rcSolver.exe', cp_str, co_str])`の実行ファイル名を書き換える。
4. 「EV3単体で動作させる場合」の1.～4.を実行する。
5. [LEGO Mindstorms×AI　機械学習その1　環境構築編](https://qiita.com/Hiroki-Fujimoto/items/6ce278411ca151fee750#pc%E3%81%A8ev3%E3%81%AEbluetooth%E6%8E%A5%E7%B6%9A)を参考にPCとEV3をBluetooth接続する。
6. [LEGO Mindstorms×AI　機械学習その2　線形回帰編](https://qiita.com/Hiroki-Fujimoto/items/6dae8c407e56a38625cf#pc-ev3%E9%96%93%E3%81%AEbluetooth%E6%8E%A5%E7%B6%9A%E3%81%AB%E5%88%A9%E7%94%A8%E3%81%97%E3%81%A6%E3%81%84%E3%82%8Bip%E3%82%A2%E3%83%89%E3%83%AC%E3%82%B9%E3%82%92%E8%AA%BF%E3%81%B9%E3%82%8B)を参考にPC-EV3間のBluetooth接続に利用しているIPアドレスを調べる。
7. `EV3/main.py`の19行目(`s.connect(('xxx.xxx.xxx.xxx', 50010))`)と`PC/Identify_Solve.py`の195行目`s.bind(('xxx.xxx.xxx.xxx', 50010))`IPアドレス部分を調べたものに書き換える。
8. 「EV3単体で動作させる場合」の5.を実行する(ケーブルでPCとEV3を接続する必要はない)。

### 実行方法
1. PCからEV3へssh接続して2×2ルービックキューブをルービックキューブソルバーにセットする。
2. PC側の`Identify_Solve.py`を実行する。
3. `Start program...`の表示が出たことを確認したのち、EV3側の`main_NotConnection.py`を実行し、`Ready. Solve?`の表示が出たら`y`と入力する。

## 各ファイルが何の役割を持っているのか
### EV3フォルダ
* main.py [EV3単体で動作させるときのみ使用] ルービックキューブソルバーを起動するときに最初に走らせる。
* main_NotConnection.py [PCと通信するときのみ使用] ルービックキューブソルバーを起動するときに最初に走らせる。
* rcReader.py ルービックキューブの色を調べる。
* ColorClustering.py 読み込まれた色データからクラスタリングによって色を6色に識別する。
* kmeans_initSet.py クラスタリングをするための関数を提供する。
* rcSolver.c [EV3単体で動作させるときのみ使用] 与えられたキューブの状態から、ルービックキューブを揃える手順を計算する。
* WayOriConverter.py [EV3単体で動作させるときのみ使用] 求めた手順をルービックキューブソルバーが動かせるように変換する。
* afterSolve.py ルービックキューブソルバーが動かせるように変換した手順を求めた後にrcMoverへ手順を投げる。
* rcMover.py 与えられた手順通りにルービックキューブを回す。

### PCフォルダ
* Identify_Solve.py ルービックキューブソルバーを起動するときに最初に走らせる。
* kmeans_initSet.py EV3フォルダにあるものと同じ
* rcReader.py EV3フォルダにあるものと同じ
