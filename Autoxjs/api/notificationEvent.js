events.observeNotification();
events.on("notification", function(n){
    log("应用包名: " + n.getPackageName())
    log("通知文本：" + n.getText())
    log("通知优先级：" + n.priority)
    log("通知目录：" + n.category)
    log("通知时间：" + new Date(n.when))
    log("通知数：" + n.number)
    log("通知摘要：" + n.tickerText)
})