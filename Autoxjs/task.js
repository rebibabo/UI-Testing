文章个数 = 10

function my_click(widget) {
    let x = widget.bounds().centerX()
    let y = widget.bounds().centerY()
    // click(x, y)
    press (x, y, 200) //或者
}

function open_app() {
    app.launch('com.tencent.mm')
    sleep(1000)
    click(763, 1870)
    sleep(1000)
    click(400, 2244)
    sleep(1500)
    my_click(text("广州铁路企业号").findOne().parent())
    sleep(1500)
    my_click(id("awx").className("android.widget.TextView").text("单位头条").findOne())
    className("android.view.View").text("全部栏目").waitFor()
    sleep(2000)
}

function like_and_share() {
    while (true) {
        var template = images.read('/storage/emulated/0/Pictures/like.png.jpg')
        var p = findImage(captureScreen(), template)
        if (p) {
            sleep(5000)
            var template = images.read('/storage/emulated/0/Pictures/like.jpg')
            var _p = findImage(captureScreen(), template)
            if (!_p) {
                click(p.x, p.y)
            }
            else {
                click(p.x, p.y)
                sleep(1000)
                click(p.x, p.y)
            }
            break
        } else {
            var template = images.read('/storage/emulated/0/Pictures/like.jpg')
            var p = findImage(captureScreen(), template)
            if (p) {
                click(p.x, p.y)
                sleep(1000)
                click(p.x, p.y)
                break
            }
            else {
                swipe(540, 1800, 540, 500, 500)
                sleep(1000)
            }
        }
    }

    click(1000, 220)
    sleep(1000)
    text("分享到朋友圈").findOnce().parent().click()
    sleep(1500)
    back()
}

function main() {
    if (!requestScreenCapture()) {
        toast("请授予应用权限")
        exit()
    }
    // open_app()
    var num = 0
    while (true) {
        var ys = []
        var node = className("android.widget.FrameLayout").findOnce()
        path = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0]
        for (var i = 0; i < path.length; i++) {
            node = node.child(path[i])
        }
        for (var i = 1; i < 文章个数 + 1; i++) {
            var n = node.child(i)
            if (n.bounds().centerY() > 540 && n.bounds().centerY() < 2340) {
                ys.push(n.bounds().centerY() - 100)
            }
        }
        log(ys)
        var flag = false
        for (var i = 0; i < ys.length; i++) {
            click(500, ys[i])
            like_and_share()
            sleep(1000)
            back()
            sleep(1000)
            num += 1
            if (num >= 文章个数) {
                flag = true
                break
            }
        }
        if (flag) {
            break
        }
        swipe(500, 2200, 500, 580, 1000)
        sleep(1000)
    }
}

// main()
like_and_share()