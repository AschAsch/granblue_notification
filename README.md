## granblue_notification（グラブル団内救援通知システム）

Twitter救援を行った際に騎空団員のTwitterアカウントへReply、DMを自動送信する仕組み

---
* Python3.6
* herokuで動作中（HerokuScheduler 10min）
* heroku -> AWS Lamda+CloudWatchEventへ以降（1min)

### 2019/12/23
* 一定時間後、公開ツイッターアカウントへ救援ツイートを自動POSTする仕組みを追加
