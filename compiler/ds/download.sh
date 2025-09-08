#!/bin/bash

# shellcheck disable=SC2154
jsonData="$(curl -X POST 'https://yybadaccess.3g.qq.com/v2/dc_pcyyb_official' -H 'Content-Type: application/json' -d '{"head":{"cmd":"dc_pcyyb_official","authInfo":{"businessId":"AuthName"},"expSceneIds":"92215","hostAppInfo":{"scene":"game_detail"}},"body":{"bid":"yybhome","offset":0,"size":10,"preview":false,"listS":{"region":{"repStr":["CN"]},"pkgname":{"repStr":["com.mihoyo.hyperion"]}},"layout":"yybn_game_basic_info"}}')"
url="$(echo "$jsonData" | jq --raw-output '.data.components[0].data.itemData[0].download_url')"
curl -o mihoyobbs.apk "$url"
