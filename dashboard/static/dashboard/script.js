
//const targetHost = 'https://viewsense.herokuapp.com/dashboard/status'
const targetHost = 'http://156.67.217.141/dashboard/status';
//const targetHost = 'http://52.224.63.202:80/dashboard/status';
//const targetHost = 'http://viewsense-rv.eastus.cloudapp.azure.com/dashboard/status';


update_label = (status, address)=>{
    console.log(status, address);
    const status_label = document.getElementById("status_label");
    //Updating status label style
    switch(status){
        case 'No Camera Connection':
            status_label.innerHTML = status;
            status_label.style.backgroundColor = "#FF4A53";
            break;
        case 'Connected':
            status_label.innerHTML = `${status}, Cam IP: ${address}`;
            status_label.style.backgroundColor = "#00B050";
    }
}

async function update_status(){

    while (true){
        console.log('fething status...');
        response = await fetch (targetHost);
        if (response.status == 200) {
            response.json().then (data => update_label(data.status, data.camera_address));
            console.log(`fetch received`)    
        }
    }
}

update_status();


//const xhr = new XMLHttpRequest;
//xhr.timeout=0;

//xhr.ontimeout = function(){console.log('status timeout');}

//xhr.onerror = function(){console.log('status error');}

//xhr.onreadystatechange = function(){
//    console.log(xhr.readyState);

//    if (xhr.readyState==4 && xhr.status==200){
//        console.log('getting response');
//        let data = JSON.parse(this.responseText);
//        let status = data.status;
//        let address = data.camera_address;
//        console.log(status);
        //console.log(JSON.stringify(data.status));
//        const status_label = document.getElementById("status_label");
        //Updating status label style
//        switch(status){
//            case 'No Camera Connection':
//                status_label.innerHTML = status;
//                status_label.style.backgroundColor = "#FF4A53";
//                console.log('no camera connection');
//                break;
//            case 'Connected':
//                status_label.innerHTML = `${status}, Cam IP: ${address}`;
//                status_label.style.backgroundColor = "#00B050";
//                console.log('connected');
                //status_label.style.backgroundColor = "#0088FF";
//        }

        //Resend the request
//        xhr.open('GET', targetHost);
//        xhr.send();
//        console.log('sent');
//    }
//}

// Send the request
//xhr.open('GET', targetHost);
//xhr.send();
//console.log('sent initial oke');
