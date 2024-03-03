const { app, BrowserWindow } = require("electron")
const { ipcMain } = require("electron/main")
const fs = require('fs');

const createMainWin = () => {
    const BrowserWindow = require('electron').BrowserWindow;
    let win = new BrowserWindow({width: 1000, height: 500});
    win.loadURL("https://tenhou.net/2/?q=111m234067p88999s");

    let webContents = win.webContents;
    // console.log(webContents);

    // win.webContents.on('ready-to-show', () => {
    //     win.webContents.executeJavaScript(`
    //         alert(document.getElementsByTagName('textarea')[0].innerHTML);
    //     `)
    // })
    win.webContents.executeJavaScript(`
        document.body.innerHTML='<textarea style="width:98%;height:30em;">'+document.getElementsByTagName('textarea')[0].innerHTML;
    `)
}

app.whenReady().then(() => {
    createMainWin();
})

app.on("window-all-closed", () => {
    console.log("App quit.")
    app.quit();
})