# vge_logview

VGEのジョブ情報リストファイルの簡易ビューアです。
ジョブ情報リストは、ディフォルト設定では、
vge_output/vge_joblist.csv に出力されます。

## Usage
        ./vge_logview.py job_list.csv [output.pdf]

出力ファイル output.pdf を指定すると、可視化結果をPDFとして出力します。

## 時間軸の原点について

VGEに最初のジョブリクエストが届いた時刻を0としています。
