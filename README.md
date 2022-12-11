## OlivaBiliLive
> 原OlivaBiliLiveBot

可插件化管理的B站直播间机器人

目前机器人可以执行
- 发送弹幕
- 禁言用户 (需要房管权限)
- 全局禁言 (需要房管权限)
- 新增屏蔽字 (需要房管权限)
- 删除屏蔽字 (需要房管权限)


__WebSocket 库:  [xfgryujk/blivedm](https://github.com/xfgryujk/blivedm)__


### 使用 Docker 运行

此运行方式需要熟悉Docker环境

1. 下载源码
2. 使用 docker build 建置 image
3. 使用 docker run 运行

你可能需要预先扫描二维码並复制 data/session.json 以略过在 docker container 内扫描


### 参考

- [blivedm](https://github.com/xfgryujk/blivedm)
- [bilibili-API-collect](https://github.com/SocialSisterYi/bilibili-API-collect)