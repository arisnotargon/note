# 更新时直接发送请求提交新的字段即可更新
curl -H "Content-Type: application/json" -XPUT 'http://localhost:9200/gb/_mapping' -d '
{
  "properties":{
       "newColumn1": {
            "type": "keyword"
        }
    }
}
'