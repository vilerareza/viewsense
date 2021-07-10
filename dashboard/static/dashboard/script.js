
const xhr = new XMLHttpRequest;

//const targetHost = 'https://viewsense.herokuapp.com/dashboard/status'
//const targetHost = 'http://127.0.0.1:8000/dashboard/status';

const targetHost = 'http://52.224.63.202:80/dashboard/status';

xhr.onreadystatechange = function(){
    console.log(xhr.readyState);

    if (xhr.readyState==4 && xhr.status==200){
        console.log('getting response');
        let data = JSON.parse(this.responseText);
        let status = data.status;
        let address = data.camera_address;
        console.log(status);
        //console.log(JSON.stringify(data.status));
        const status_label = document.getElementById("status_label");
        //Updating status label style
        switch(status){
            case 'No Camera Connection':
                status_label.innerHTML = status;
                status_label.style.backgroundColor = "#FF4A53";
                console.log('no camera connection');
                break;
            case 'Connected':
                status_label.innerHTML = `${status}, Cam IP: ${address}`;
                status_label.style.backgroundColor = "#00B050";
                console.log('connected');
                //status_label.style.backgroundColor = "#0088FF";
        }

        //Resend the request
        xhr.open('GET', targetHost);
        xhr.send();
        console.log('sent');
    }
}

// Send the request
xhr.open('GET', targetHost);
xhr.send();
console.log('sent initial ok');
