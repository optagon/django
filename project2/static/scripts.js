// Execute when the DOM is fully loaded
document.addEventListener('DOMContentLoaded', () => {

    var socket = io.connect('http://' + document.domain + ':' + location.port);
    var my_storage = window.localStorage;
    socket.on('connect', () => {
        if (my_storage.getItem('channel')) {
        
            socket.emit("join_channel", my_storage.getItem('channel'));
        }
        else {
            document.querySelector("#chat").style.display = "none";
        }
        if(!my_storage.getItem('username')) {
            document.querySelector("#starter_button").disabled = false;
            document.querySelector("#create_button").disabled = true;
            document.querySelector("#channel_list").style.display = "none";
        }

        else {
            document.querySelector("#starter_button").disabled = true;
            document.querySelector("#create_button").disabled = false;
            document.querySelector("#channel_list").style.display = "block";
            socket.emit("username", my_storage.getItem("username"));
        }
        
    });

    socket.on('join_channel', data => {
        my_storage.setItem('channel', data["channel"]);
        document.querySelector("#messages").innerHTML = "";
        document.querySelector("#chathead").innerHTML = data["channel"];
        document.querySelector("#chat").style.display = "block";
        var x;
        for (x in data["messages"]) {
            const li = document.createElement('li');
            li.innerHTML = `<strong>${data["messages"][x].user}:</strong> <div><span>${data["messages"][x].msg}</span></div> <small>(${data["messages"][x].my_time})</small>`;
            document.querySelector("#messages").append(li);
        }
    });
    socket.on('leave_channel', channel => {
        my_storage.removeItem("channel");
        document.querySelector("#chathead").innerHTML = "";
        document.querySelector("#chat").style.display = "none";
    });
    socket.on('channel_error', msg => {
        alert(msg);
    });
    socket.on('room_message', data => {
        console.log("Message received!");
        const li = document.createElement('li');
        li.innerHTML = `<strong>${data.user}:</strong> <div><span>${data.msg}</span></div> <small>(${data.my_time})</small>`;
        document.querySelector("#messages").append(li);
    });
    document.querySelector("#sendbutton").onclick = () => {
        msg = document.querySelector("#my_message").value;
        user = my_storage.getItem('username');
        const channel = my_storage.getItem('channel');
        socket.emit('room_message',{'msg': msg, 'user': user, 'channel': channel});
        document.querySelector("#my_message").value = '';
    };
    document.querySelector("#leave_channel").onclick = () => {
        socket.emit("leave_channel", my_storage.getItem("channel"));
    };
    document.querySelectorAll(".my_channel").forEach(li => {
        li.onclick = () => {
            socket.emit('change_channel', my_storage.getItem('channel'), li.dataset.channel);
        };
    });

    document.querySelector("#starter_form").onsubmit =  () => {
        my_storage.setItem('username', document.querySelector("#name").value);
        document.querySelector("#starter_button").disabled = true;
        document.querySelector("#create_button").disabled = false;
        document.querySelector("#channel_list").style.display = "block";
        document.querySelector("#name").value = "";
        socket.emit("username", my_storage.getItem('username'));
        return false;

    };
    document.querySelector("#create_channel").onsubmit = () => {
        const channel = document.querySelector("#channel").value;
        socket.emit("channel_creation", channel);
        return false;
    };
});