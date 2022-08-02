# es的一些基础用法
## 主要参考资料
官方教程es权威指南： https://www.elastic.co/guide/cn/elasticsearch/guide/current/index.html

# 安装
## 运行es的服务容器
首先安装docker和docker-compose，然后写入本目录中的docker-compose.yml文件。
首先启动其中的elasticsearch容器，执行：
``` bash
docker-compose up -d elasticsearch
```
等待镜像拉取，容器启动，在浏览器地址栏输入http://127.0.0.1:9200/ 如果看到自述内容说明启动成功，例如：
``` json
{
  "name" : "ff786a59905f",
  "cluster_name" : "elasticsearch",
  "cluster_uuid" : "U178gbE-RG6knzb8CoZ8AA",
  "version" : {
    "number" : "7.7.0",
    "build_flavor" : "default",
    "build_type" : "docker",
    "build_hash" : "81a1e9eda8e6183f5237786246f6dced26a10eaf",
    "build_date" : "2020-05-12T02:01:37.602180Z",
    "build_snapshot" : false,
    "lucene_version" : "8.5.1",
    "minimum_wire_compatibility_version" : "6.8.0",
    "minimum_index_compatibility_version" : "6.0.0-beta1"
  },
  "tagline" : "You Know, for Search"
}
```
如果启动失败可以使用如下命令查看容器标准输出的日志进行调试
``` bash
docker logs <tag>
```

## 运行kibana的容器
通过以下命令获取es容器的信息
```bash
docker inspect <tag>
```
找到输出结果中的NetworkSettings.Networks，其中会有该容器在docker虚拟网络中的ip，IPAddress的值就是，接下来创建kibana.yml文件，其中的elasticsearch.hosts设置为刚刚查到的ip地址，然后使用如下命令来启动kibana的容器
``` bash
docker-compose up -d kibana
```
等待镜像拉取，容器启动，在浏览器地址栏输入http://127.0.0.1:5601/ 如果看到kibana的应用页面则说明启动成功

# 插入
es的交互通过http经由的rest接口实现，以下交互如无特殊说明均可通过kibana或curl工具进行调试

es插入数据前无需进行数据定义，可直接通过put或post请求进行插入，例如：
``` bash
curl -X PUT "localhost:9200/megacorp/employee/1?pretty" -H 'Content-Type: application/json' -d'
{
    "first_name" : "John",
    "last_name" :  "Smith",
    "age" :        25,
    "about" :      "I love to go rock climbing",
    "interests": [ "sports", "music" ]
}
'
```
其中uri中最后一个path为id（1），重复插入相同的id的话会得到新的version，对于未定义的类型可以使用如下的path代替：
```
(/{index}/_doc/{id}, /{index}/_doc, or /{index}/_create/{id})
```

# 准备测试数据
## 创建mapping

mapping类似关系型数据库中的表结果定义（DDL），虽然es中无需创建mapping也可以使用（es会自动创建），但为了方便管理，提高使用效率，在准备数据前最好先创建mapping（尤其是生产环境中）
### mapping中的类型
分为简单类型和复杂类型，用于搜索的数据尽可能使用简单类型
#### 简单类型
+ Text/Keyword
+ Date
+ Integer/Float/Double/Long
+ Boolean
+ Ip

Text/Keyword在早期版本的es中被称为string字符串，由于官方教程基于2.x的版本，这里需要注意官方教程内容已过时。

text类型的数据用来索引长文本，例如电子邮箱主体部分或者一些产品的介绍geo_point
geo_shape / percolator，这些文本会被分析，在建立索引后被分词器进行分词，转化为词组。经过分词机制后es允许检索到该文本切分而成的词语，但text类型的数据不能用来做过滤、排序、聚合等操作

keyword类型的数据可以满足电子邮箱、主机名、状态码等数据的要求，不进行分词，常常被用来做过滤、排序、聚合等操作
如果即需要分词搜索，也需要聚合排序等操作，关系型数据库中同一个字段同步到es时需要设置为text并增加keyword子字段

## 更新mapping
给mapping增加字段直接发送请求增加字段即可，见本目录中的update_mapping.sh

*注意* es中mapping的字段创建好之后无法修改和删除，如需修改删除需要删除整个mapping

#### 复杂对象和嵌套对象
主要是以json组织的对象和嵌套对象，在es中会被转化为底层的扁平结构，不建议使用，保存到关系型数据库即可，如需搜索需要自行转化为简单类型处理

#### 地理信息类型
+ geo_point
+ geo_shape / percolator

用于位置信息检索等需求

### 执行创建脚本
使用本目录中的test_mapping.sh创建mapping

## 创建测试数据
执行当前目录中的test_data.sh文件，当前指定的es主机为localhost:9200，如果不是这个主机和端口则根据实际情况调整

## 删除索引
使用DELETE请求方法删除
``` bash
curl -X DELETE "localhost:9200/us?pretty"
```

# 搜索入门
## match检索
match部分匹配，搜索字段中包含关键词时可以得到结果
``` bash
GET /gb/_search
GET /gb/_search
{
  "query": {
    "match": {
      "name": 
        "Mary"
    }
  }
}
```
## term匹配
term精准匹配，将上面的关键词用于term匹配方式时无法得出结果
``` bash
GET /gb/_search
{
  "query": {
    "term": {
      "name": 
        "Mary"
    }
  }
}
```

必须使用name.keyword字段进行搜索，且关键词与结果完全匹配才能得出搜索结果
``` bash
GET /gb/_search
{
  "query": {
    "term": {
      "name.keyword": 
        "Mary Jones"
    }
  }
}
```
term的复数形式terms可匹配对个关键词，只要其中一个符合即可命中

``` bash
GET /gb/_search
{
  "query": {
    "terms": {
      "name.keyword": 
        ["Mary Jones"]
    }
  }
}
```

## 复合搜索
同时满足name和date均为指定的值（and关系）
``` bash
GET gb/_search
{
  "query": {
    "bool": {
      "must": [
        {"term": {
      "name.keyword": 
        "Mary Jones"
        }},
        {"term": {
          "date": {
            "value": "2014-09-13"
          }
        }}
      ]
    }
  }
}
```

满足其中之一即可（or关系）
``` bash
GET gb/_search
{
  "query": {
    "bool": {
      "should": [
        {"term": {
          "date": {
            "value": "2014-09-13"
          }
        }},
        {"term": {
          "date": {
            "value": "2014-09-15"
          }
        }}
      ]
    }
  }
}
```

亦可以嵌套使用

更多高级搜索功能在官方教程： https://www.elastic.co/guide/cn/elasticsearch/guide/current/search-in-depth.html
<br>

# 聚合
聚合是es中非常重要的功能，可用于实现动态生成筛选项标签，统计等需求
## 准备实验数据
```bash
POST /cars/_bulk
{ "index": {}}
{ "price" : 10000, "color" : "red", "make" : "honda", "sold" : "2014-10-28" }
{ "index": {}}
{ "price" : 20000, "color" : "red", "make" : "honda", "sold" : "2014-11-05" }
{ "index": {}}
{ "price" : 30000, "color" : "green", "make" : "ford", "sold" : "2014-05-18" }
{ "index": {}}
{ "price" : 15000, "color" : "blue", "make" : "toyota", "sold" : "2014-07-02" }
{ "index": {}}
{ "price" : 12000, "color" : "green", "make" : "toyota", "sold" : "2014-08-19" }
{ "index": {}}
{ "price" : 20000, "color" : "red", "make" : "honda", "sold" : "2014-11-05" }
{ "index": {}}
{ "price" : 80000, "color" : "red", "make" : "bmw", "sold" : "2014-01-01" }
{ "index": {}}
{ "price" : 25000, "color" : "blue", "make" : "ford", "sold" : "2014-02-12" }
```

## 运行聚合
在请求体的顶层中输入aggs参数,例如如下请求可以获取全部颜色的聚合
``` bash
GET /cars/_search
{
    "size" : 0,
    "aggs" : { 
        "popular_colors" : { 
            "terms" : { 
              "field" : "color.keyword"
            }
        }
    }
}
```
*注意* color原始字段为text，无法进行聚合操作，应次需要使用它的keyword子字段color.keyword

## 带有统计的聚合
使用聚合时可以根据统计进行排序，例如需要根据相同颜色的总数进行倒序排列时，可以使用以下的请求：
``` bash
GET /cars/_search
{
    "size" : 0,
    "aggs" : { 
        "popular_colors" : { 
            "terms" : { 
              "field" : "color.keyword",
              "order": {
                "_count": "desc"
              }
            }
        }
    }
}
```

取每种颜色的平均价时：
``` bash
GET /cars/_search
{
   "size" : 0,
   "aggs": {
      "colors": {
         "terms": {
            "field": "color.keyword"
         },
         "aggs": { 
            "avg_price": { 
               "avg": {
                  "field": "price"
               }
            }
         }
      }
   }
}
```



