## granblue_notification（グラブル団内救援通知システム）

Twitter救援を行った際に騎空団員のTwitterアカウントへReply、DMを自動送信する仕組み

---
* Python3.6
* herokuで動作中（HerokuScheduler 10min）
* heroku -> AWS Lamda+CloudWatchEventへ以降（1min)

### 2020/01/06
* 監視対象のタイムラインをuserからhomeへ変更（複数人からのPOSTに対応）
* ユーザー情報をjson形式で保持する仕組みを追加

### 2020/01/05
* ツイートチェックの方法をfavorites/createへ変更

### 2019/12/23
* 一定時間後、公開ツイッターアカウントへ救援ツイートを自動POSTする仕組みを追加
