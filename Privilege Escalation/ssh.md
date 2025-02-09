## Search
- Secureフォルダ等に`.png`があった場合に`strings`コマンドで秘密鍵等がmつかる可能性がある。
## execution
#### ファイル作成・実行
- `cat << EOF > test_rsa`
- `ssh -i test_rsa user@<ip>`
