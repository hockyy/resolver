# TLX-Resolver


This project forked from [acm-resolver](https://github.com/lixin-wei/acm-resolver), which is used to roll the list of ACM series competitions.

Compared with the original project, the animation efficiency is mainly optimized, the color of the interface is changed, and the document is enriched, the color is also changed and the features are being improved.

## To run

### Build

```bash
docker build --tag cf12-resolver .
docker run --detach --publish 9001:80 --name cf12-resolver cf12-resolver:latest
```

### JSON structure

```
{
  problem_count: 10,
  solutions: {... },
  users: {... }
}
```

### solutions

```
381503: {
  user_id: "1",
  problem_index: "1",
  verdict: "AC",
  submitted_seconds: 22
},
381504: {
  user_id: "2",
  problem_index: "1",
  verdict: "WA",
  submitted_seconds: 23
},
```

### users

```
1: {
  name: "花落人亡两不知",
  college: "HZNU",
  is_exclude: true
},
2: {
  name: "大斌丶凸(♯｀∧´)凸",
  college: "HDU",
  is_exclude: false
},
3: {
  name: "天才少女队",
  college: "PKU",
  is_exclude: true
},
```

