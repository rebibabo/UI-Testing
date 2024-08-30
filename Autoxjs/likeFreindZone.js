var day = 3; // 最多点到几天前的朋友圈

function my_click(widget) {
    let x = widget.bounds().centerX()
    let y = widget.bounds().centerY()
    click(x, y)
}

if (!requestScreenCapture()) {
    toast("请求截图失败")
    exit()
}

function check() {
    var template = images.read('/storage/emulated/0/Pictures/like.jpg')
    var p = findImage(captureScreen(), template)
    if (p) {
        return true
    } else {
        var template = images.read('/storage/emulated/0/Pictures/like2.jpg')
        var p = findImage(captureScreen(), template)
        if (p) {
            return true
        } else {
            return false
        }
    }
}

app.launch("com.tencent.mm")
id("icon_tv").className("android.widget.TextView").text("发现").findOne().parent().parent().click()
sleep(500)
click(600, 330)
sleep(1000)

while (text(day + "天前").exists() === false) {
    var node = className("android.widget.FrameLayout").findOnce()
    var nodes = node.find(id("n9a")) // 一条朋友圈
    for (var i = 0; i < nodes.length; i++) {
        like_btn = nodes[i].findOne(id("r2"))   // 点赞按钮
        if (like_btn === null) {
            continue
        }
        var y = like_btn.bounds().centerY()
        if (y < 259 || y > device.height - 50) {
            continue
        }
        like_btn.click()
        sleep(1000)
        if (!check()) {   // 如果没有点赞
            click(600, y)
        }
        else {
            like_btn.click()
        }
        sleep(1000)
    }
    swipe(600, 2000, 600, 360, 1000)
    sleep(1500)
}