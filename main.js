const { app, BrowserWindow } = require('electron')
const { ipcMain } = require("electron/main")
const fs = require('fs');

const createWindow = () => {
    let win = new BrowserWindow({
        show:false,
        width: 1200,
        height: 800,
        webPreferences: {
            nodeIntegration: true,
            enableRemoteModule: true,
            contextIsolation: false
        }
    })
    win.loadFile('index.html')
    win.on("ready-to-show", () => {
        win.show();
    })
    win.on("close", () => {
        win = null;
    })
}

app.whenReady().then(() => {
    createWindow()
})

app.on('window-all-closed', () => {
    console.log("Quit")
    app.quit()
})

ipcMain.on('readFileSync', (event, path) => {
    try {
        const data = fs.readFileSync(path, 'utf8');
        event.returnValue = data;
    } catch (err) {
        console.error(err);
        event.returnValue = false;
    }
})