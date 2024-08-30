function my_click(name, time) {
    widget = desc(name).findOne()
    let x = widget.bounds().centerX()
    let y = widget.bounds().centerY()
    // 如果 x 的坐标小于0或者大于1200，说明要左滑或者右滑
    while (x < 0 || x > 1200) {
        console.log(x)
        if (x < 0) {
            swipe(100, y, 800, y, 100)
        } else {
            swipe(800, y, 100, y, 100)
        }
        widget = desc(name).findOne()
        x = widget.bounds().centerX()
        y = widget.bounds().centerY()
    }
    // longClick(x, y)
    console.log(x)
    sleep(1000)
    press(x, y, time) //或者
}

function shutdown(name) {
    my_click(name, 1000)
    sleep(1000)
    id("item_title").className("android.widget.TextView").text("应用信息").findOne().parent().click()
    sleep(1000)
    if (className("android.widget.LinearLayout").desc("结束运行").findOne().enabled()) {
        className("android.widget.LinearLayout").desc("结束运行").findOne().click()
        sleep(1000)
        click(700, 2400)
        sleep(1000)
    }
    home()
}

function shutdown_all() {
    while (id("clearAnimView").exists() === false) {
        recents()
        sleep(500)
        if (className("android.widget.TextView").text("近期没有任何内容").exists()) {
            home()
            return
        }
    }
    id("clearAnimView").findOne().click()
    home()
}

home()
// shutdown_2("安全服务 应用信息")
shutdown("CSDN")
// exit()