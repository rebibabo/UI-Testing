if(!requestScreenCapture()) { // 请求截图权限
    toast("请求截图失败！");
    exit();
}
img = captureScreen("/storage/emulated/0/DCIM/Camera/0.png");   // 保存截图到指定路径
sleep(2000)
app.launchApp("相册")   // 打开相册
sleep(1000)
click(100, 700)     // 点击刚保存的截图相册
className("android.widget.LinearLayout").desc("发送").findOne().click()  // 点击发送按钮
sleep(1000)
id("chooser_icon").className("android.widget.ImageView").desc("微信").findOne().click() // 选择发送到微信
sleep(2000)
text("文件传输助手").id("ou7").findOne().parent().click()
sleep(1000)
id("mm_alert_ok_btn").findOne().click() // 点击发送按钮
sleep(4000)
swipe(500, 2600, 500, 2000, 500)    // 进入最近任务窗口
sleep(1000)
swipe(450, 1400, 50, 1400, 200)    // 关闭微信