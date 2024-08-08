const chatSocket = new WebSocket("ws://" + window.location.host + "/");
console.log(`🚀  chatSocket:`, chatSocket)
chatSocket.onopen = function (e) {
    console.log("The connection was setup successfully!");
};
chatSocket.onclose = function (e) {
    console.log("Something unexpected happened !");
};

document.querySelector("#id_message_send_input").focus();
document.querySelector("#id_message_send_input").onkeyup = function (e) {
    if (e.keyCode == 13) {
        document.querySelector("#id_message_send_button").click();
    }
};

document.querySelector("#id_media_message_send_input").focus();
document.querySelector("#id_media_message_send_input").onkeyup = function (e) {
    if (e.keyCode == 13) {
        document.querySelector("#id_message_send_button").click();
    }
};


document.querySelector("#id_message_send_button").onclick = function (e) {
    var messageInput = document.querySelector(
        "#id_message_send_input"
    ).value;
    var messageMediaInput = document.querySelector(
        "#id_media_message_send_input"
    );

    if (messageInput) {
        chatSocket.send(JSON.stringify({ message: messageInput, username: `request.user.username`, type: "text" }));
    }
    if (messageMediaInput.value) {
        messageMediaInput.addEventListener('change', function (event) {
            const file = event.target.files[0];
            console.log(`🚀  file:`, file)
            const reader = new FileReader();
            reader.onload = (event) => {
                chatSocket.send(JSON.stringify({ message: event.target.result, username: `request.user.username`, type: "image" }));
            };
            reader.readAsDataURL(file);
        })
    }

};
chatSocket.onmessage = function (e) {
    const data = JSON.parse(e.data);
    const messages = data.message
    for (let index = 0; index < messages.length; index++) {
        const element = JSON.parse(messages[index]);
        var div = document.createElement("div");
        if (data.type == "text") {
            div.textContent = element.user + " : " + element.text;
        }

    }

    // var div = document.createElement("div");
    // var img = new Image();
    // if (data.type == "text") {
    //     div.textContent = data.username + " : " + data.message;
    // }
    // if (data.type === "image") {
    //     img.src = data.message;
    //     img.style.width = "100px"
    //     img.style.height = "100px"

    //     div.textContent = data.username + " : ";
    //     div.appendChild(img);
    // }
    document.querySelector("#id_message_send_input").value = "";
    document.querySelector("#id_media_message_send_input").value = null;
    document.querySelector("#id_chat_item_container").appendChild(div);
};