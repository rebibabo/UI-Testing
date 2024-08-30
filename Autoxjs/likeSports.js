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

function my_click(widget){
    let x = widget.bounds().centerX()
    let y = widget.bounds().centerY()
    click(x, y)
}

home()
sleep(1000)
shutdown_all()
sleep(3000)
while (id("jha").exists() === false) {
    app.launch("com.tencent.mm")
    console.log("launch wechat")
    sleep(1000)
}
id("jha").findOne().click()
sleep(1000)

setText("微信运动")
sleep(1000)
click(600, 400)
sleep(1000)
my_click(id("bll").findOne())
sleep(1000)
people = id("oct").findOne().parent().parent().parent().parent().parent().child(1).child(0).child(0).child(1).child(0).child(0).child(0).child(0)
my_steps = parseInt(people.child(1).child(1).child(1).child(0).child(1).text(), 10)
var last_step = 100000 
var loop_last_step = 100000 
var cnt = 0
while (true) {
    console.log("loop", cnt)
    for (var i = 0; i < people.childCount() - 1; i++) {
        if (people.child(i).childCount() !== 1) {
            step = parseInt(people.child(i).child(1).child(1).child(0).child(1).text())
            if (step !== my_steps && step < last_step) {
                last_step = step
                like_btn = people.child(i).child(1).child(1).child(1).child(0).child(1)
                my_click(like_btn)
            }
        }
    }
    console.log("swipe")
    // swipe(600, 2500, 600, 600, 3000)
    swipe(600, 2400, 600, 1300, 500)
    sleep(2000)
    people = id("oct").findOne().parent().parent().parent().parent().parent().child(1).child(0).child(0).child(1).child(0).child(0).child(0).child(0)
    if (loop_last_step === last_step) {
        cnt += 1
    } else {
        cnt = 0
    }
    if (cnt > 1 || last_step < 10000) {
        break
    }
    loop_last_step = last_step
}