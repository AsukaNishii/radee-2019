
# RaspberryPiの初回sshについて

## ディスプレイ無しでやる場合の注意点

まず，microSDカードのboot配下で次のことをする必要がある．

- `ssh`という名の空ファイルを作成
- `config.txt`に`dtoverlay=dwc2`を追記
- `cmdline.txt`内の`rootwait`と`quiet`の間に`modules-load=dwc2,g_ether`を追記

このmicroSDカードを使ってRaspberryPiを起動してPCとUSBまたはイーサケーブルで接続する．

その後，PC上で`ssh pi@raspberrypi.local`とすればsshができる．

## ssh-keyエラーを吐く場合の処理

RaspberryPiにsshする際に鍵まわりでエラーを吐くことがある．

その際には`ssh -R ネットワーク名`とすれば解決する．
(厳密にはあまりよくないが気にしない)
