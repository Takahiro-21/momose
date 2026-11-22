---
name: hanakoya-nouhinsho-pdf
description: ㈱はなこや宛の納品書スプレッドシートを、納品書シート1枚ずつPDFにして info@hanakoya.com 宛のメールにまとめる。「はなこやの納品書をPDFにして送って」「納品書送付」などで使う。
---

# はなこや 納品書PDF送付

納品書を作るたびに行う定型作業。

## 手順

1. **スプレッドシートを探す**: Google Drive で `title contains 'はなこや納品書'`（Googleスプレッドシート）を検索し、
   今月の「㈱はなこや納品書R{和暦年}.{月}月分」を使う。月の指定がなければ最新のものを使う。
2. **シート一覧を取る**: `get_spreadsheet`（fields: sheets.properties.title）。
   送るのは「{月}月NO.x」のシートだけ。**受付データ・原紙・読み取りメモは送らない。**
3. **「読み取りメモ」を確認する**: 未確認の項目が残っていれば、送る前にユーザーに伝える。
4. **PDFにする**: Drive の `download_file_content`（exportMimeType: application/pdf）でファイル全体をPDFに書き出し、
   scratchpad にコピーしてから `split_sheets.py` で1シート＝1PDFに分ける:
   `python3 -I .claude/skills/hanakoya-nouhinsho-pdf/split_sheets.py all.pdf out はなこや納品書R8.11月分`
   出力ページ数とシート数が合っているか確認する。
5. **今回送る分を決める**: Gmail で `to:info@hanakoya.com subject:納品書添付` の送信済みを検索し、
   今月すでに送ったNO.は除く（ユーザーが「全部」と言えば全部）。
6. **下書きを作る**（送信はユーザーが確認してから。勝手に送らない）:
   - 宛先: info@hanakoya.com
   - 件名: 【納品書添付の件】　ファッションリフォーム・モモセです
   - 本文:
     ```
     株式会社 はなこや 御中

     お世話になっております。
     R{年}年{月}月度 納品書NO {最初} 〜 NO {最後} を添付いたします。
     ご確認よろしくお願いいたします。
     ```
   - `includeSignature: true`、添付はNO.の小さい順。
7. ユーザーに下書きリンク・添付したNO.・読み取りメモの残りを報告し、送信してよいか確認する。

## 注意
- 送信元は info2@momose-fr.com。月末には別途「{月}月度 ご請求書のご送付の件」メールがある（このスキルの対象外）。
- 1シートが2ページ以上になる場合、split_sheets.py は1ページ目しか取らないので、ページ数を必ず確認する。
