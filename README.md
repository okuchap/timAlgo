# timAlgo

松島先生主催の[メカニズムデザイン勉強会](http://www.econexp.org/hitoshi/AMFmeeting.htm)で、
Stanford CS DepartmentのTim Roughgardenによる講義["A Second Course in Algorithms"](http://theory.stanford.edu/~tim/w16/w16.html)のレクチャーノートを読むので、その成果物を挙げていきます。講義に出てきたアルゴリズムをちまちま実装していけたらなあ、と思っています。

"*Ch\*\*.ipynb*"というファイルが、第\*\*回の講義に対応したノートになっています。

## 使用言語とか環境とか
Python 3系 + Jupyter Notebook を主に使います。
ノートを見たり、編集したりするのには、Pythonやその周りの諸々を導入する必要があります。
導入は、Anacondaを用いると良いと思います。[尾山ゼミのgithubページ](https://github.com/OyamaZemi/StudyNotes/blob/master/README.md)に解説があります。

グラフ系のアルゴリズムを実装する際には、[NetworkX](https://networkx.github.io/)を用いるかもしれません。

## Pythonの練習
もし、Pythonを使ったことがないor不慣れな場合は以下のサイトが参考になると思います。

[1. Google's Python Class](https://developers.google.com/edu/python/)

GoogleによるPythonの入門講義。サクッとPythonの文法を学ぶことができます。
  
[2. Problem Solving with Algorithms and Data Structures using Python](http://interactivepython.org/runestone/static/pythonds/index.html#)

Pythonの文法の解説（特に1にはないclassの解説がわかりやすいです）に加えて、基本的なアルゴリズムについて学ぶことができます。レベル的にも、"A Second Course in Algorithms"のpre-requisiteに近いと思われます。

## 参考になりそうな文献
レクチャーノートを読んでいる中でわからないものが出てきた際に、参考にできそうな文献を挙げておきます。

[1. 杉原厚吉(2001)『データ構造とアルゴリズム』共立出版](https://www.amazon.co.jp/%E3%83%87%E3%83%BC%E3%82%BF%E6%A7%8B%E9%80%A0%E3%81%A8%E3%82%A2%E3%83%AB%E3%82%B4%E3%83%AA%E3%82%BA%E3%83%A0-%E6%9D%89%E5%8E%9F-%E5%8E%9A%E5%90%89/dp/4320120345)

データ構造とアルゴリズムの入門書です。薄いのでさらっと読めます。これでprerequisiteとして指定されている内容の
大部分はカバーできると思います。

[2. Kleinberg(2005), *Algorithm Design*](https://www.amazon.com/Algorithm-Design-Jon-Kleinberg/dp/0321295358)

分厚い。[邦訳](https://www.amazon.co.jp/%E3%82%A2%E3%83%AB%E3%82%B4%E3%83%AA%E3%82%BA%E3%83%A0%E3%83%87%E3%82%B6%E3%82%A4%E3%83%B3-Jon-Kleinberg/dp/4320122178)あり。応用例などが豊富で、次に挙げるCLRSよりは読んでいて楽しそう。特に、2章「アルゴリズム解析の基礎事項」と8章「NPと計算困難性」は参考になりそう。

[3. Cormen, *et al.*(2009), *Introduction to ALgorithms*](https://www.amazon.com/Introduction-Algorithms-3rd-MIT-Press/dp/0262033844)

これも分厚い。[邦訳](https://www.amazon.co.jp/%E3%82%A2%E3%83%AB%E3%82%B4%E3%83%AA%E3%82%BA%E3%83%A0%E3%82%A4%E3%83%B3%E3%83%88%E3%83%AD%E3%83%80%E3%82%AF%E3%82%B7%E3%83%A7%E3%83%B3-%E7%AC%AC3%E7%89%88-%E7%B7%8F%E5%90%88%E7%89%88-%E4%B8%96%E7%95%8C%E6%A8%99%E6%BA%96MIT%E6%95%99%E7%A7%91%E6%9B%B8-%E3%82%B3%E3%83%AB%E3%83%A1%E3%83%B3/dp/476490408X)あり。昔から定評のある教科書らしいです。（多分アルゴリズム版マスコレルみたいな感じです）CLRSと略されてたりします。

[4. 藤重悟(2002)『グラフ・ネットワーク・組合せ論』共立出版](https://www.amazon.co.jp/%E3%82%B0%E3%83%A9%E3%83%95%E3%83%BB%E3%83%8D%E3%83%83%E3%83%88%E3%83%AF%E3%83%BC%E3%82%AF%E3%83%BB%E7%B5%84%E5%90%88%E3%81%9B%E8%AB%96-%E5%B7%A5%E7%B3%BB%E6%95%B0%E5%AD%A6%E8%AC%9B%E5%BA%A7-18-%E8%97%A4%E9%87%8D-%E6%82%9F/dp/4320016173)

グラフ理論についての教科書。2章がレクチャーノート前半部分の内容をカバーしています。
