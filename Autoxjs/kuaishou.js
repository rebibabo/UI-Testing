function open_app() {
    app.launch("com.kuaishou.nebula")
    sleep(2000)
    click(844, 2542)
    sleep(5000)
}

function sign_in() { // 签到
    click(606, 1764)
    sleep(2000)
    click(1100, 447)
    sleep(1000)
}

function my_click(widget){
    let x = widget.bounds().centerX()
    let y = widget.bounds().centerY()
    click(x, y)
}

function 领福利() {
    if (text("领福利").exists()) {
        for (var i = 0; i < 10; i++) {
            my_click(text("领福利").findOne())
            sleep(30000)
            click(477, 200)
            sleep(1000)
            click(589, 1637)
            sleep(1000)
        }
    }
}

function 抽福利() {
    if (text("抽福利").exists()) {
        my_click(text("抽福利").findOne())
        sleep(1000)
        for (var i = 0; i < 20; i++) {
            click(300, 1950)
            sleep(1000)
            if (i) {
                click(600, 1600)
                sleep(30000)
                click(477, 200)
                sleep(1000)
            }
            sleep(1000)
            click(600, 2050)
            sleep(7000)
            click(600, 1975)
            sleep(1000)
        }
    }
}
 
function main() {
    // open_app()
    // sign_in()
    swipe(600, 2300, 600, 300, 1000)
    sleep(1000)
    
}

main()