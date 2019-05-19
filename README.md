## RADEE-2019

2019年度用リポジトリ


## COMMIT MESSAGE RULE

`commit`する際のメッセージは次のように書くことにします．

```
prefix name summary

- detail-01
- detail-02
- detail-03
```

`name`はできれば統一してください．

prefix(`add`, `update`, `fixed`, `delete`のうちどれか)については下の例を見てください．


### 例1 add
`kazuki-iwanaga`が「LEDを光らせる」機能を持つ`led.py`を書いたなら，
この時の`commit`時メッセージは

```
add kazuki-iwanaga LEDを光らせるled.pyを作成

- LEDを光らせる機能を持つled.pyを作成
```

### 例2 update
`kazuki-iwanaga`が`led.py`に「LEDを点滅させる」機能をつけたなら，
この時の`commit`メッセージは

```
update kazuki-iwanaga LEDを点滅させる機能を追加

- led.pyにLEDを点滅させる機能を追加
```

### 例3 fixed
`kazuki-iwanaga`が`led.py`の「LEDの点滅が止まらない」バグを修正したなら，

```
fixed kazuki-iwanaga LEDの点滅が止まらないバグを修正

- led.pyのLEDの点滅が止まらないバグを修正
```

### 例4 delete
`kazuki-iwanaga`が`led.py`を削除したなら，

```
delete kazuki-iwanaga led.pyを削除

- 不要になったのでled.pyを削除
```
