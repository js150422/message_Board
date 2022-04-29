
let alertText = document.getElementById('uploaded_image');
let recordQ;


const getNewRecord = async () => {
    const newData = await getNewApi();
    renderNew(newData);
};



if(alertText){
    alertText.style.color = 'red';
}

document.addEventListener('DOMContentLoaded', async () => {
    const historyData = await getHistoryApi();
    renderHistory(historyData);
});


const sample_image = document.getElementsByName('sample_image')[0]
sample_image.addEventListener('change', () =>{
    upload_image(sample_image.files[0]);
});



 function getHistoryApi(){
    return fetch("/api/history", {
        method:"GET",
    }).then(function(response){
        return response.json();
    }).then((result) => {
        historyData=result
        return historyData ;
    });

  };


 function getNewApi(){
    recordQ += 1
    if (isNaN(recordQ)){recordQ=1}
    return fetch("/api/newRecord/"+(recordQ),{
        method:"GET",
    }).then(function(response){
        return response.json();
    }).then((result) => {
        newRecord=result
        return newRecord ;
    });
  };



const upload_image = (file) => {
	// check file type
	if(!['image/jpeg', 'image/png', 'image/gif'].includes(file.type))
	{
		alertText.textContent = "只接受副檔名為JPG、PNG及GIF";
		document.getElementsByName('sample_image')[0].value = '';
        return;
    }

    // check file size (< 2MB)
    if(file.size > 2 * 1024 * 1024)
    {
    	alertText.textContent = "檔案大小請在 2 MB內";
    	document.getElementsByName('sample_image')[0].value = '';
        return;
    }

}




function send(){
    message = document.getElementById('message')
    if (message.value == ''){
        alertText.textContent = "請填入訊息";
        document.getElementsByName('sample_image')[0].value = '';
        message.value = '';
    }else{
        const data = new FormData();
        data.append('files', sample_image.files[0])
        data.append('name', sample_image.files[0].name)
        data.append('message', message.value)
        try{
            fetch("/api/upload", {
                method:"POST",
                body : data
            }).then(function(response){
                uploadResult = response
                if ('ok' in uploadResult){
                    getNewRecord()
                    alertText.textContent = '成功上傳'
                    document.getElementsByName('sample_image')[0].value = '';
                    message.value = '';

                }else{
                    alertText.textContent = '新增失敗'
                    document.getElementsByName('sample_image')[0].value = '';
                    message.value = '';
                }
            });
        } catch (err) {
            console.warn(err);
        }
    }
}


function renderHistory(historyData){
    if ('error' in historyData){
        alertText.textContent = historyData["error"]
    }else{
        recordQ = historyData["record"].length
        messageBox = document.getElementById("messageBox")
        for(i = historyData["record"].length-1;  i >= 0; i--){
            hr = document.createElement('hr')
            messageRecord = document.createElement('div')
            messageRecord.setAttribute("id","messageRecord")
            messageRecord.textContent = historyData["record"][i]["message"]
            img = document.createElement('img')
            img.setAttribute("id","img")
            recordFileName = historyData["record"][i]["s3-URL"].split('/messageBoard/')[1]
            img.src = 'https://d3qig2ybk47ceb.cloudfront.net/messageBoard/'+recordFileName
            messageBox.append(hr)
            messageBox.append(messageRecord)
            messageBox.append(img)
        }
    }

}

function renderNew(newData){
    hr = document.createElement('hr')
    messageBox = document.getElementById("messageBox")
    messageRecord = document.createElement('div')
    messageRecord.setAttribute("id","messageRecord")
    messageRecord.textContent = newData["record"]["message"]
    img = document.createElement('img')
    img.setAttribute("id","img")
    newRecordFileName = newData["record"]["s3-URL"].split('/messageBoard/')[1]
    img.src = 'https://d3qig2ybk47ceb.cloudfront.net/messageBoard/'+newRecordFileName
    refNode = document.getElementsByTagName('hr')[0];
    messageBox.insertBefore(hr, refNode);
    messageBox.insertBefore(messageRecord, refNode);
    messageBox.insertBefore(img, refNode);

}

