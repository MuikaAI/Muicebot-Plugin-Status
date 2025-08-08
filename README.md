<div align=center>
  <img width=200 src="https://bot.snowy.moe/logo.png"  alt="image"/>
  <h1 align="center">MuiceBot-Plugin-Status</h1>
  <p align="center">基于 nonebot_plugin_htmlrender 的 Muicebot 状态插件</p>
</div>
<div align=center>
  <a href="https://nonebot.dev/"><img src="https://img.shields.io/badge/nonebot-2-red" alt="nonebot2"></a>
  <img src="https://img.shields.io/badge/Code%20Style-Black-121110.svg" alt="codestyle">
  <a href='https://qm.qq.com/q/Q5rVU7wlag'><img src="https://img.shields.io/badge/QQ群-MuiceHouse-pink" alt="QQ群组"></a>
</div>

<details>
    <summary>效果示例</summary>
	<img src="./src/example.png" alt="example" style="zoom: 33%;" />
</details>

## 使用方式

使用 `.status` 或 `/status` 即可

## 配置项

### status__avatar_url

- 说明: bot 图像链接

- 类型: str

- 默认值: https://s2.loli.net/2025/04/20/oK6pncNCeWfIyE3.jpg

### status__backgroud_url

- 说明: 背景图片链接

- 类型: str

- 默认值: https://s2.loli.net/2025/04/20/nYN2kbs38Xc6zBj.jpg

### status__nickname

- 说明: 机器人昵称

- 类型: str

- 默认值: MuikaAI

### status__priority

- 说明: 指令优先级

- 类型: int

- 默认值: 5


## 注意

模板文件中使用了 `tailwindcss` 的 CDN 实现，而官方并不推荐这种方法且存在获取问题。

我们以后可能会更改有关实现，也欢迎您提交 PR 来帮助我们更改这个功能！