# 百灵推送

核心推送服务，支持leancloud，firebase，邮件与短信推送。

## API

启动项目后，访问 <http://127.0.0.1:8000/docs>

## 单元测试

### 复制环境变量

```shell
> cp .env.example .env
```

### 执行单元测试

```shell
> make test
```

## 本地压测结果

### 启动服务器

```shell
uvicorn braun.main:app --host 0.0.0.0 --port 8000 --workers 8
```

### POST /job 压测

```shell
> wrk -t4 -c2000 -d60s --script=benchmark/add_job_android.lua --latency http://127.0.0.1:8000/job
Running 1m test @ http://127.0.0.1:8000/job
  4 threads and 2000 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency   679.00ms  487.81ms   2.00s    66.81%
    Req/Sec   688.95    426.96     2.35k    66.28%
  Latency Distribution
     50%  621.71ms
     75%  934.01ms
     90%    1.40s 
     99%    1.92s 
  132624 requests in 1.00m, 21.50MB read
  Socket errors: connect 0, read 5498, write 274, timeout 10212
Requests/sec:   2206.69
Transfer/sec:    366.35KB
```

### PUT /job/{job_id}/report 压测

```shell
> wrk -t4 -c2000 -d60s --script=benchmark/arrive_device.lua --latency http://127.0.0.1:8000/job/f1b5a1b4c1a54991a6c86a136f4103a1/report                                           15:31:43
Running 1m test @ http://127.0.0.1:8000/job/f1b5a1b4c1a54991a6c86a136f4103a1/report
  4 threads and 2000 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency     1.03s   442.97ms   2.00s    66.21%
    Req/Sec   421.29    205.06     1.35k    68.65%
  Latency Distribution
     50%    1.01s 
     75%    1.33s 
     90%    1.66s 
     99%    1.96s 
  94163 requests in 1.00m, 11.49MB read
  Socket errors: connect 0, read 2877, write 556, timeout 11374
Requests/sec:   1567.30
Transfer/sec:    195.91KB
```
