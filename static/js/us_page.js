 function changeAvatar() {
    document.getElementById('uploadInput').click();
    }

    function handleFileSelect() {
        let form = document.getElementById('uploadForm');
        let formData = new FormData(form);
        fetch('/upload', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById('avatar').src = data.avatarUrl;
            })
            .catch(error => console.error(error));
}