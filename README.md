# 2x2 Rubik's Cube Solver
教育版レゴ®マインドストーム® EV3を使った2×2ルービックキューブを自動でそろえてくれる装置「ルービックキューブソルバー」のソースコードです。

**[ルービックキューブソルバーを動かした動画](https://youtu.be/zLtCLgSnmFU)**

EV3単体で動作させることができます。
EV3単体での動作が遅い場合はPCと通信して、ルービックキューブを回す手順を計算する処理をPCに任せることができます。

<!-- ## EV3単体で動作させる場合
### 準備
1. [教育版レゴ®マインドストーム® EV3によるPythonプログラミング](https://education.lego.com/ja-jp/product-resources/mindstorms-ev3/%E5%85%88%E7%94%9F%E5%90%91%E3%81%91%E3%83%AA%E3%82%BD%E3%83%BC%E3%82%B9/ev3-python%E3%81%A7%E3%81%AE%E3%83%97%E3%83%AD%E3%82%B0%E3%83%A9%E3%83%9F%E3%83%B3%E3%82%B0)に移動し、"EV3 MicroPython micro SD card image"をダウンロードする。
2. microSDカード(4GB以上)にダウンロードしたイメージを書き込む。
3. EV3のmicroSDカードスロットに挿入し電源を入れる。
4.  -->

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