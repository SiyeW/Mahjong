function mainFrameLoad(){
    // var mainFrame = document.getElementById('mainFrame');
    // var content = mainFrame.contentWindow.document.getElementsByTagName('table')[0];
    // document.getElementById('showingDiv').innerHTML = content;
}

const { ipcRenderer } = require("electron");

function readFile(path = 'cards') {
	return ipcRenderer.sendSync("readFileSync", path);
}
// ipcRenderer.on('readFileSyncReturn', (ev, data) => {//接收回复
// 	networkData = data;
// 	console.log(networkData);
// })

function checkFile(){
    var newCards = readFile();
    console.log(newCards)
    if(newCards!==cards){
        // document.getElementById('mainFrame').src="https://tenhou.net/2/?q="+newCards;
        document.getElementById('mainFrame').src="https://tool.liumingye.cn/majiang/dapai.html#"+newCards;
        cards = newCards;
    }
}

var cards;
window.setInterval(checkFile,200);