#!/bin/bash

# shellcheck disable=SC2154
jsonData="$(curl -X GET "https://api-takumi.miyoushe.com/ptolemaios_api/api/getLatestRelease" -H "x-rpc-client_type: 2" -H "x-rpc-app_version: 2.67.1" -H "x-rpc-channel: miyousheluodi" -H "x-rpc-h265_supported: 1" -H "referer: https://app.mihoyo.com" -H "x-rpc-verify_key: bll8iq97cem8" -H "x-rpc-csm_source: " -H "user-agent: okhttp/4.9.3")"
url="$(echo "$jsonData" | jq --raw-output '.data.package_url')"
curl -o mihoyobbs.apk "$url"
