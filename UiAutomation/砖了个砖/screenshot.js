if(!requestScreenCapture()) { // 请求截图权限
    toast("请求截图失败！");
    exit();
}

function fill_zero(num) {
    if (num < 10) {
        return "0" + num;
    }
    return num;
}

function get_format_time() {
    time = new Date();   // 获取当前时间
    year = time.getFullYear()
    month = fill_zero(time.getMonth() + 1)
    day = fill_zero(time.getDate())
    hour = fill_zero(time.getHours())
    minute = fill_zero(time.getMinutes())
    second = fill_zero(time.getSeconds())
    return year + month + day + '_' + hour + minute + second
}

// img = captureScreen("/storage/emulated/0/DCIM/Camera/IMG_" + get_format_time() +".jpg");   // 保存截图到指定路径
img = captureScreen("/storage/emulated/0/DCIM/Camera/IMG_0.jpg")
sleep(2000)
app.launchApp("相册")   // 打开相册
sleep(5000)
click(100, 1000)     // 点击刚保存的截图相册
sleep(1000)
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
sleep(1000)
swipe(450, 1400, 50, 1400, 200)    // 关闭微信
sleep(1500)
click(400, 1200)    // 回到游戏界面