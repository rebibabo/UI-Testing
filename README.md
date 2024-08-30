# 介绍
![image](https://github.com/user-attachments/assets/7875facc-661f-4e40-a59f-a360361a5069)
![image](https://github.com/user-attachments/assets/21c2e23d-47a6-4066-b887-a19765b2b625)
![image](https://github.com/user-attachments/assets/1229b785-98f9-4c2b-bbc6-e781faa5f79f)
![image](https://github.com/user-attachments/assets/f40af0f3-66b0-40a6-9264-0b1ca4917b5d)


## Autoxjs
Autoxjs用于app自动化，文件夹里面有记录.md总结了环境的搭建以及操作的一些技巧，api中包含一些常用的api函数

- 点击指定坐标点——click.js
- 获取截图——capture.js
- 通过OCR匹配图片位置——matchPicture.js
- 监听短信消息——notificationEvent.js
- 关闭应用程序——shutdown.js

一些实际应用
- buyTicket.js——12306自动抢票
- copyCaptcha.js——监听短信验证码并发送到微信文件传输助手
- likeFreindZone.js——朋友圈自动点赞
- likeSports.js——微信步数自动点赞
- task.js——微信公众号点击任务

## Playwright
Playwright为python的一个爬虫包，下面是实际应用

- downloads.py——下载url地址的文件
- get_leetcode_problem.py——下载leetcode题目代码
- get_patent_info.py——根据用户输入的关键词，搜索专利之星所有检索信息，并下载其pdf、图片以及文本信息
- translate.py——在线和有道翻译进行交互，实时翻译

## UiAutomation
UiAutomation是一个控制电脑程序的自动化框架，下面是一些实际应用

- wechat.py——实现手机与电脑通过微信传输助手交互，微信自动回复消息
- chatRobot.py——结合LLM实现微信智能聊天助手，实现手机与Kimi的交互
- 无忧托尔——微信小程序，结合Autoxjs,scrcpy,UiAutomation，能够操作手机玩无忧托儿游戏，玩到了153分

  ![image](https://github.com/user-attachments/assets/f3573383-897e-47c0-8583-c3c1da9bf32f)

- 砖了个砖——微信小程序，同上结合Autojs,scrcpy,UiAutomation，以及蒙特卡洛树搜索算法，玩到了第34层
  
  ![image](https://github.com/user-attachments/assets/0dce4552-8f00-4f95-8558-2b789c3c4967)

